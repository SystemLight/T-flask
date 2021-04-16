# T-flask

Flask项目开发模板

## 安装依赖

```python
# 添加环境变量
PIPENV_VENV_IN_PROJECT = 1

pipenv install
```

## 初始化数据库

```shell
flask initdb
```

## 运行

```shell
flask run
```

## 部署nginx代理uwsgi配置

```
location / {
    include uwsgi_params;
    uwsgi_pass unix:[PROJECT_PATH]/uwsgi.sock
}
```

## License

T-flask uses the MIT license, see LICENSE file for the details.
