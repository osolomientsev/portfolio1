import requests as r
#from sqlalchemy.testing.provision import update_db_opts


def add_project():
    data = {"user_id":1,"title": "some test title", "description": "some test descrition", "link":"some test link"}
    response = r.post("http://127.0.0.1:8000/projects", json=data)
    print(response.text)
    print(response.status_code)

def add_user():
    data = {"username":"Alex","password": "Alex123", "user_mail": "alex@den.com"}
    response = r.post("http://127.0.0.1:8000/user_registration", json=data)
    print(response.text)
    print(response.status_code)


def get_token():
    data ={
  "user_mail": "alex@den.com",
  "password": "Alex123"
    }
    response = r.post("http://127.0.0.1:8000/login", json=data)
    print(response.text)
    return response.json()["access_token"]



def update_user():
    data = {"username":"Alex"}
    token = f"Bearer {get_token()}"
    headers = {"Authorization": token}
    response = r.put("http://127.0.0.1:8000/user_update/1", json=data, headers=headers)
    print(response.text)
    print(response.status_code)

if __name__ == "__main__":
    add_project()
