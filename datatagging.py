from tika import parser
import os.path
import json
import requests

working_directory = '../knowledge_based/'

def tagging(file,link,content_type,query):
    new_list=[]

# In tagging function, tag downloded files using curl command in solr.
# 1.file = name of the downloaded files   
# 2.query: keyword to download the documents using search result
# 3.content_type:pdf,text,videos or multi
# 4.link= keyword to download the documents using search result
    
    folder_location = working_directory+'Tags/tag_details.json'
    #Solr query for tagging
    url = 'http://52.53.165.238:8983/solr/tagssub/tag?fl=id,tag_name,subtags.tag_name&wt=json&indent=true'
    #content type must be text 
    headers = {"Content_type" : "text/plain"}
    #parse content from file using Tika
    file_data = parser.from_file(file)
    text = file_data['content']
    #post the parsed content into Solr for tagging
    posting = requests.post(url, data=text.encode('utf-8'), headers=headers)
    response_json = posting.json()
#     print(response_json)
    #responsed we got from solr
    total_tag_count = response_json['tagsCount']
    individual_tag = response_json['response']['numFound']
    tags = response_json['response']['docs'][0:individual_tag] 
    tags_individual = response_json['response']['docs']
#     print(response_json)
    if total_tag_count == 0:
        os.remove(file)
    else:
        print("\nTotal Number of Tags: ", total_tag_count)
        print("\nIndividual Tag Count: ", individual_tag)
        for i in range(individual_tag):
            main_tag = tags_individual[i]['tag_name']
            print("\nMain Tag :",main_tag)
            sub_tag = tags_individual[i]['subtags.tag_name']
            print("Sub Tag :",sub_tag)
            tag_id = tags_individual[i]['id']
            print("Tag ID :",tag_id)
        file_name = file.split('/')[-1]
        title_name = os.path.splitext(file_name)[0]
        y = {
            'url' : link,
            'query': query,
            'content_type' : content_type,
            'title' : title_name,
            'tag_details' : {
                'no of tags' : total_tag_count,
                'tags' : tags,
                'individual_tags' : individual_tag,
                }
            }  
        new_list.append(y)
        print(new_list)
        

        #save the response into Json file
        #if file already exsists save it or create a file then save it
        # if path.exists(folder_location) == True:
        #     with open(folder_location) as outfile:
        #         data = json.loads(outfile.read())
        #         temp = data['content_tagging']
        #         y = {
        #             'url' : link,
        #             'query': query,
        #             'content_type' : content_type,
        #             'title' : title_name,
        #             'tag_details' : {
        #                 'no of tags' : total_tag_count,
        #                 'tags' : tags,
        #                 'individual_tags' : individual_tag,
        #                 }
        #             }
        #         print(y)
        #         temp.append(y)
        #         output.append(y)

        #     with open(folder_location,'w') as f:
        #         json.dump(data,f,indent=4)
        # else:
        #     data = {}
        #     data['content_tagging'] = [
        #         {
        #         'url' : link,
        #         'query': query,
        #         'content_type' : content_type,
        #         'title' : title_name,
        #         'tag_details' : {
        #             'no of tags' : total_tag_count,
        #             'tags' : tags,
        #             'individual_tags' : individual_tag,
        #         }
        #     }
        #     ]
        #     with open(folder_location, 'w') as outfile:
        #         json.dump(data, outfile)
        
    return new_list
                
def tagging_code_snippet(filename,link,content_type,query):
# In tagging_code_snippet function, tag downloded files using curl command in solr.
# 1.filename = title of the downloaded code snippet files   
# 2.query: keyword to download the documents using search result
# 3.content_type:pdf,text,videos or multi
# 4.link= keyword to download the documents using search result

    new_list=[]
    folder_location = working_directory+'Tags/tag_details.json'
    #Solr query for tagging
    url = 'http://52.53.165.238:8983/solr/codesnippet/tag?fl=id,tagname&wt=json&indent=true'
    #content type must be text 
    headers = {"Content_type" : "text/plain"}
    tagging_filename = filename.split('/')[-1]
    posting = requests.post(url,data=tagging_filename,headers=headers)
    response_json = posting.json()
    #responsed we got from solr
    total_tag_count = response_json['tagsCount']
    individual_tag = response_json['response']['numFound']
    tags = response_json['response']['docs'][0:individual_tag] 
    if total_tag_count == 0:
        os.remove(filename)
    else:
        print("\nTotal Number of Tags: ", total_tag_count)
        print("\nIndividual Tag Count: ", individual_tag)
        print("\nTags :", tags)
        #save the response into Json file
        #if file already exsists save it or create a file then save it
        y = {
                'url' : link,
                'query': query,
                'content_type' : content_type,
                'title' : title_name,
                'tag_details' : {
                    'no of tags' : total_tag_count,
                    'tags' : tags,
                    'individual_tags' : individual_tag,
                        }
                    }
        new_list.append(y)
        # if path.exists(folder_location) == True:
        #     with open(folder_location) as outfile:
        #         data = json.load(outfile)
        #         temp = data['content_tagging']
        #         y = {
        #             'url' : link,
        #             'query': query,
        #             'content_type' : content_type,
        #             'title' : tagging_filename,
        #             'tag_details' : {
        #                 'no of tags' : total_tag_count,
        #                 'tags' : tags,
        #                 'individual_tags' : individual_tag,
        #                 }
        #             }
        #         temp.append(y)
        #         output.append(y)

        #     with open(folder_location,'w') as f:
        #         json.dump(data,f,indent=4)
        # else:
        #     data = {}
        #     data['content_tagging'] = [
        #         {
        #         'url' : link,
        #         'query': query,
        #         'content_type' : content_type,
        #         'title' : tagging_filename,
        #         'tag_details' : {
        #             'no of tags' : total_tag_count,
        #             'tags' : tags,
        #             'individual_tags' : individual_tag,
        #         }
        #     }
        #     ]
        #     with open(folder_location, 'w') as outfile:
        #         json.dump(data, outfile)
    print(new_list)
    return new_list


def posting(filename):

# In posting function post the documents to solr using curl command
# 1. filename= name of the downloaded files 
    
    file_name = filename.split('/')[-1]
    file_data = parser.from_file(filename)
    text = file_data['content']
    data = [
        {
            'id' : file_name,
            'content' : text
        }
        ]
        
    dataset = json.dumps(data)
    url = 'http://52.53.165.238:8983/solr/documents/update?commit=true'
    headers={'Content-Type': 'text/json'}
    response = requests.post(url,data=dataset.encode('utf-8'),headers=headers) 


def score(query):

# In score function,with query as a keyword get the score of each document using curl command and display top 10.
# 1.query= keyword to download the documents using search result
    
    doc_name = []
    number = 10
    url = 'http://52.53.165.238:8983/solr/documents/select?q=content:'+query+'&start=0&rows='+str(number)+'&fl=id,score&wt=json&indent=true'
    response = requests.get(url)
    response_json = response.json()
    response_id = response_json['response']['docs']
    if len(response_id) < number:
        for i in range(len(response_id)):
            doc_id = response_id[i]['id']
            print("\nDocument Name :",doc_id)
            doc_name.append(doc_id)
            doc_score = response_id[i]['score']
            print("\nScore :",doc_score)
    else:
        for i in range(number):
            doc_id = response_id[i]['id']
            print("\nDocument Name :",doc_id)
            doc_name.append(doc_id)
            doc_score = response_id[i]['score']
            print("\nScore :",doc_score)
#     if filename not in doc_name:
#         os.remove(filename)
  
