# T-flask

> Flask项目开发模板

## 技术栈

### 后端

- [werkzeug](https://www.osgeo.cn/werkzeug/)
- [flask](https://dormousehole.readthedocs.io/en/latest/index.html)
- [gevent](https://www.gevent.org/contents.html)
- [gevent-websocket](https://gitlab.com/noppo/gevent-websocket)
- [webargs](https://webargs.readthedocs.io/en/latest/)
- [pillow](https://pillow.readthedocs.io/en/stable/)
- [captcha](https://github.com/lepture/captcha)
- [python-dotenv](https://saurabh-kumar.com/python-dotenv/#getting-started)
- [pymysql](https://pymysql.readthedocs.io/en/latest/modules/connections.html)
- [sqlalchemy](https://docs.sqlalchemy.org/en/14/contents.html)
- [alembic](https://alembic.sqlalchemy.org/en/latest/)
- [sqlacodegen](https://github.com/agronholm/sqlacodegen)
- [marshmallow](https://marshmallow.readthedocs.io/en/stable/)
- [marshmallow-sqlalchemy](https://marshmallow-sqlalchemy.readthedocs.io/en/latest/index.html)
- [flask-sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/)
- [flask-sqlacodegen](https://github.com/ksindi/flask-sqlacodegen)
- [flask-migrate](https://github.com/miguelgrinberg/Flask-Migrate)
- [flask-marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/index.html)
- [flask-socketio](https://flask-socketio.readthedocs.io/en/latest/)

### 前端

- [jquery](https://jquery.cuishifeng.cn/)
- [underscore](https://www.underscorejs.com.cn/)
- [layui](https://www.layuiweb.com/doc/index.htm)
- [notify](https://gitee.com/u33/notify)
- [layui 第三方组件平台](https://layui.org.cn/fly/extend/index.html)
- [socketio](https://socket.io/)

## 用法

1. T-flask默认使用 `pipenv` 作为包管理器，如果没有安装请执行下面命令

```shell
pip install pipenv

安装后添加环境变量
PIPENV_VENV_IN_PROJECT = 1
PIPENV_PYPI_MIRROR = https://mirrors.aliyun.com/pypi/simple/
```

2. 还原依赖环境

```
pipenv install
```

3. T-flask默认使用阿里源仓库作为安装源

```shell
[[source]]
url = "https://mirrors.aliyun.com/pypi/simple/"
verify_ssl = true
name = "aliyun"
```

4. 部署nginx代理uwsgi配置

- uwsgi管理

```shell
# 启动uWSGI服务器
uwsgi --ini ./uwsgi.ini

# 停止指定uwsgi
uwsgi --stop uwsgi.pid

# 停止所有uwsgi
pkill -f uwsgi -9
 
# 查看所有uWSGI进程
ps aux | grep uwsgi

# 重启uWSGI服务器
service uwsgi restart
```

- 宝塔面板：Python项目管理器配置uwsgi.ini

```text
[uwsgi]
project = t-flask
socket = 127.0.0.1:5000
chmod-socket = 666
uid = root
gid = root
chdir = /www/wwwroot/%(project).lisys.club/server
logto = ./info.log
wsgi-file= ./wsgi.py
callable = app
vacuum = True
http-keepalive = True
master = True
processes = 1
threads = 128
max-requests = 5000
```

- uwsgi直接命令行启动运行

```text
[uwsgi]
project = t-flask
socket = 127.0.0.1:5000
chmod-socket = 666
uid = root
gid = root
chdir = .
venv = ./.venv
pidfile = ./uwsgi.pid
daemonize = ./%(project).log
wsgi-file= ./wsgi.py
callable = app
vacuum = True
http-keepalive = True
master = True
processes = 1
threads = 128
max-requests = 5000
```

- uwsgi启动并且支持websocket访问

```text
[uwsgi]
project = t-flask
http = 127.0.0.1:5555
http-websockets = True
uid = root
gid = root
chdir = .
venv = ./.venv
pidfile = ./uwsgi.pid
daemonize = ./%(project).log
wsgi-file= ./wsgi.py
callable = app
vacuum = True
http-keepalive = True
master = True
processes = 1
threads = 128
gevent = 1000
async = 30
max-requests = 5000
```

- 配置nginx代理：/etc/nginx/sites-enabled/default

```text
# 普通socket代理
location / {
    include uwsgi_params;
    uwsgi_pass 127.0.0.1:5000;
}

# SSE支持
location ^~ /api/file/subscribe/ {
    include uwsgi_params;
    uwsgi_pass 127.0.0.1:5001;
    uwsgi_buffering off;
}

# websocket支持（版本要求1.4以上）
# 反向代理可能会跨域，设置SocketIO跨域参数即可
# uwsgi不要启用多进程
location / {
    proxy_pass http://127.0.0.1:5000;
    proxy_cookie_domain domino_server nginx_server;
    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}

location /socket.io/ {
    proxy_pass http://127.0.0.1:5000/socket.io/;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}
```

- Flask: SSE支持代码

```python
def stream():
    yield 'data: {}\n\n'


@app.route('/message', methods=['GET'])
def message():
    return Response(stream(), mimetype="text/event-stream")
```

5. 数据库管理

```shell
# 数据库初始化
flask initdb

# 数据库迁移
flask db init
flask db migrate -m "add note timestamp"
flask db upgrade

# 数据库回滚
flask db downgrade

# 反向生成数据模型
flask-sqlacodegen mysql+pymysql://root:password@127.0.0.1/db_name --outfile "model.py"  --flask
```

## License

T-flask uses the MIT license, see LICENSE file for the details.
