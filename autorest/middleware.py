"""
This module provides a slowdown middleware for developer debugging purposes.
"""

import time


class TimeDelayMiddleware:
    """
    Middleware for slowing down the response for debugging. Adjust the delay
    (in seconds) in the ``__init__`` method.
    """

    def __init__(self, get_response, delay=2):
        self.get_response = get_response
        self.delay = delay

    def __call__(self, request):
        if '/api/' in request.path:
            time.sleep(self.delay)
        response = self.get_response(request)
        return response
