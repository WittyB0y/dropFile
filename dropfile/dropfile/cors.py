class CorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # self.get_response = {}

    def __call__(self, request):
        response = self.get_response(request)
        # response = {}
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response