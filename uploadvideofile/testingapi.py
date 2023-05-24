import requests
import praw
import prawcore

client_id='MpVe0s7TUeAjMj9UVJbO-g'
client_secret='owxGhaijKhQHeXnVkI77JbH1vhswSg'
redirect_uri = 'http://18.223.209.108/uploadvideofile/upload/'
access_token_url = 'https://www.reddit.com/api/v1/access_token'

# Replace with your actual client ID, client secret, and redirect URI


# Create a Reddit instance
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    user_agent="softwares testing/1.0.0 (by /u/ForsoftwareTesting)"  # Replace with your desired user agent
)

# Generate the authorization URL
auth_url = reddit.auth.url(
    scopes=['identity', 'read', 'submit'],  # Specify the scopes you need
    state='YOUR_STATE',  # Optional: Specify your own state value
    duration='permanent'  # Specify the desired duration: 'temporary' or 'permanent'
)

# Print the authorization URL and instruct the user to visit it
print(f'Please visit the following URL and grant permission to your application:\n{auth_url}')

# After the user grants permission, they will be redirected to the redirect URI
# The authorization code will be included as a query parameter in the URL

# Retrieve the authorization code from the user
authorization_code = input('Enter the authorization code: ')

try:
    # Exchange the authorization code for an access token
    access_token = reddit.auth.authorize(authorization_code)

    # Use the access token to make authenticated API requests
    # For example, retrieve the authenticated user's information
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
