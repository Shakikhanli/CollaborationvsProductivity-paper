import requests
import json
import pandas as pd

# list_commit_sha = []  # list to save sha of commit
commit_pages = []  # list of urls of commit pages
data = []
client_id = ''  # you have to write your own id
client_secret = ''  # you have to write your own secret
fail_list = []

"""
Function to collect all commit pages
"""


def collect_page(repo_name, project_name):
    number = 0
    collected_pages = []
    first_url = 'https://api.github.com/repos/' \
                + repo_name + '/' + project_name + '/commits?client_id=' \
                + client_id + '&client_secret=' + client_secret + '&per_page=45&page=1'
    res = requests.get(first_url)
    collected_pages.append(first_url)  # adding first url to our list
    while 'next' in res.links.keys():  # taking all url through pagination until it ends
        try:
            number = number + 1
            print(number + " page is collected")
            collected_pages.append(res.links['next']['url'])
            first_url = res.links['next']['url']
            res = requests.get(first_url)
        except:
            break

    print("All commit pages are collected...")
    return collected_pages


"""
Function to collect all sha of all commits
"""


def collect_sha(pages):
    list_commits = []
    list_commit_sha = []
    for each_page in pages:
        page = requests.get(each_page)
        list_commits = page.json()
        # here sha of each commit is taken
    for each_commit in list_commits:
        try:
            list_commit_sha.append(each_commit['sha'])
        except:
            print("This page has problem: " + each_commit)
            print(each_commit)
    print("All commit sha collection is done ... ")
    print(" ")

    return list_commit_sha


"""
Function to create json strings.
"""


def counting_commits(list_commit_sha, repo_name, project_name):
    for x in range(len(list_commit_sha)):
        if len(list_commit_sha) < 20:
            fail_list.append(repo_name + ' // ' + project_name)


df = pd.read_excel('Projects list.xlsx', sheet_name='MERN stack')
count = 0

for index, row in df.iterrows():
    try:
        front_links = '{"links":' + row['Frontend'] + '}'
        data = json.loads(front_links)
        for x in data['links']:
            commit_pages = collect_page(row['Repo_name'], x)
            sha_list = collect_sha(commit_pages)
            counting_commits(sha_list, row['Repo_name'], x)

        back_links = '{"links":' + row['Backend'] + '}'
        data = json.loads(back_links)
        for x in data['links']:
            commit_pages = collect_page(row['Repo_name'], x)
            sha_list = collect_sha(commit_pages)
            counting_commits(sha_list, row['Repo_name'], x)
        print("PROJECT " + str(row['Project_name']) + " finished...")
    except:
        continue

print("FAIL LIST")
print(fail_list)