import requests
import json
from bs4 import BeautifulSoup
import re
import urllib.request
import os
from urllib.parse import urljoin
#import pandas as pd
import urllib3
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from googlesearch import search
import random
from datacollection import pdf_content 
from datatagging import tagging 
from datacollection import text_content
from datatagging import score
from datacollection import video_content
from datacollection import code_snippet1
from datacollection import code_snippet

# query = input('Enter Your Query: ') #search query
# lang = input('Enter language ex:[en,fr,ar,jp,cn...]: ') #search language
# content_type = input('Enter your Format:[multi,pdf,videos,program or code,text,images...]: ')

def content_type_multi(query,lang,content_type):

# In content_type_multi collect url for pdf,code,videos
#  1.query: keyword to download the documents using search result
#  2.Lang: language name
#  3.content_type:type of format like pdf, program, videos,images etc..
    output=[]
    my_dict1=[]
    dict_temp1={}
    my_dict2=[]
    dict_temp2={}
    my_dict3=[]
    dict_temp3={}
    content_type1 = "pdf"
    url1 = 'https://www.google.com/search?hl={}&q={}&q={}&num=10&ie=UTF-8'.format(lang,query,content_type1)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko)Version/12.1.1 Safari/605.1.15'}#headers
    source1=requests.get(url1, headers=headers).text # url source
    soup1 = BeautifulSoup(source1, 'html.parser')
    search_div1 = soup1.find_all(class_='yuRUbf') # find all divs tha contains search result


    for result1 in search_div1: # loop result list
        print('Title: %s'%result1.h3.string) #geting h3
        print('Url: %s'%result1.a.get('href')) #geting a.href
        text = result1.get_text()
        print(result1.text)
        print('\n')
        dict_temp1['Title']=result1.h3.string
        dict_temp1['Url']=result1.a.get('href')
        my_dict1.append(dict_temp1)
        dict_temp1={}

    content_type2 = "videos"
    url2 = 'https://www.google.com/search?hl={}&q={}&q={}&num=10&ie=UTF-8'.format(lang,query,content_type2)#url
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko)Version/12.1.1 Safari/605.1.15'}#headers
    source2=requests.get(url2, headers=headers).text # url source
    soup2 = BeautifulSoup(source2, 'html.parser')
    search_div2 = soup2.find_all(class_='yuRUbf') # find all divs tha contains search result


    for result2 in search_div2: # loop result list
        print('Title: %s'%result2.h3.string) #geting h3
        print('Url: %s'%result2.a.get('href')) #geting a.href
        text = result2.get_text()
        print(result2.text)
        print('\n')
        dict_temp2['Title']=result2.h3.string
        dict_temp2['Url']=result2.a.get('href')
        my_dict2.append(dict_temp2)
        dict_temp2={}

    content_type3 = "program"
    url3 = 'https://www.google.com/search?hl={}&q={}&q={}&num=10&ie=UTF-8'.format(lang,query,content_type3)#url
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko)Version/12.1.1 Safari/605.1.15'}#headers
    source3=requests.get(url3, headers=headers).text # url source
    soup3 = BeautifulSoup(source3, 'html.parser')
    search_div3 = soup3.find_all(class_='yuRUbf') # find all divs tha contains search result


    for result3 in search_div3: # loop result list
        print('Title: %s'%result3.h3.string) #geting h3
        print('Url: %s'%result3.a.get('href')) #geting a.href
        text = result3.get_text()
        print(result3.text)
        print('\n')
        dict_temp3['Title']=result3.h3.string
        dict_temp3['Url']=result3.a.get('href')
        my_dict3.append(dict_temp3)
        dict_temp3={}
    url1 = []
    for i in range(len(my_dict1)):
        url1.append(my_dict1[i]['Url'])
    url2 = []
    for i in range(len(my_dict2)):
        url2.append(my_dict2[i]['Url'])
    url3 = []
    for i in range(len(my_dict3)):
        url3.append(my_dict3[i]['Url'])
    t1=[]
    for i in range(len(my_dict1)):
        t1.append(my_dict1[i]['Title'])
    t2=[]
    for i in range(len(my_dict2)):
        t2.append(my_dict2[i]['Title'])
    t3=[]
    for i in range(len(my_dict3)):
        t3.append(my_dict3[i]['Title'])

    for i in range(len(url1)):
        output1=pdf_content(url1[i], content_type,query)
    for i in range(len(url2)):
        output2=video_content(url2[i], content_type,query)
    for i in range(len(url3)):
        output3=code_snippet1(url3[i], i, content_type,query)
    output= output.append((output1,output2,output3))
    return output

def content_type_individual(query,lang,content_type):

# In content_type_individual collect url for pdf,code,videos,text
#  1.query: keyword to download the documents using search result
#  2.Lang: language name
#  3.content_type:type of format like pdf, program, videos,images etc..
    output=[]
    my_dict=[]
    dict_temp={}
	# requests
    url = 'https://www.google.com/search?hl={}&q={}&q={}&num=20&ie=UTF-8'.format(lang,query,content_type)#url
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko)Version/12.1.1 Safari/605.1.15'}#headers
    source=	requests.get(url, headers=headers).text # url source

    # BeautifulSoup
    soup = BeautifulSoup(source, 'html.parser')
    search_div = soup.find_all(class_='yuRUbf') # find all divs tha contains search result

    for result in search_div: # loop result list
        print('Title: %s'%result.h3.string) #geting h3
        print('Url: %s'%result.a.get('href')) #geting a.href
        text = result.get_text()
        print(result.text)
        print('\n')
    #     dict_temp={'Title':result.h3.string, 'Url':result.a.get('href')}
    #     my_dict.update(dict_temp)
    #     with open('sample.json', 'w') as fp:
    #         json.dump(my_dict, fp,sort_keys=True, indent=4)
        dict_temp['Title']=result.h3.string
        dict_temp['Url']=result.a.get('href')
        my_dict.append(dict_temp)
        dict_temp={}

    url=[]
    for i in range(len(my_dict)):
        url.append(my_dict[i]['Url'])
    t=[]
    for i in range(len(my_dict)):
        t.append(my_dict[i]['Title'])

    for i in range(len(url)):
        if (content_type == "pdf"):
            output.append(pdf_content(url[i], content_type,query))
        elif (content_type == "videos"):
            output.append(video_content(url[i], content_type,query))
        elif (content_type == "program"):
            output.append(code_snippet(url[i], i, content_type,query))
        else:
            output.append(text_content(url[i], i, content_type,query))
    
    return output

def url_collection(query, lang, content_type):
    working_directory = '../knowledge_based/'

    if content_type == "multi":
        output=content_type_multi(query,lang,content_type)

    else:
        output = content_type_individual(query,lang,content_type)
    if (content_type != "program"):
        score(query)
    
    return output

# def url_process():
#     working_directory = '../knowledge-base/'
#     if(content_type=="multi"):
#         for i in range(len(url1)):
#             pdf_content(url1[i],content_type)
#         for i in range(len(url2)):
#             video_content(url2[i],content_type)
#         for i in range(len(url3)):
#             code_snippet1(url3[i],i,content_type)
#     else:
#         for i in range(len(url)):
#             if(content_type=="pdf"):
#                 pdf_content(url[i],content_type)
#             elif(content_type=="videos"):
#                 video_content(url[i],content_type)
#             elif(content_type=="program"):
#                 code_snippet(url[i],i,content_type)
#             else:
#                 text_content(url[i],i,content_type)
#     if(content_type!="program"):
#         score(query)

