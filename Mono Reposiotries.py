import requests
import json
import time
import pickle
import pandas as pd
import xlsxwriter
from datetime import datetime, date, timedelta


count = 1
file_number = -1
repo_count = 0
all_found = 0
limit = 4800


def check_name(repo_name):
    warning_names = ['course', 'book', 'tutorial', 'lesson', 'teach', 'part', 'internship', 'bootcamp', 'notes',
                     'collection']
    repo_name = repo_name.lower()
    for name in warning_names:
        if repo_name.__contains__(name):
            return False

    return True


def create_dates():
    date_list = []
    first_date = datetime.strptime('2021-01-01', '%Y-%m-%d').date()
    second_Date = first_date + timedelta(days=15)

    # print(first_date)
    date_list.append(first_date)
    date_list.append(second_Date)

    for index in range(0, 23):
        first_date = second_Date + timedelta(days=1)
        second_Date = second_Date + timedelta(days=15)

        date_list.append(first_date)
        date_list.append(second_Date)

        # print('1st date: ' + str(first_date) + ' // ' + '2nd date: ' + str(second_Date))

    return date_list


df = pd.DataFrame(
    columns=['Repo owner', 'Repository', 'Repo_url'])

collected_repos = []
dict_list = []

headers = {
    'Authorization': 'Token {You should put here your token which you received from Github API}'
}
url = 'https://api.github.com/search/repositories?q=fullstack+language:javascript+created:2022-01-01..2022-01-15'

response = requests.request("GET", url, headers=headers)
file_content = json.loads(response.text)

for each_item in file_content['items']:

    all_found += 1
    if each_item['fork'] == False and check_name(each_item['name']) and each_item['name'] not in collected_repos:
        repo_count += 1
        collected_repos.append(each_item['name'])
        dict1 = {'Repo owner': '', 'Repository': '', 'Repo_url': ''}

        dict1['Repo owner'] = each_item['owner']['login']
        dict1['Repository'] = each_item['name']
        dict1['Repo_url'] = each_item['url']

        dict_list.append(dict1)

        # series = pd.Series(dict1)
        # series.to_frame()
        # df = df.append(series, ignore_index=True)
        # df = pd.DataFrame.from_records(dict_list)

print('Total Amount of collected repos: ' + str(repo_count))
print(url)

bla = 0

# print(response.links.keys())

while 'next' in response.links.keys():
    count += 1

    try:

        url = response.links['next']['url']
        response = requests.request("GET", url, headers=headers)
        file_content = json.loads(response.text)

        # if 'documentation_url' not in file_content:

        for each_item in file_content['items']:

            all_found += 1
            if each_item['fork'] == False and check_name(each_item['name']) and each_item['name'] not in collected_repos:
                repo_count += 1
                collected_repos.append(each_item['name'])
                dict1 = {'Repo owner': '', 'Repository': '', 'Repo_url': ''}

                dict1['Repo owner'] = each_item['owner']['login']
                dict1['Repository'] = each_item['name']
                dict1['Repo_url'] = each_item['url']

                dict_list.append(dict1)
        # else:
        #     print('Secondary limit reached. Application will sleep for 5 mins ...')
        #     time.sleep(3)

    except Exception as error:
        print(url)
        print(file_content)
        print(error)
        time.sleep(3)
        continue

        # series = pd.Series(dict1)
        # series.to_frame()
        # df = df.append(series, ignore_index=True)
        # df = pd.DataFrame.from_records(dict_list)

    print('Total Amount of collected repos: ' + str(repo_count))
    print(url)







df = pd.DataFrame.from_records(dict_list)

writer = pd.ExcelWriter('Excel files/test.xlsx', engine='xlsxwriter')
df.to_excel(writer, 'Sheet1')
writer.save()


print('Totak amout: ' + str(all_found))
