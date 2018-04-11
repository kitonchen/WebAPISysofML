# coding=utf-8
class ApiException(Exception):
    status_code = 400

    def __init__(self, message, detail, status_code=400):
        Exception.__init__(self)
        self.status_code = status_code
        self.message = message
        self.detail = detail
