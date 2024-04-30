from httpx import request

from ...main import app

#users api
def test_get_all_users():
    response = request('GET', "http://127.0.0.1:8000/users/")
    assert response.status_code == 200
    
    
def test_get_user_by_login_not_found():
    response = request('GET', "http://127.0.0.1:8000/users/?login=kim")
    assert response.status_code == 404


def test_post_user():
    response = request("POST", r"http://127.0.0.1:8000/users/?name=%D0%9A%D0%B0%D0%BB%D0%B8%D0%BD%D0%B8%D0%BD&surname=%D0%98%D0%B3%D0%BE%D1%80%D1%8C&patronymic=%D0%9C%D0%B8%D1%85%D0%B0%D0%B9%D0%BB%D0%BE%D0%B2%D0%B8%D1%87&mail=mail%40asu.ru&login=kim&pwd=qwerty")
    assert response.status_code == 200


def test_post_user_duplicate():
    response = request("POST", r"http://127.0.0.1:8000/users/?name=%D0%9A%D0%B0%D0%BB%D0%B8%D0%BD%D0%B8%D0%BD&surname=%D0%98%D0%B3%D0%BE%D1%80%D1%8C&patronymic=%D0%9C%D0%B8%D1%85%D0%B0%D0%B9%D0%BB%D0%BE%D0%B2%D0%B8%D1%87&mail=mail%40asu.ru&login=kim&pwd=qwerty")
    assert response.status_code == 409
    
    
def test_get_user_by_login():
    response = request('GET', "http://127.0.0.1:8000/users/?login=kim")
    assert response.status_code == 200
    
    
def test_get_user_by_id_not_found():
    response = request('GET', "http://127.0.0.1:8000/users/999999999")
    assert response.status_code == 404
    
    
def test_get_user_by_id():
    response = request('GET', "http://127.0.0.1:8000/users/?login=kim")
    user_id = response.json()["id"]
    response = request('GET', f"http://127.0.0.1:8000/users/{user_id}")
    assert response.status_code == 200


def test_put_user():
    response = request('GET', "http://127.0.0.1:8000/users/?login=kim")
    user_id = response.json()["id"]
    response = request('PUT', f"http://127.0.0.1:8000/users/{user_id}?name=%D0%98%D0%BC%D1%8F&surname=%D0%A4%D0%B0%D0%BC%D0%B8%D0%BB%D0%B8%D1%8F&patronymic=%D0%9E%D1%82%D1%87%D0%B5%D1%81%D1%82%D0%B2%D0%BE&mail=mail%40mail.asu.ru&login=lll&pwd=pwd&verified=true")
    assert response.status_code == 200
    
def test_put_user_conflict():
    request("POST", r"http://127.0.0.1:8000/users/?name=%D0%9A%D0%B0%D0%BB%D0%B8%D0%BD%D0%B8%D0%BD&surname=%D0%98%D0%B3%D0%BE%D1%80%D1%8C&patronymic=%D0%9C%D0%B8%D1%85%D0%B0%D0%B9%D0%BB%D0%BE%D0%B2%D0%B8%D1%87&mail=mail%40asu.ru&login=kim&pwd=qwerty")
    response = request('GET', "http://127.0.0.1:8000/users/?login=lll")
    user_id = response.json()["id"]
    response = request('PUT', f"http://127.0.0.1:8000/users/{user_id}?name=%D0%9A%D0%B0%D0%BB%D0%B8%D0%BD%D0%B8%D0%BD&surname=%D0%98%D0%B3%D0%BE%D1%80%D1%8C&patronymic=%D0%9C%D0%B8%D1%85%D0%B0%D0%B9%D0%BB%D0%BE%D0%B2%D0%B8%D1%87&mail=mail%40asu.ru&login=kim&pwd=qwerty&verified=true")
    assert response.status_code == 409
    
    
def test_patch_user():
    response = request('GET', "http://127.0.0.1:8000/users/?login=kim")
    user_id = response.json()["id"]
    response = request('PATCH', f"http://127.0.0.1:8000/users/{user_id}?name=%D0%98%D0%BC%D1%8F&surname=%D0%A4%D0%B0%D0%BC%D0%B8%D0%BB%D0%B8%D1%8F&patronymic=%D0%9E%D1%82%D1%87%D0%B5%D1%81%D1%82%D0%B2%D0%BE&mail=mail%40maill.asu.ru&login=llll&pwd=pwd&verified=true")
    assert response.status_code == 200
    
    
def test_patch_user_not_found():
    response = request('PATCH', r"http://127.0.0.1:8000/users/9999999?name=%D0%98%D0%BC%D1%8F&surname=%D0%A4%D0%B0%D0%BC%D0%B8%D0%BB%D0%B8%D1%8F&patronymic=%D0%9E%D1%82%D1%87%D0%B5%D1%81%D1%82%D0%B2%D0%BE&mail=mail%40mail.asu.ru&login=lll&pwd=pwd&verified=true")
    assert response.status_code == 404
    
    
def test_patch_user_conflict():
    response = request('GET', "http://127.0.0.1:8000/users/?login=lll")
    user_id = response.json()["id"]
    response = request('PATCH', f"http://127.0.0.1:8000/users/{user_id}?name=%D0%9A%D0%B0%D0%BB%D0%B8%D0%BD%D0%B8%D0%BD&surname=%D0%98%D0%B3%D0%BE%D1%80%D1%8C&patronymic=%D0%9C%D0%B8%D1%85%D0%B0%D0%B9%D0%BB%D0%BE%D0%B2%D0%B8%D1%87&mail=mail%40asu.ru&login=llll&pwd=qwerty&verified=true")
    assert response.status_code == 409
    
    
def test_delete_user():
    response = request('GET', "http://127.0.0.1:8000/users/?login=lll")
    user_id = response.json()["id"]
    response = request('DELETE', f"http://127.0.0.1:8000/users/{user_id}")
    assert response.status_code == 200