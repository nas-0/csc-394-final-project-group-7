import requests
import praw
import prawcore

client_id='MpVe0s7TUeAjMj9UVJbO-g'
client_secret='owxGhaijKhQHeXnVkI77JbH1vhswSg'
redirect_uri = 'http://18.223.209.108/uploadvideofile/reddit_callback/'
access_token_url = 'https://www.reddit.com/api/v1/access_token'

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    user_agent="softwares testing/1.0.0 (by /u/ForsoftwareTesting)"  
)


auth_url = reddit.auth.url(
    scopes=['identity', 'read', 'submit'],  # Specify the scopes you need
    state='YOUR_STATE',  # Optional: Specify your own state value
    duration='permanent'  # Specify the desired duration: 'temporary' or 'permanent'
)

print(f'Please visit the following URL and grant permission to your application:\n{auth_url}')


authorization_code = input('Enter the authorization code: ')

try:
    
    access_token = reddit.auth.authorize(authorization_code)

    user = reddit.user.me()
    print(f'Authenticated as: {user.name}')

except praw.exceptions.PRAWException as e:
    print(f'Error occurred: {e}')

subreddit_name = 'testingapi32'  # Replace with the subreddit where you want to post the video
video_file_path = 'https://mutiplatformsvideosupload.net/video/TESTING2%20-%20Made%20with%20Clipchamp_3HB7EI1.mp4'  # Replace with the path to the video file

try:
    subreddit = reddit.subreddit(subreddit_name)
    submission = subreddit.submit(title='This is for testing purpose', url=video_file_path)
    print('Video posted successfully!')
except praw.exceptions.APIException as e:
    print(f'Error posting the video: {e}')
