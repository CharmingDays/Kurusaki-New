import discord,asyncio
import time,datetime
from discord.ext import commands
from discord.ext.commands import Cog,command
import requests as rq
import bs4, json
from bs4 import BeautifulSoup as soup





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

    def __repr__(self):
        page=soup(self.data.text,'html.parser')
        username=page.find('a',attrs={'class':'header-profile-link'})

        return f"Logged in as {username.text}"

    def login_data(self):
        return self.data


class AnimeAPI(object):
    def __init__(self):
        self.base="https://myanimelist.net"
        self.user_session=None
        self.token=None
        self.headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
        self.session=rq.Session()
        self.username=None

    async def KitsuSearch(self,anime):
        headers={"Accept":"application/vnd.api+json","Content-Type":"application/vnd.api+json"}
        base="https://kitsu.io/api/edge"
        url=f"{base}/anime?filter[text]={anime}"
        data=rq.get(url,headers=self.headers)
        if data.ok:
            return data.json()

        return AnimeRequestError(data)


    def write_data(self,data):
        with open('web_data.html','w',encoding='utf-8')as html:
            html.write(data.text)

    def write_text(self,data):
        with open("test.txt",'w',encoding='utf-8')as f:
            f.write(str(data))

    def check_login(self,data):
        page=soup(data.text,'html.parser')
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
        page=soup(__data.text,'html.parser')
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
        if self.check_login(login_data):
            self.user_session=session
            return AnimeLogin(login_data)
            self.username=username.title()

        return AnimeRequestError(login_data)


    def who(self):
        return self.username,self.token


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


    def all_search(self,_search):
        url=f"{self.base}/search/all?q={_search}"
        request_data=self.session.get(url,headers=self.headers)
        page=soup(request_data,'html.parser')
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
            animes=value.find_all('div',attrs={'class':'list di-t w100'})
            for anime in animes:
                name=anime.find('a',attrs={'class':'hoverinfo_trigger fw-b fl-l'})
                thumbnail=anime.find('img',attrs={'alt':name.text})
                all_results[key][name.text]={
                    'thumbnail':thumbnail['data-src'],
                    'link':name['href']
                    }
    

        for key, value in _managa.items():
            mangas=value.find_all('div',attrs={'class':'list di-t w100'})
            for manga in mangas:
                name=manga.find('a',attrs={'class':'hoverinfo_trigger fw-b'})
                thumbnail=manga.find('img',attrs={'alt':name.text})
                all_results[key][name.text]={
                    'thumbnail':thumbnail['data-src'],
                    'link':name['href']
                }


        for key, value in _characters.items():
            characters=value.find_all('div',attrs={'class':'list di-t w100'})
            for character in characters:
                name=manga.find('a',attrs={'class':'hoverinfo_trigger fw-b'})
                thumbnail=manga.find('img',attrs={'alt':name.text})
                all_results[key][name.text]={
                    'thumbnail':thumbnail['data-src'],
                    'link':name['href']
                }

        for key, value in _people.items():
            peoples=value.find_all('div',attrs={'class':'list di-t w100'})
            for people in peoples:
                name=people.find('a',attrs={'class':'hoverinfo_trigger fw-b'})
                thumbnail=people.find('img',attrs={'alt':name.text})
                all_results[key][name.text]={
                    'thumbnail':thumbnail['data-src'],
                    'link':name['href']
                }


        return all_results




    def anime_search(self,anime):
        url=f"{self.base}/anime.php?q=anime"
        request_data=self.session.get(url,headers=self.headers)




api=AnimeAPI()
