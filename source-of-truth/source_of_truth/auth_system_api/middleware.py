from django.http.response import JsonResponse
import json

ACCESS_TYPE = ('Content-Type', 'application/json')

class ResponseMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response._headers.get('content-type') == ACCESS_TYPE:
            json_data = json.loads(response.content.decode('utf8'))
            
            new_json = {}
            for key, value in zip(json_data.keys(), json_data.values()):
                good_key = "".join(map(str.capitalize, key.split("_")))
                new_json[good_key] = value
            return JsonResponse(new_json)
        else:
            return response