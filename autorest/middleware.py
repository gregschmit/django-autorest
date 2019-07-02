import time


class TimeDelayMiddleware(object):
    """
    Slow down the response for debugging.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if '/api/' in request.path:
            time.sleep(2)
        response = self.get_response(request)
        return response
