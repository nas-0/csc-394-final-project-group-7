from django.conf import settings
import json
import requests
import re

import googleapiclient.discovery
import googleapiclient.errors



class Youtube:

    def __init__(self,*args,**kwargs):

        # this is where we get data from youtube api
        self.developer_key=settings.YOUTUBE_API_KEY
        self.api_service_name = settings.YOUTUBE_API_SERVICE_NAME
        self.api_version = settings.YOUTUBE_API_VERSION
        self.channel_id = settings.YOUTUBE_CHANNEL_ID

        self.youtube = googleapiclient.discovery.build(
            self.api_service_name, 
            self.api_version, 
            developerKey=self.developer_key)
    def get_date(self):
       #this where  we data from youtube api


        def schedule_api():
            pass

