class SimpleCORSMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Para requisições OPTIONS (Preflight), respondemos diretamente com status 200
        if request.method == "OPTIONS":
            from django.http import HttpResponse
            response = HttpResponse()
        else:
            response = self.get_response(request)

        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Headers"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        return response
