import requests as r
#from sqlalchemy.testing.provision import update_db_opts



def add_user():
    data = {"username":"Alex","password": "Alex123", "user_mail": "den@den.com"}
    response = r.post("http://127.0.0.1:8000/users/user_registration", json=data)
    print(response.text)
    print(response.status_code)


def get_token():
    data ={
  "user_mail": "alexander@den.com",
  "password": "Alex123"
    }
    response = r.post("http://127.0.0.1:8000/login", json=data)
    print(response.text)
    return response.json()["access_token"]

def add_project():
    headers = {"Authorization": f"Bearer {get_token()}"}
    data = {"title": "some test title1", "description": "some test descrition1", "link":"some test link1"}
    response = r.post("http://127.0.0.1:8000/projects/new_project", json=data,  headers=headers)
    print(response.text)
    print(response.status_code)

def update_user():
    data = {"username":"alex great"}
    token = f"Bearer {get_token()}"
    headers = {"Authorization": token}
    response = r.put("http://127.0.0.1:8000/users/2", json=data, headers=headers)
    print(response.text)
    print(response.status_code)

    # def get_user():
    #     token = f"Bearer {get_token()}"
    #     headers = {"Authorization": token}
    #     response = r.get("http://127.0.0.1:8000/user_update/1", json=data, headers=headers)
    #     print(response.text)
    #     print(response.status_code)

if __name__ == "__main__":
    add_project()
    #update_user()

