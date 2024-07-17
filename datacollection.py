import requests
import re
import urllib.request
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
import urllib3
from urllib.parse import urljoin
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from datatagging import posting
from datatagging import tagging
from datatagging import tagging_code_snippet
import os.path

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

working_directory = '../knowledge_based/'
def pdf_content(url,content_type,query):
# In pdf_content function extract content from url and save it as .pdf 
# if url ends with .pdf extract the whole content and write itt as .pdf or else it will look for .pdf files in hyperlink and write it as .pdf.
# 1.url = url to download the pdf files.  
# 2.query: keyword to download the documents using search result
# 3.content_type:pdf and multi type.
    #folder location to save pdf files
    folder_location=working_directory+'pdf/'
    if(url.endswith('pdf')):
        try:
            r = requests.get(url,verify=False,allow_redirects=True,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko)Version/12.1.1 Safari/605.1.15'})
            filename = url.split('/')[-1] # this will take only -1 splitted part of the url
            file_name= folder_location+filename
#             print(file_name)
            with open(file_name,'wb') as output_file:
                output_file.write(r.content)
#             print("SD")
            posting(file_name)
            output = tagging(file_name,url,content_type,query)
            print('Download Completed!!!')
            return output
        except Exception as e:
            print("\nNo pdf found on the page ")
    else:
        try:
            #search for pdf in url and save it
            response = requests.get(url,verify=False,allow_redirects=True)
            soup= BeautifulSoup(response.text, "html.parser")
            n_pdfs = 0
            if(soup.select("a[href$='.pdf']")):
                for link in soup.select("a[href$='.pdf']"):
                    n_pdfs+= 1
                    filename = os.path.join(folder_location,link['href'].split('/')[-1])
#                     print(filename)
            #save pdf file
                    with open(filename, 'wb') as f:
                        f.write(requests.get(urljoin(str(url),link['href'])).content)
                    posting(filename)
                #tag the saved pdf file
                    output=tagging(filename,url,content_type,query)
                    return output
            else:
                print('\nNo pdfs found on the page')
        except Exception as e:
            print("NO") 

            
