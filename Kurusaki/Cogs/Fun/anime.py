import discord,asyncio
import time,datetime
from discord.ext import commands
from discord.ext.commands import Cog,command
import requests as rq
import bs4, json
from bs4 import BeautifulSoup as soup
from AnimeError import NoUserLogin




class AnimeRequestError(object):
    def __init__(self,data):
        self.data=data

    def __repr__(self):
        return str(self.data.status_code)


    @property
    def _json(self):
        return self.data.json()



    @property
    def request_data(self):
        return self.data



class AnimeLogin(object):
    def __init__(self,data):
        self.data=data
        self.parser='html.parser'

    def __repr__(self):
        page=soup(self.data.text,self.parser)
        username=page.find('a',attrs={'class':'header-profile-link'})

        return f"Logged in as {username.text}"

    def login_data(self):
        return self.data


class AnimeAPI(object):
    def __init__(self):
        self.base="https://myanimelist.net"
        self.parser='html.parser'
        self.user_session=None
        self.token=None
        self.headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
        self.session=rq.Session()
        self.cookies=None
        self.username=None


    async def kitsu_search(self,anime):
        base="https://kitsu.io/api/edge"
        url=f"{base}/anime?filter[text]={anime}"
        data=rq.get(url,headers=self.headers)
        if data.ok:
            return data.json()

        return AnimeRequestError(data)



    def all_search(self,_search):
        url=f"{self.base}/search/all?q={_search}"
        request_data=self.session.get(url,headers=self.headers)
        page=soup(request_data,self.parser)
        request_results=page.find_all(name='article')
        all_results={
            "anime":{},
            "managa":{},
            "characters":{},
            "people":{}
        }
        _anime={
            "anime":request_results[0]
        }
        
        _managa={   
            "managa":request_results[1],
        }
        _characters={
             "characters":request_results[2],
        }
        _people={
            "people":request_results[3]
        }

        for key, value in _anime.items():
            container='list di-t w100'
            images='hoverinfo_trigger fw-b'
            animes=value.find_all('div',attrs={'class':container})
            for anime in animes:
                name=anime.find('a',attrs={'class':'hoverinfo_trigger fw-b fl-l'})
                thumbnail=anime.find('img',attrs={'alt':name.text})
                all_results[key][name.text]={
                    'thumbnail':thumbnail['data-src'],
                    'link':name['href']
                    }
    

        for key, value in _managa.items():
            mangas=value.find_all('div',attrs={'class':container})
            for manga in mangas:
                name=manga.find('a',attrs={'class':images})
                thumbnail=manga.find('img',attrs={'alt':name.text})
                all_results[key][name.text]={
                    'thumbnail':thumbnail['data-src'],
                    'link':name['href']
                }


        for key, value in _characters.items():
            characters=value.find_all('div',attrs={'class':container})
            for character in characters:
                name=character.find('a',attrs={'class':images})
                thumbnail=character.find('img',attrs={'alt':name.text})
                all_results[key][name.text]={
                    'thumbnail':thumbnail['data-src'],
                    'link':name['href']
                }

        for key, value in _people.items():
            peoples=value.find_all('div',attrs={'class':container})
            for people in peoples:
                name=people.find('a',attrs={'class':images})
                thumbnail=people.find('img',attrs={'alt':name.text})
                all_results[key][name.text]={
                    'thumbnail':thumbnail['data-src'],
                    'link':name['href']
                }


        return all_results



    def write_data(self,data):
        with open('web_data.html','w',encoding='utf-8')as html:
            html.write(data.text)

    def write_text(self,data):
        with open("test.txt",'w',encoding='utf-8')as f:
            f.write(str(data))

    def check_login(self,data):
        page=soup(data.text,self.parser)
        try:
            name=page.find('a',attrs={'class':'header-profile-link'})
            self.username=name.text
            return True
        except Exception as Error:
            print(Error)

        


    def login(self,username,password):
        if self.user_session is not None:
            return "Please signout before logging in"

        _login="/login.php?from=%2F"
        url=f"{self.base}{_login}"
        session=rq.Session()
        __data=session.get(url,headers=self.headers)
        page=soup(__data.text,self.parser)
        token=page.find('meta',attrs={'name':'csrf_token'})
        self.token=token['content']
        payload={
        'user_name': username,
        'password': password,
        'cookie': '1',
        'sublogin': 'Login',
        'submit': '1',
        'csrf_token': token['content']
        }
        login_data=session.post(url,data=payload,headers=self.headers)
        if self.check_login(login_data): #login success: True
            self.user_session=session
            self.username=username.title()
            return AnimeLogin(login_data)


        return AnimeRequestError(login_data)


    def who(self):
        if self.username is not None:
            return self.username
        
        raise NoUserLogin


    def logout(self):
        if self.user_session is None:
            return "No account logged in"
        
        url=f"{self.base}/logout.php"
        payload={'csrf_token':self.token}
        self.user_session.post(url,data=payload,headers=self.headers)
        self.user_session.close()
        self.username=None
        self.user_session=None
        self.token=None
        return "Logged out"



    def anime_search(self,anime):
        url=f"{self.base}/anime.php?q=anime"
        request_data=self.session.get(url,headers=self.headers)



    def anime_list(self):
        url=self.base+f'/animelist/{self.who()}'
        list_request=self.user_session.get(url,headers=self.headers)
        anime_list=soup(list_request.text,self.parser)
        anime_list=anime_list.find('table',attrs={'class':'list-table'})['data-items']
        anime_list=anime_list.replace('&quot;','"')
        json_data=json.loads(anime_list)
        return json_data
        


