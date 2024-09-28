import requests

# Define the base URL for the authorization dialog
url = 'https://api.upstox.com/v2/login/authorization/dialog'

# Define the query parameters
params = {
    'response_type': 'code',
    'client_id': '5fc24406-3944-4703-a90d-36e36a2323d0',       # Replace with your API key
    'redirect_uri': 'https://127.0.0.1', # Replace with your redirect URI
}

# Send the GET request with the query parameters
response = requests.get(url, params=params)

# Print the status code of the response
print(response.status_code)

# Print the response text (or use response.json() if the response is in JSON format)
print(response.text)

import requests

url = 'https://api.upstox.com/v2/login/authorization/token'
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded'
}
data = {
    'code': 'BqruT0',
    'client_id': '5fc24406-3944-4703-a90d-36e36a2323d0',
    'client_secret': 'gg1v867h2m',
    'redirect_uri': 'https://127.0.0.1',
    'grant_type': 'authorization_code'
}

response = requests.post(url, headers=headers, data=data)

# Print the response status code and JSON content
print('Status Code:', response.status_code)
print('Response JSON:', response.json())