def text_content(url,i,content_type,query):
# In text_content function extract content from url and save it as .txt 
# 1.url = url to download the text or html files.  
# 2.query: keyword to download the documents using search result
# 3.content_type:text or multi
    i = i
    folder_location = working_directory+'Text/'
    try:
        # req = urllib.request.Request(url,data=None,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36' }) 
        # page = urllib.request.urlopen(req)
        # soup = BeautifulSoup(page,"html.parser")
        req = url
        headers={ 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36' }
# page = urllib.request.urlopen(req)
        source = requests.get(req,data=None, headers=headers).text
        soup = BeautifulSoup(source,"html.parser")
        #preprocess the text 
        txt = '\n'.join([x.text for x in soup.find_all('p')])
        txt = txt.replace('  ', ' ')
        txt = re.sub('\[\d+\]', '', txt)
        txt = re.sub('\d+. ', '', txt)
        txt = txt.replace("\n\n", "\n")
        print("txt")
        #filename to save text files
        filename_text = folder_location+query+'%d.txt'%i
        #save text file
        with open(filename_text,'w')as f:
            f.write(txt)
        posting(filename_text)
    #tag the saved text file
        output = tagging(filename_text,new_list,content_type,query)
        return output

    except Exception as e:
        print('\nNo text has been found')
        
        
def video_content(url,content_type,query):
# In video_content function,  extract youtube videos from url and save it as .mp4 file.
# if videos has transcript files then save it as .txt files. 
# 1.url = url to download the videos files.  
# 2.query: keyword to download the documents using search result
# 3.content_type:videos or multi
    #folder location for videos and transcript files
    folder_location_video = working_directory+'Videos/'
    Transcript = working_directory+'Videos/'
    file_name_start_pos = url.rfind("=") + 1
    file_name = url[file_name_start_pos:]
    try:
        #if the url have transcript download the video and extract transcript from it or print no video found
        if(YouTubeTranscriptApi.get_transcript(file_name)):
            srt= YouTubeTranscriptApi.get_transcript(file_name)
            try:
                yt_obj = YouTube(url)
                yt_obj_download = yt_obj.streams.get_highest_resolution()
                #download video with transcript
                video = yt_obj_download.download(folder_location_video)
            except Exception as e:
                  print("No videos found on the page")
            #print('All YouTube videos downloaded successfully.')
            name = video.split('/')[-1]
            video_name = os.path.splitext(name)[0]
            filename_youtube_text = Transcript+video_name+'.txt'
            print(filename_youtube_text)
            #save transcript
            with open(filename_youtube_text,'w')as f:
                for i in srt:
                    f.write('%s\n' %i['text'])
            posting(filename_youtube_text)
            #tag the saved transcipt
            output = tagging(filename_youtube_text,url,content_type,query)
            # print(output)
            return output
    except Exception as e:
        print("\nNo YouTube videos found on the page")


def code_snippet(url,i,content_type,query):
# In code_snippet function, search for specifc html elements to extract code from url and save it as .txt 
# 1.url = url to download the program files.  
# 2.query: keyword to download the documents using search result
# 3.content_type:program or multi
    folder_location = working_directory+'codes/'
#     for i in range(len(new_list)):
    i=i
    try:
        req = url
        headers={ 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36' }
# page = urllib.request.urlopen(req)
        source = requests.get(req,data=None, headers=headers).text
        soup = BeautifulSoup(source,"html.parser")
        print(soup)
        # req = urllib.request.Request(url,data=None,headers={ 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko)Version/12.1.1 Safari/605.1.15' }) 
        # page = urllib.request.urlopen(req)
        # soup = BeautifulSoup(source,"html.parser")
        if(soup.find_all('code')):
            txt = '\n'.join([x.text for x in soup.find_all('code')])
        elif(soup.find_all('div',class_='codeblock')):
            txt= '\n'.join([x.text for x in soup.find_all('div',class_='codeblock')])
        elif(soup.find_all('pre')):
            txt = '\n'.join([x.text for x in soup.find_all('pre')])
        else:
            txt = '\n'.join([x.text for x in soup.find_all('div',class_='geshifilter')])
            txt = txt.rstrip()
        file = folder_location+t[i]+'.txt'
        with open(file,'w')as f:
            f.write(txt)
            f.close()
        str_directory = folder_location
        # get list of all files in the directory and remove possible hidden files
        list_files = [x for x in os.listdir(str_directory) if x[0]!='.']

        # now loop through the files and remove empty ones
        for each_file in list_files:
            file_path = '%s/%s' % (str_directory, each_file)
            # check size and delete if 0
            if os.path.getsize(file_path)==0:
                os.remove(file_path)
            else:
                pass
        output = tagging_code_snippet(file,url,content_type,query)
        return output
    except Exception as e:
        print("No code")
            
def code_snippet1(new_list,i,content_type,query):
# In code_snippet function, search for specifc html elements to extract code from url and save it as .txt 
# 1.new_list = url to download the program files.  
# 2.query: keyword to download the documents using search result
# 3.content_type:program or multi
#     for i in range(len(new_list)):
    i=i
    try:
        req = urllib.request.Request(new_list,data=None,headers={ 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko)Version/12.1.1 Safari/605.1.15'}) 
        page = urllib.request.urlopen(req)
        soup = BeautifulSoup(page,"html.parser")
        if(soup.find_all('code')):
            txt = '\n'.join([x.text for x in soup.find_all('code')])
        elif(soup.find_all('div',class_='codeblock')):
            txt= '\n'.join([x.text for x in soup.find_all('div',class_='codeblock')])
        elif(soup.find_all('pre')):
            txt = '\n'.join([x.text for x in soup.find_all('pre')])
        else:
            txt = '\n'.join([x.text for x in soup.find_all('div',class_='geshifilter')])
            txt = txt.rstrip() 
        filename = working_directory+'Code/'+t3[i]+'.txt' 
        with open(filename,'w')as f:
            f.write(txt)
            f.close()
        str_directory = working_directory+'Code'
        # get list of all files in the directory and remove possible hidden files
        list_files = [x for x in os.listdir(str_directory) if x[0]!='.']

        # now loop through the files and remove empty ones
        for each_file in list_files:
            file_path = '%s/%s' % (str_directory, each_file)
            # check size and delete if 0
            if os.path.getsize(file_path)==0:
                os.remove(file_path)
            else:
                pass
        output = tagging_code_snippet(filename,new_list,content_type,query)
        return output
    except Exception as e:
        print("No code")
        
