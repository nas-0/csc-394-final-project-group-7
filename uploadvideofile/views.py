import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import requests
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# This variable specifies the Google OAuth 2.0 scopes that this application
# requests.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

def index(request):
    context = {}
    return render(request, 'index.html', context)

def get_access_token(authorization_code):
    """
    This function retrieves an access token from the Google API using the authorization code obtained
    during the OAuth 2.0 flow.
    """
    url = 'https://accounts.google.com/o/oauth2/v2/auth'
    token_endpoint = 'https://accounts.google.com/o/oauth2/v2/auth'
    token_data = {
        'code': authorization_code,
        'client_id': settings.GOOGLE_CLIENT_ID,
        'client_secret': settings.GOOGLE_CLIENT_SECRET,
        'redirect_uri': settings.GOOGLE_REDIRECT_URI,
        'grant_type': 'authorization_code'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(token_endpoint, data=token_data, headers=headers)
    print(response.content)
    print(response.text)

    response.raise_for_status()

    # Parse the response and extract the access token
    response_data = response.json()
    access_token = response_data.get('access_token')
    response.raise_for_status()

    if response.status_code == 200:
        access_token = response.json()['access_token']
        return access_token
    else:
        return None

def upload_to_youtube(title, description, tags, category, privacy_status, file_path, access_token):
    """
    This function uploads a video to YouTube using the YouTube API.
    """
    try:
        # Authorize the API request.
        youtube = googleapiclient.discovery.build('youtube', 'v3', credentials=access_token)

        # Define the video resource properties that are being set.
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': category,
            },
            'status': {
                'privacyStatus': privacy_status
            }
        }

        # Call the API's videos.insert method to create and upload the video.
        request = youtube.videos().insert(
            part='snippet,status',
            body=body,
            media_body=googleapiclient.http.MediaFileUpload(file_path)
        )
        response = request.execute()

        # Return the ID of the newly uploaded video.
        return response['id']

    except googleapiclient.errors.HttpError as error:
        print(f'An error occurred: {error}')
        return None


@csrf_exempt
def upload(request):
    context = {}
    

    if request.method == 'POST':
        # Get the uploaded video file
        uploaded_video_file = request.FILES['video']
        # Save the video file to the file system
        fs = FileSystemStorage()
        name = fs.save(uploaded_video_file.name, uploaded_video_file)
        video_path = fs.path(name)
        # Get the authorization code from the POST data
        authorization_code = request.POST.get('code')
        # Get an access token using the authorization code
        access_token = get_access_token(authorization_code)
        if access_token:
            # Upload the video to YouTube
            video_id = upload_to_youtube(
                request.POST.get('title'),
                request.POST.get('description'),
                request.POST.get('tags'),
                request.POST.get('category'),
                request.POST.get('privacy'),
                video_path,
                access_token
            )
            if video_id:
                context['message'] = 'Video uploaded successfully!'
                context['video_url'] = f'https://www.youtube.com/watch?v={video_id}'
            else:
                context['message'] = 'An error occurred while uploading the video.'
        else:
            context['message']='An error occurred while getting the access token.'
    return render(request, 'upload.html', context)
