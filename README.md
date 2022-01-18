# T-flask

> Flask项目开发模板

## 用法

1. T-flask默认使用 `pipenv` 作为包管理器，如果没有安装请执行下面命令

```shell
pip install pipenv

安装后添加环境变量
PIPENV_VENV_IN_PROJECT = 1
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
name = "pypi"
```

4. 部署nginx代理uwsgi配置

```
# 开启uwsgi
uwsgi --ini ./uwsgi.ini

# 配置/etc/nginx/sites-enabled/default
location / {
    include uwsgi_params;
    uwsgi_pass 127.0.0.1:5000;
}
```

```shell
# 停止指定uwsgi
uwsgi --stop uwsgi.pid

# 停止所有uwsgi
pkill -f uwsgi -9

# 启动uWSGI服务器
uwsgi --ini uwsgi.ini
 
# 重启uWSGI服务器
sudo service uwsgi restart
 
# 查看所有uWSGI进程
ps aux | grep uwsgi
 
# 停止所有uWSGI进程
sudo pkill -f uwsgi -9
```

5. 初始化数据库

```shell
flask initdb
```

6. 数据库迁移

```shell
flask db init
flask db migrate -m "add note timestamp"
flask db upgrade

// 回滚
flask db downgrade
```

7. 反向生成数据模型

```shell
flask-sqlacodegen mysql+pymysql://root:password@127.0.0.1/db_name --outfile "model.py"  --flask
```

8. websocket支持

- 服务端预装依赖模块

    - flask-socketio
    - gevent
    - gevent-websocket

- 客户端依赖

    - socketio

- uwsgi配置必须启用HTTP模式，同时不要启用多个进程工作，使用NGINX的负载均衡代替这个选项

```
[uwsgi]
master = True
http = 127.0.0.1:5555
http-websockets = True
gevent = 1000
async = 30
project = t-flask
home = ./.venv
chdir = .
module = app
callable = app
processes = 1
max-requests = 5000
pidfile = ./uwsgi.pid
daemonize = ./%(project).log
vacuum = True
```

- nginx配置（版本要求1.4以上才能支持websocket代理）

```
location / {
    proxy_cookie_domain domino_server nginx_server;
    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_pass http://127.0.0.1:5000;
}

location /socket.io/ {
    proxy_pass http://127.0.0.1:5000/socket.io/;

    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_http_version 1.1;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header Host $host;
}
```

- 注意事项：

    - 反向代理可能会跨域，设置SocketIO跨域参数即可
    - uwsgi不要启用多进程

## License

T-flask uses the MIT license, see LICENSE file for the details.
