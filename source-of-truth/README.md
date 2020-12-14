## Source-of-truth
___
Этот сервис нужен для хранения всей информации о пользователях зарегистрированных в сервисе __auth_portal__

## Команды работы с сервисом
___
<br>

__1. `/Auth`__

С помощью этого запроса пользователь получает информацию о своей сессии
Для авторизации нужно отправить `username` и `password` в формате _form-data_

__Example:__
```py
import requests

url = "http://localhost/Auth"

payload={
    'username': <username>,
    'password': <password>
    }

response = requests.request("POST", url, data=payload)
```

__Positive Response:__

```json
{
    "SessionId": 123123, 
    "ErrorCode": "",
    "Permission": "READ"
}
```

__Negative Response:__
```json
{
    "ErrorCode": "Incorrect user name or password",
    "Permission": "READ",
    "SessionId": 0
}
```
<br>

__2. `/GetPerson[?personId=123]`__

Этот запрос может выполнять только авторизованный ранее пользователь. 
Нужен для получения информации о авторизованном пользователе или указанном в queryString

__Example:__
```py
import requests

url = "http://localhost/GetPerson"

headers = {
  'Cookie': 'csrftoken=<csrftoken>; sessionid=<session_id>'
}

response = requests.request("GET", url, headers=headers)
```

__Positive Response:__
```json
{
    'ErrorCode': '',
    'Permission': 'READ',
    'Profile': {
        'Email': 'ivan.ivanov@site.com',
        'Username': 'ivan.ivanov',
        'FirstName': 'Иван',
        'LastName': 'Иванов',
        'Phone': '+375 29 111 11 11',
        'Skype': 'ivan.ivanov'
        }
}
```

__Negative Response:__ (Не авторизованный user)
```json
{
    "ErrorCode":"Session expired",
    "Permission":"READ",
    "Profile":null
}
```

__Negative Response:__ (Запрашеваеммый пользователь не существует)
```json
{
    "ErrorCode":"",
    "Permission":"READ",
    "Profile":null
}
```
<br>

__3. `/GetAllPerson`__
Запрос предоставляет информацию о всех пользователях зарегистрированных в системе.

__Example:__
```py
import requests

url = "http://localhost/GetAllPerson"


headers = {
  'Cookie': 'csrftoken=<csrftoken>; sessionid=<session_id>'
}

response = requests.request("GET", url, headers=headers)
```

__Positive Response:__
```json
{
    "ErrorCode": "",
    "Permission": "READ",
    "Users": [
        {
            "Email": "Aaron@mail.ru",
            "Username": "Aaron",
            "First_Name": "Aaron",
            "Last_Name": "Scott",
            "Phone": "+375297750511",
            "Skype": "Aaron.Scott"
        },
        {
            "Email": "German@mail.ru",
            "Username": "German",
            "First_Name": "German",
            "Last_Name": "Sanchez",
            "Phone": "+375294226313",
            "Skype": "German.Sanchez"
        },
        {...}
}
```

__Negative Response:__ (Не авторизованный user)
```json
{
    "ErrorCode": "Session expired",
    "Permission": "READ",
    "Users": []
}
```
<br>

__4. `/logout`__
Метод разлогинивает пользователя из системы и теперь чтобы получить доступ к данным, опять нужно авторизоваться

__Example:__
```py
import requests

url = "http://localhost/logout"

response = requests.request("GET", url)
```