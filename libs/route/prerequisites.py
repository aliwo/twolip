from functools import wraps
from flask import g


class prerequisites:

    def __init__(self, inspector, func_name):
        self.inspector = inspector()
        self.inspect_func_name = func_name

    def __call__(self, func):
        @wraps(func)
        def decorated(*args, **kwargs):
            getattr(self.inspector, self.inspect_func_name)()
            g.pr_result = self.inspector.get_result()
            return func(*args, **kwargs)
        return decorated
