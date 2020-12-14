import requests


class DataService:
    BASE_DATA_SERVICE_PATH = "http://192.168.32.89:8000"

    def authorize_user_by_request(self, request):
        """Make request to get session from server service/"""
        url = f"{self.BASE_DATA_SERVICE_PATH}/Auth"

        credentials = {
            'username': request.POST["username"],
            'password': request.POST["password"]
        }

        session = requests.Session()
        response_with_session = session.post(url, data=credentials)
        return response_with_session

    def get_user_data(self, request):
        cookies = {**request.COOKIES, "sessionid": request.user.session_id_for_data_service}
        s = requests.Session()
        url = f"{self.BASE_DATA_SERVICE_PATH}/GetPerson"
        req = requests.Request("GET", url, cookies=cookies)
        req = s.prepare_request(req)
        response = s.send(req)
        return response.json()
