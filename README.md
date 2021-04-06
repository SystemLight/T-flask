# T-flask

flask项目开发模板

## 用法

1. T-snake默认使用 `pipenv` 作为包管理器，如果没有安装请执行下面命令

```
pip install pipenv

安装后添加环境变量
PIPENV_VENV_IN_PROJECT = 1
```

2. 还原依赖环境

```
pipenv install
```

3. T-flask默认使用阿里源仓库作为安装源

4. 注意事项

- 控制器和视图中的blue_print变量会自动注册蓝图，如果没有识别到会抛出异常

## License

T-flask uses the MIT license, see LICENSE file for the details.

```
在项目根目录下执行命令

启动：uwsgi --ini uwsgi.ini

重启：uwsgi --reload uwsgi.pid

停止：uwsgi --stop uwsgi.pid
```
