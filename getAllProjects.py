import json
import requests

api_token = '6921c5aa4b0f4fb38700091ffe07e07b738fa3d1'
api_url = 'https://api.github.com/'
  
## Downloading all the projects
i = 0
repo_result = []
while i < 500: # This number will be increased to collect all the projects
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

print('List of all projects with more than 20 commits -> ', len(repo_result))



## Removing projects having less than 8 issues
i = 0
while i < len(repo_result):
  repo_owner = repo_result[i]['owner']['login']
  repo_name = repo_result[i]['name']
  issue_url = api_url + 'repos/' + repo_owner + '/' + repo_name + '/' + 'issues'
  print(issue_url)
  headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(api_token)}
  issue_response = requests.get(issue_url, headers=headers).json()

  print(len(issue_response))

  if(len(issue_response) > 10):
    print("we can take this repo")
    i = i + 1
  else:
    print("this repo will be rejected")
    repo_result.pop(i)

print('List of all projects with more than 8 issues -> ', len(repo_result))

## Selecting only software engineering projects


## Selecting the projects with Pull Request > 0
i = 0
while i < len(repo_result):
  repo_owner = repo_result[i]['owner']['login']
  repo_name = repo_result[i]['name']
  PR_url = api_url + 'repos/' + repo_owner + '/' + repo_name + '/' + 'pulls?state=all'
  print(PR_url)
  headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(api_token)}
  PR_response = requests.get(PR_url, headers=headers).json()

  print(len(PR_response))

  if(len(PR_response) > 0):
    print("we can take this repo")
    i = i + 1
  else:
    print("this repo will be rejected")
    repo_result.pop(i)

print('List of all projects with atleast 1 PR -> ', len(repo_result))


## Selecting the projects with no. of releases > 0
i = 0
while i < len(repo_result):
  repo_owner = repo_result[i]['owner']['login']
  repo_name = repo_result[i]['name']
  release_url = api_url + 'repos/' + repo_owner + '/' + repo_name + '/' + 'releases'
  print(release_url)
  headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(api_token)}
  release_response = requests.get(release_url, headers=headers).json()

  print(len(release_response))

  if(len(release_response) > 0):
    print("we can take this repo")
    i = i + 1
  else:
    print("this repo will be rejected")
    repo_result.pop(i)

print('List of all projects with atleast 1 release -> ', len(repo_result))