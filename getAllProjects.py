import json
import requests

api_token = '**'
api_url = 'https://api.github.com/'
  
## Downloading all the projects
i = 0
repo_result = []
while i < 1000: # This number will be increased to collect all the projects
  repo_url = api_url + 'repositories?since=' + str(i)
  print(repo_url)
  headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(api_token)}
  repo_response = requests.get(repo_url, headers=headers).json()
  repo_response_copy = list(repo_response) # cloning the original list to get the id of the last object

  j = 0
  while j < len(repo_response):
    repo_owner = repo_response[j]['owner']['login']
    repo_name = repo_response[j]['name']
    commit_url = api_url + 'repos/' + repo_owner + '/' + repo_name + '/commits'
    print(commit_url)
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(api_token)}
    commit_response = requests.get(commit_url, headers=headers).json()

    print(len(commit_response))

    if(len(commit_response) > 20):
      print("we can take this repo")
      j = j + 1     
    else:
      print("this repo will be rejected")
      repo_response.pop(j)
  try:
    print(len(repo_response_copy))
    id = repo_response_copy[99]["id"]   
    i = id + 1
    print(id)
    repo_result = repo_result + repo_response
    print(i)    
  except:
    print("Done")
    break

with open("repo_file.json", "w") as repo_file:
  json.dump(repo_result, repo_file)

