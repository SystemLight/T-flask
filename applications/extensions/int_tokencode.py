import random
import time
from threading import Thread


class TokenCodeNotSetError(Exception):
    ...


def _on_gen_token():
    return "".join([
        str(random.randint(0, 9)),
        str(random.randint(0, 9)),
        str(random.randint(0, 9)),
        str(random.randint(0, 9))
    ])


class TokenCode:

    def __init__(self, auto_run=True, expire_time=300, retries=5, token_byte_size=3, on_gen_token=None):
        self._token_pool = {}

        self.expire_time = expire_time
        self.retries = retries
        self.token_byte_size = token_byte_size

        if on_gen_token is None:
            self.on_gen_token = _on_gen_token
        else:
            self.on_gen_token = on_gen_token

        self.is_running = True
        self.thread = None

        if auto_run:
            self.run()

    def __len__(self):
        return len(self._token_pool)

    def get_token(self, k):
        return self._token_pool.get(k, {'value': None})['value']

    def set_token(self, v):
        k = self.retry_token()

        if k is None:
            raise TokenCodeNotSetError('Duplicate key values exist and cannot be saved')

        self._token_pool[k] = {
            'value': v,
            'expire': time.time() + self.expire_time
        }
        return k

    def retry_token(self):
        now_try_num = 0
        while now_try_num < self.retries:
            k = self.on_gen_token()
            if self._token_pool.get(k, None) is None:
                return k
            now_try_num += 1
        return None

    def loop_clear(self):
        while self.is_running:
            for k in list(self._token_pool.keys()):
                if self._token_pool[k]['expire'] < time.time():
                    try:
                        del self._token_pool[k]
                    except KeyError:
                        ...
            time.sleep(1)

    def run(self):
        self.is_running = True
        self.thread = Thread(target=self.loop_clear)
        self.thread.setDaemon(True)
        self.thread.start()

    def stop(self):
        self.is_running = False


tc = TokenCode(expire_time=600)
