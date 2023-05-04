import requests

# Replace CLIENT_ID, CLIENT_SECRET, REDDIT_USERNAME, and REDDIT_PASSWORD with your app's credentials and a valid Reddit account's credentials
CLIENT_ID = 'MZ9N_VToT15PkC38Ij7JsQ'
CLIENT_SECRET = 'evbH7PflRspt2_Uj_SyJxvNoTwaJhg'
REDDIT_USERNAME = 'ForsoftwareTesting'
REDDIT_PASSWORD = 'Password876'

# Set the headers and data for the POST request
headers = {'User-Agent': 'myBot/0.0.1'}
data = {
    'grant_type': 'password',
    'username': REDDIT_USERNAME,
    'password': REDDIT_PASSWORD
}

# Make the POST request to obtain an access token
response = requests.post(
    'https://www.reddit.com/api/v1/access_token',
    headers=headers,
    data=data,
    auth=(CLIENT_ID, CLIENT_SECRET)
)

# Get the access token from the response
access_token = response.json()['access_token']
print(f'Access token: {access_token}')
