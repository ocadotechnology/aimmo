from aimmo.exceptions import LimitExceeded

class LimitExceededMiddleware:
    def process_exception(self, request, exception):
        if isinstance(exception, LimitExceeded):
            # TODO: Return view
            print(request)
            print("Too many games!")

        return None
