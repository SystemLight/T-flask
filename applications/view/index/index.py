import time

from flask import render_template, Blueprint

from ...extensions import Task, sse

index_bp = Blueprint('Index', __name__, url_prefix='/')


@index_bp.route('/')
def index():
    return render_template('index/index.html')


@Task
def task():
    time.sleep(0.5)
    sse.emit('hello', str(time.time()))


@sse.stream
def stream(msg):
    return msg


@index_bp.route('/sse/stream', methods=['GET'])
def sse_stream():
    task.restart()
    return stream.response(key='hello')


@index_bp.route('/sse/stop')
def stop_task():
    task.destroy()
    return {}


@index_bp.route('/sse/memory')
def memory():
    return str(len(sse._event_pool['hello']))


@index_bp.route('/sse/page')
def sse_page():
    return render_template('sse/index.html')
