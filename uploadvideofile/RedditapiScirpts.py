import praw 

reddit = praw.Reddit(client_id='MpVe0s7TUeAjMj9UVJbO-g',
                     client_secret='owxGhaijKhQHeXnVkI77JbH1vhswSg',
                     username='Software721',
                     password='Herrera876',
                     user_agent="softwares testing/1.0.0 (by /u/ForsoftwareTesting)")

            # create a Reddit instance by providing the required credentials


            # define the subreddit where you want to upload the video
subreddit_name = 'testingapi32'
subreddit = reddit.subreddit(subreddit_name)

            # define the video link and the title of the post
video_link = 'https://mutiplatformsvideosupload.net/video/TESTING2%20-%20Made%20with%20Clipchamp_3HB7EI1.mp4'
title = 'Testing/may 8,2023'

            # create the submission object
submission = subreddit.submit(title=title, url=video_link)

            # print the link to the newly created post
print(submission.url)



subreddit_name = 'testingapi32'  # Replace with the subreddit where you want to post the video
video_file_path = 'https://mutiplatformsvideosupload.net/video/TESTING2%20-%20Made%20with%20Clipchamp_3HB7EI1.mp4'  # Replace with the path to the video file

try:
    subreddit = reddit.subreddit(subreddit_name)
    submission = subreddit.submit(title='This is for testing purpose', url=video_file_path)
    print('Video posted successfully!')
except praw.exceptions.APIException as e:
    print(f'Error posting the video: {e}')

