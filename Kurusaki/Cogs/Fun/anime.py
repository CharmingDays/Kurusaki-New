import discord,asyncio
import time,datetime
from discord.ext import commands
from discord.ext.commands import Cog,command
import requests as rq, json
from bs4 import BeautifulSoup as soup


class RequestObject(object):
    def __init__(self,rq_data):
        self.data=rq_data
        self.code=rq_data.status_code
    

    def __repr__(self):
        if self.code.ok is True:
            return "OK"

        return str(self.code)


    


    def json(self):
        try:
            attempt_json=self.data.json()
        except Exception:
            raise AttributeError("Unable to get JSON data")

        if self.code.ok and not hasattr(self,'json'):
            setattr(self,'json',attempt_json)

        return {'status_code':self.code,'json':self.data.json()}






class AniList(object):
    def __init__(self):
        self.data=1

    
    def search_anime(self,name):
        query = r'''
        query ($search: String,$type: MediaType) { # Define which variables will be used in the query (id)
        Media (search: $search, type: $type) { # Insert our variables into the query arguments (id) (type: ANIME is hard-coded in the query)
            id
            title {
            romaji
            english
            native
            }
        }
        }
        '''
        variables = {
            'search': 'Naruto'
        }

        url = 'https://graphql.anilist.co'

        response = rq.post(url, json={'query': query, 'variables': variables})
        return RequestObject(response)

