import requests


BASE_URL = 'http://127.0.0.1:5000/'

# Testing auth
def test_login():
    URL = 'http://127.0.0.1:5000/auth/login'
    login_data = {
        "admin": "drea",
        "password": "31Scrabble&Scoreboard10"
    }
    response = requests.post(URL, json=login_data)
    print(response.text)

def test_refresh():
    URL = 'http://127.0.0.1:5000/auth/refresh'
    headers = {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MTE2MzE5OTYsIm5iZiI6MTYxMTYzMTk5NiwianRpIjoiNzlmMWZlODktMGU4My00ZDM5LTg0ZDktNTYyZDAyZWZkNjI3IiwiZXhwIjoxNjE0MjIzOTk2LCJpZGVudGl0eSI6MSwidHlwZSI6InJlZnJlc2gifQ.9tCBTWvXfVV1TBJWFalD16thMHtxyQ_3oRhDEAhEsvg"}
    response = requests.post(URL, headers=headers)
    print(response.text)

def test_new_player():
    URL = 'http://127.0.0.1:5000/api/v1/players'
    headers = {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MTE2MzE5OTYsIm5iZiI6MTYxMTYzMTk5NiwianRpIjoiZjUxMTBlNjQtYzYzMy00YjQxLTgyYmUtM2E4ZDEzOTNlMjkyIiwiZXhwIjoxNjExNjMyODk2LCJpZGVudGl0eSI6MSwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.-eG30wZrEEgfgkpYCnYj48H95kh6FT6KeLrHlDOEPb4"}
    player_data = {
        'name': "Álvaro"
    }
    response = requests.post(URL, json=player_data, headers=headers)
    print(response.text)

def test_get_all_players():
    URL = 'http://127.0.0.1:5000/api/v1/players'
    headers = {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MTE2MzE5OTYsIm5iZiI6MTYxMTYzMTk5NiwianRpIjoiZjUxMTBlNjQtYzYzMy00YjQxLTgyYmUtM2E4ZDEzOTNlMjkyIiwiZXhwIjoxNjExNjMyODk2LCJpZGVudGl0eSI6MSwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.-eG30wZrEEgfgkpYCnYj48H95kh6FT6KeLrHlDOEPb4"}
    response = requests.get(URL, headers=headers)
    print(response.text)

if __name__ == "__main__":
    test_refresh()
