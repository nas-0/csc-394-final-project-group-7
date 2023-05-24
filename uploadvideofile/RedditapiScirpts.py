import praw 

reddit = praw.Reddit(client_id='VhmckEe4MW5dA-b5p2IriQ',
                     client_secret='AXqknNGBxgmvZ9e7VnvyQzitz8NIgg',
                     username='softwaretesting7',
                     password='Software7',
                     user_agent="softwares testing/1.0.0 (by /u/ForsoftwareTesting)")

            # create a Reddit instance by providing the required credentials


            # define the subreddit where you want to upload the video
subreddit_name = 'test34243242'
subreddit = reddit.subreddit(subreddit_name)

            # define the video link and the title of the post
video_link = 'https://mutiplatformsvideosupload.net/video/TESTING2%20-%20Made%20with%20Clipchamp_3HB7EI1.mp4'
title = 'Testing/may 8,2023'

            # create the submission object
submission = subreddit.submit(title=title, url=video_link)

            # print the link to the newly created post
print(submission.url)
