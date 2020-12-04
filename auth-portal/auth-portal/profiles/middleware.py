import datetime

from django.contrib.auth import logout
from django.shortcuts import redirect


class CheckSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        exp = request.session.get("expire_date")

        if exp:
            expire_date = datetime.datetime.strptime(request.session.get("expire_date"), "%Y-%m-%dT%H:%M:%S.%f")
            current_time = datetime.datetime.now()
            if expire_date - current_time < datetime.timedelta():
                logout(request)
                return redirect("login")
        return response


