import praw 

reddit = praw.Reddit(client_id='MZ9N_VToT15PkC38Ij7JsQ',
                     client_secret='evbH7PflRspt2_Uj_SyJxvNoTwaJhg',
                     username='ForsoftwareTesting',
                     password='Password876',
                     user_agent="sdasd/1.0.0 (by /u/ForsoftwareTesting)")
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
