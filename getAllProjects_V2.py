from multiprocessing import Process,Lock
import time
import json
import requests
  
## Downloading all the projects
repo_result = []

Token_list = ['557d55dde3f4e15b876267910ef4a4972ca29384','e6fa26fca89ff5c562b8ed6ed5e2d95b1f8186c4']

i = 0
count = 0
  
api_url = 'https://api.github.com/'



while i < 10000: # This number will be increased to collect all the projects

  repo_url = api_url + 'repositories?since=' + str(i)
  #print(repo_url)

  
  exception_count = 0
  while exception_count < 2:
    for k in range(0,len(Token_list)):
      try:
        headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(Token_list[k])}
        repo_response = requests.get(repo_url, headers=headers).json()        
        break        
      except:
        continue
    if k == len(Token_list):
      time.sleep(1000)
      exception_count = exception_count + 1
    else:
      break      

  
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
      count = count + 1


  except:
    print ("exception occurred")    

  if (count == 4990):
    break


  try:

    print(len(repo_response))
    last_id = repo_response[99]["id"]   
    i = last_id      
    repo_result = repo_result + project_list
        
  except:
    print(" finished ")
    break

  ## Removing projects having less than 8 issues
  p = 0
  while p < len(repo_result):
    
    repo_owner = repo_result[p]['owner']
    repo_name = repo_result[p]['name']
    issue_url = api_url + 'repos/' + repo_owner + '/' + repo_name + '/' + 'issues'
    #print(issue_url)

    exception_count = 0
    while exception_count < 2:
      for k in range(0,len(Token_list)):
        try:
          headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(Token_list[k])}
          issue_response = requests.get(issue_url, headers=headers).json()          
          break
        except:
          continue
      if k == len(Token_list):
        time.sleep(1000)
        exception_count = exception_count + 1
      else:
        break


    if(len(issue_response) > 10):
      p = p + 1
    else:
      repo_result.pop(p)

  #print('List of all projects with more than 8 issues -> ', len(repo_result))

  ## Selecting the projects with Pull Request > 0

  m = 0

  while m < len(repo_result):
    repo_owner = repo_result[m]['owner']
    repo_name = repo_result[m]['name']
    PR_url = api_url + 'repos/' + repo_owner + '/' + repo_name + '/' + 'pulls?state=all'

    exception_count = 0
    while exception_count < 2:
      for k in range(0,len(Token_list)):
        try:
          headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(Token_list[k])}
          PR_response = requests.get(PR_url, headers=headers).json()          
          break
        except:
          continue
      if k == len(Token_list):
        time.sleep(1000)
        exception_count = exception_count + 1
      else:
        break


    if(len(PR_response) > 0):      
      m = m + 1
    else:      
      repo_result.pop(m)
  
  ## Selecting Projects with commits > 20
  n = 0

  while n < len(repo_result):
    repo_owner = repo_result[n]['owner']
    repo_name = repo_result[n]['name']
    commit_url = api_url + 'repos/' + repo_owner + '/' + repo_name + '/' + 'commits'


    exception_count = 0
    while exception_count < 2:
      for k in range(0,len(Token_list)):
        try:
          headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(Token_list[k])}
          commit_response = requests.get(commit_url, headers=headers).json()          
          break
        except:
          continue
      if k == len(Token_list):
        time.sleep(1000)
        exception_count = exception_count + 1
      else:
        break

    if(len(commit_response) > 20):      
      n = n + 1
    else:      
      repo_result.pop(n)


with open("repo_file.json", "w") as repo_file:
  json.dump(repo_result, repo_file)
  print(len(repo_result))
    
    