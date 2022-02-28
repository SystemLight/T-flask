import copy
import queue
import time
import weakref
from threading import Thread
from collections import defaultdict

from flask import Response, stream_with_context


class Ping:
    ...


class Recycle:
    ...


class Stream:

    def __init__(self, _sse, stream_func):
        self.sse = _sse
        self.deal_ping = lambda *args: 'ping'
        self.deal_recycle = lambda *args: 'recycle'
        self.deal_message = stream_func

    def stream(self, key: str, *args):
        while True:
            for i in self.sse.listen(key):
                if isinstance(i, self.sse.Ping):
                    yield self.sse.message(self.deal_ping(*args))
                elif isinstance(i, self.sse.Recycle):
                    yield self.sse.message(self.deal_recycle(*args))
                else:
                    yield self.sse.message(self.deal_message(i, *args))

    def response(self, key, *args):
        return Response(stream_with_context(self.stream(key, *args)), mimetype="text/event-stream")

    def on_ping(self, func):
        self.deal_ping = func

    def on_recycle(self, func):
        self.deal_recycle = func


class Monitor:

    def __init__(self, q):
        self.q = q
        self.update_time = time.time()
        self.is_recycle = False

    def put(self, value):
        self.q.put(value, block=False)
        self.update_time = time.time()

    def get(self, timeout):
        return self.q.get(timeout=timeout)

    @property
    def livetime(self):
        return time.time() - self.update_time


class ServerSentEvents:
    Ping = Ping
    Recycle = Recycle

    def __init__(self, app=None):
        self._event_pool = defaultdict(lambda: weakref.WeakSet())
        self._is_thread_flag = True
        self._thread = Thread(target=self._run_gc_task, daemon=True)

        if app:
            self.init_app(app)

    @staticmethod
    def message(data):
        return f'data: {data}\n\n'

    @staticmethod
    def response(gen_func):
        def wrap(*args):
            return Response(stream_with_context(gen_func(*args)), mimetype="text/event-stream")

        return wrap

    def init_app(self, app):
        self.app = app
        self.maxsize = self.app.config.get('SSE_MAXSIZE', 0)  # 派发n次无消费者则销毁
        self.overtime = self.app.config.get('SSE_OVERTIME', 1800)  # 超过30分钟无消费者
        self.ping_time = self.app.config.get('SSE_PING_TIME', 1)  # 固定时间内无数据派发则派发一个ping包
        self.sse_gc = self.app.config.get('SSE_GC', False)  # 是否开启自动gc回收超时容器

        if self.sse_gc:
            self._thread.start()

    def pop_queue(self, key, mo: Monitor):
        if not isinstance(key, str):
            raise ValueError('key must be a string')
        try:
            mo.is_recycle = True
            self._event_pool[key].remove(mo)
        except ValueError:
            ...

    def clear(self, key):
        self._event_pool.pop(key)

    def emit(self, key: str, args=None):
        for mo in copy.copy(self._event_pool[key]):
            try:
                mo.put(args)
            except queue.Full:
                self.pop_queue(key, mo)  # 超出给定次数无人消费清除
                continue

    def listen(self, key: str):
        mo = Monitor(queue.Queue(maxsize=self.maxsize))
        self._event_pool[key].add(mo)
        while True:
            try:
                yield mo.get(timeout=self.ping_time)
            except queue.Empty:
                if mo.is_recycle:
                    break
                yield Ping()
        yield Recycle()

    def stream(self, func):
        return Stream(self, func)

    def _run_gc_task(self):
        while self._is_thread_flag:
            time.sleep(1)
            self.gc()

    def gc(self):
        for key in self._event_pool:
            self.gc_key(key)

    def gc_key(self, key):
        old_collect = []
        for mo in self._event_pool[key]:
            if mo.livetime > self.overtime:
                old_collect.append(mo)
        for mo in old_collect:
            self.pop_queue(key, mo)

    def close(self):
        self._is_thread_flag = False
        time.sleep(2)
        self._event_pool = None


sse = ServerSentEvents()


def init_sse(app):
    sse.init_app(app)
