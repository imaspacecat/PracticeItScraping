import requests as req
from dotenv import dotenv_values
import re
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from seleniumwire.utils import decode


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

links = re.findall("\/problem\/view.+(?=\")", problems_solved)

driver = webdriver.Chrome()
driver.get(url_login)
driver.find_element(By.NAME, "usernameoremail").send_keys(config['EMAIL'])
driver.find_element(By.NAME, "password").send_keys(config['PASSWORD'])
driver.find_element(By.ID, "submitbutton").submit()

f = open("links.txt", "a")

for link in links:
    driver.get(root + link)
    driver.find_element(By.ID, "solutionsubmit").click()
    for r in driver.requests:
        if r.url == "https://practiceit.cs.washington.edu/test/enqueue-job":
            data = decode(r.body, r.headers.get('Content-Encoding', 'identity'))
            print(
                r.url + "/" + str(data.decode())
            )
            f.write(r.url + "/" + str(data.decode()))
