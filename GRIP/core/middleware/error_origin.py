# core/middleware/error_origin.py

class ErrorOriginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        print("🚨 Exception caught:", type(exception).__name__, str(exception))
        return None
