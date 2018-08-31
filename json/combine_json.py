import json

combined_list = []

for i in range(1,5):
	with open('repo_file' + str(i) + '.json') as json_file:
	   	data = json.load(json_file)	   	
	   	combined_list = combined_list + data

print(len(combined_list))

## Removing duplicates from combined_list  

seen = set()
new_list = []
for d in combined_list:
    t = tuple(d.items())
    if t not in seen:
        seen.add(t)
        new_list.append(d)

print(len(new_list))

with open("combined_list.json", "w") as repo_file:
    json.dump(new_list, repo_file)