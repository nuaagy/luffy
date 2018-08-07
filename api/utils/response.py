class BaseResponse:
    def __init__(self):
        self.code = 1
        self.data = None
        self.error = None

    @property
    def dict(self):
        return self.__dict__