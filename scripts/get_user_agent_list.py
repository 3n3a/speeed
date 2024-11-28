import requests

url = 'https://raw.githubusercontent.com/microlinkhq/top-user-agents/refs/heads/master/src/desktop.json'
r = requests.get(url, allow_redirects=True)
open('user_agents.json', 'wb').write(r.content)