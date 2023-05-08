import requests
def post_to_facebook(title, desc, group_access_token, file_path,):
    # Set up the API endpoint and parameters
    url = "https://graph-video.facebook.com/v16.0/me/videos"
    access_token = group_access_token

    import os

    # Get the file size of the video in bytes
    print(f"{type(file_path)}, {file_path}")
    file_size = os.path.getsize(file_path)

    # Set up the data to be posted
    data = {
        "upload_phase": "start",
        "access_token": access_token,
        "file_size": file_size,
    }

    # Make the initial request to start the upload
    response = requests.post(url, data=data)
    response_json = response.json()
    print("herre")
    # Check for any errors in the response
    if "error" in response_json:
        print(response_json["error"]["message"])
        exit()

    # Get the video ID and upload session ID from the response
    video_id = response_json["video_id"]
    upload_session_id = response_json["upload_session_id"]

    # Set up the data for the next request
    data = {
        "upload_phase": "transfer",
        "access_token": access_token,
        "start_offset": 0,
        "upload_session_id": upload_session_id,
    }

    # Set up the files for the video upload
    files = {
        "video_file_chunk": ("test2.mp4", open(file_path, "rb")),
    }

    # Make the request to upload the video chunks
    response = requests.post(url, data=data, files=files)
    response_json = response.json()
    print("ohere")
    # Check for any errors in the response
    if "error" in response_json:
        print(response_json["error"]["message"])
        exit()

    # Set up the data for the final request
    data = {
        "upload_phase": "finish",
        "access_token": access_token,
        "upload_session_id": upload_session_id,
        "title": title,
        "description": desc,
    }

    # Make the request to finish the video upload
    response = requests.post(url, data=data)
    response_json = response.json()
    print("here")
    # Check for any errors in the response
    if "error" in response_json:
        print(response_json["error"]["message"])
        exit()

    # Print the video ID of the uploaded video
    print("Video uploaded with ID:", video_id)