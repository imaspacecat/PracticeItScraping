import requests as req
from dotenv import dotenv_values

root = "https://practiceit.cs.washington.edu"
url_login = root + "/login"

config = dotenv_values(".env")

payload = {
    'usernameoremail': config['EMAIL'],
    'password': config['PASSWORD']
}

s = req.sessions.session()
r = s.post(url_login, data=payload)
problems_solved = s.get("https://practiceit.cs.washington.edu/user/problems-solved").text
print(problems_solved)

with open('links.txt', 'r') as f:
    for link in f:
        s.post(link)


