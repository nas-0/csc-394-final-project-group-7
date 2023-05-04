import requests
import json

# Reddit API endpoint for submitting a post
api_endpoint = 'https://oauth.reddit.com/api/submit'

# User access token
access_token = 'your_access_token_here'

# Video post parameters
subreddit = 'videos'
title = 'My Awesome Video'
video_url = 'https://www.example.com/my_video.mp4'

# Headers for API request
headers = {
    'User-Agent': 'My App/1.0.0',
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

# Body of API request
payload = {
    'sr': subreddit,
    'title': title,
    'url': video_url,
    'kind': 'link'
}

# Send the API request to post the video
response = requests.post(api_endpoint, headers=headers, data=json.dumps(payload))

# Check the response status code
if response.status_code == 200:
    print('Video posted successfully!')
else:
    print(f'Error posting video: {response.status_code} {response.reason}')
