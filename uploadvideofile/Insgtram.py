import requests

# Set up the access token and user ID
access_token = 'YOUR_ACCESS_TOKEN'
user_id = 'USER_ID'

# Set up the API endpoint and payload
url = f'https://graph.facebook.com/v13.0/{user_id}/videos'
payload = {'access_token': access_token}
files = {'file': open('YOUR_FILE_PATH', 'rb')}

# Make the API call to upload the file
response = requests.post(url, data=payload, files=files)

# Parse the response to get the video ID
video_id = response.json()['id']

# Use the video ID to publish the video to the user's feed (optional)
feed_url = f'https://graph.facebook.com/v13.0/{user_id}/feed'
feed_payload = {'access_token': access_token, 'attached_media[0]': f'{{"media_fbid":"{video_id}"}}'}
requests.post(feed_url, data=feed_payload)

