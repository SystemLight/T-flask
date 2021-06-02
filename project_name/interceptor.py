def init_app(app):
    @app.errorhandler(400)
    def bad_request(e):
        """

        集中处理400错误

        :param e:
        :return:

        """
        data = getattr(e, "data", None)
        if data:
            return {"data": data, "code": e.code}
        return e
