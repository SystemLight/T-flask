# T-flask

flask项目开发模板

## 用法

1. T-snake默认使用 `pipenv` 作为包管理器，如果没有安装请执行下面命令

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
    uwsgi_pass 127.0.0.1:5000
}
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

## License

T-flask uses the MIT license, see LICENSE file for the details.
