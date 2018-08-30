from multiprocessing import Process,Lock
import json
import requests
  
## Downloading all the projects
repo_result1 = []
repo_result2 = []

def func1():
  i = 0
  count = 0
  global repo_result1  
  api_url = 'https://api.github.com/'
  api_token = 'XX'


  while i < 500000: # This number will be increased to collect all the projects

    repo_url = api_url + 'repositories?since=' + str(i)
    #print(repo_url)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(api_token)}
    repo_response = requests.get(repo_url, headers=headers).json()
    count = count + 1


    print(count)
    project_list = []

    try:

      for j in range(0,len(repo_response)):
        project_id = repo_response[j]['id']
        project_name = repo_response[j]['name']
        project_full_name = repo_response[j]['full_name']
        project_html_url = repo_response[j]['html_url']
        project_owner_name = repo_response[j]['owner']['login']
        project_obj = {"id" : project_id, "name": project_name, "full_name" : project_full_name, "html_url" : project_html_url, "owner" : project_owner_name}
        project_list.append(project_obj)

    except:
      print ("exception occurred")    

    if (count == 4990):
      break


    try:

      print(len(repo_response))
      last_id = repo_response[99]["id"]   
      i = last_id      
      repo_result1 = repo_result1 + project_list
          
    except:
      print(" func1 is finished")
      break
    
  with open("repo_file1.json", "w") as repo_file:
    json.dump(repo_result1, repo_file)



def func2():
  i = 1000000
  count = 0
  global repo_result2  
  api_url = 'https://api.github.com/'
  api_token = 'XX'


  while i < 1000000: # This number will be increased to collect all the projects

    repo_url = api_url + 'repositories?since=' + str(i)
    #print(repo_url)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(api_token)}
    repo_response = requests.get(repo_url, headers=headers).json()
    count = count + 1


    print(count)
    project_list = []

    try:

      for j in range(0,len(repo_response)):
        project_id = repo_response[j]['id']
        project_name = repo_response[j]['name']
        project_full_name = repo_response[j]['full_name']
        project_html_url = repo_response[j]['html_url']
        project_owner_name = repo_response[j]['owner']['login']
        project_obj = {"id" : project_id, "name": project_name, "full_name" : project_full_name, "html_url" : project_html_url, "owner" : project_owner_name}
        project_list.append(project_obj)

    except:
      print ("exception occurred")    

    if (count == 4990):
      break


    try:

      #print(len(repo_response))
      last_id = repo_response[99]["id"]   
      i = last_id      
      repo_result2 = repo_result2 + project_list
          
    except:
      print(" func2 is finished")
      break
    
  with open("repo_file2.json", "w") as repo_file:
    json.dump(repo_result2, repo_file)



if __name__ == '__main__':
  lock = Lock()    
  p1 = Process(target=func1)  
  p2 = Process(target=func2)
  p1.start()
  p2.start()  
  p1.join()  
  p2.join()
  
