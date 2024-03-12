""" This script only collects names of users and list of their repositories"""
import requests
import json
import time
import itertools
import pandas as pd
import xlsxwriter
from datetime import datetime, date, timedelta

count = 1
file_number = -1
user_count = 0
all_found = 0
limit = 4800
languages = ['javascript', 'typescript', 'java', 'python', 'php', 'c#', 'go', 'ruby', 'html']


def check_name(repo_name):
    warning_names = ['course', 'book', 'tutorial', 'lesson', 'teach', 'part', 'internship', 'bootcamp', 'notes',
                     'collection']
    repo_name = repo_name.lower()
    for name in warning_names:
        if repo_name.__contains__(name):
            return False

    return True


def get_repo_list(user_name):
    repo_list = []
    headers = {
        'Authorization': 'Token {You should put here your token which you received from Github API}'
    }
    url = 'https://api.github.com/users/' + user_name + '/repos'

    response = requests.request("GET", url, headers=headers)
    file_content = json.loads(response.text)

    for each_repo in file_content:
        if not each_repo['fork']:
            repo_list.append(each_repo['name'])

    return repo_list


def create_dates():
    date_list = []
    first_date = datetime.strptime('2022-01-01', '%Y-%m-%d').date()
    second_Date = first_date + timedelta(days=7)

    date_str = str(first_date) + '..' + str(second_Date)
    date_list.append(date_str)

    for index in range(0, 11):
        first_date = second_Date + timedelta(days=1)
        second_Date = second_Date + timedelta(days=15)

        date_str = str(first_date) + '..' + str(second_Date)
        date_list.append(date_str)

    return date_list


collected_users = []

excel_data_df = pd.read_excel('Excel files/2016-2021.xlsx', sheet_name='Sheet1', engine='openpyxl')
json_str = excel_data_df.to_json(orient="records")
projects = json.loads(json_str)

for each_project in projects:
    collected_users.append(each_project['User'])

excel_data_df = pd.read_excel('Excel files/2021(3).xlsx', sheet_name='Sheet1', engine='openpyxl')
json_str = excel_data_df.to_json(orient="records")
projects = json.loads(json_str)

for each_project in projects:
    collected_users.append(each_project['User'])

df = pd.DataFrame(
    columns=['User', 'Repository list', 'Repository list url'])

dict_list = []
date_count = 0
file_count = 0

print('total %d' %len(collected_users))

for each_language in languages:

    for each_date in create_dates():
        date_count += 1
        headers = {
            'Authorization': 'Token {You should put here your token which you received from Github API}'
        }
        url = 'https://api.github.com/search/repositories?q=backend+language:' + each_language + '+created:' + each_date

        response = requests.request("GET", url, headers=headers)
        file_content = json.loads(response.text)

        print(url)

        try:
            for each_item in file_content['items']:

                all_found += 1
                if each_item['fork'] == False and check_name(each_item['name']) and \
                        each_item['owner']['login'] not in collected_users:

                    user_count += 1
                    collected_users.append(each_item['owner']['login'])
                    repository_list = get_repo_list(each_item['owner']['login'])

                    if len(repository_list) > 1:
                        dict1 = {'User': '', 'Repository list': '', 'Repository list url': ''}

                        dict1['User'] = each_item['owner']['login']
                        dict1['Repository list'] = get_repo_list(each_item['owner']['login'])
                        dict1['Repository list url'] = 'https://api.github.com/users/' + each_item['owner'][
                            'login'] + '/repos'

                        dict_list.append(dict1)

        except Exception as error:
            print(url)
            # print(file_content)
            print(error)
            print('There was error. App will sleep for 4 mins')
            time.sleep(240)
            continue

        print('Total Amount of collected users: ' + str(user_count))

        while 'next' in response.links.keys():
            count += 1

            try:

                url = response.links['next']['url']
                response = requests.request("GET", url, headers=headers)
                file_content = json.loads(response.text)

                if 'documentation_url' not in file_content:

                    for each_item in file_content['items']:

                        all_found += 1
                        if each_item['fork'] == False and check_name(each_item['name']) and each_item['owner'][
                            'login'] not in collected_users:

                            user_count += 1
                            collected_users.append(each_item['owner']['login'])
                            repository_list = get_repo_list(each_item['owner']['login'])

                            if len(repository_list) > 1:
                                dict1 = {'User': '', 'Repository list': '', 'Repository list url': ''}

                                dict1['User'] = each_item['owner']['login']
                                dict1['Repository list'] = get_repo_list(each_item['owner']['login'])
                                dict1['Repository list url'] = 'https://api.github.com/users/' + each_item['owner'][
                                    'login'] + '/repos'

                                dict_list.append(dict1)
                else:
                    print('Secondary limit reached. Application will sleep for 4 mins ...')
                    time.sleep(240)

            except Exception as error:
                print(url)
                # print(file_content)
                print(error)
                print('There was error. App will sleep for 5 mins')
                time.sleep(240)
                continue

            print('Total Amount of collected users: ' + str(user_count))

    # if date_count == 2:
    #     file_count += 1
    #     df = pd.DataFrame.from_records(dict_list)
    #
    #     writer = pd.ExcelWriter('Excel files/2020_part(' + str(file_count) + ').xlsx', engine='xlsxwriter')
    #     df.to_excel(writer, 'Sheet1')
    #     writer.save()
    #
    #     print('File have been saved ...')
    #     date_count = 0

df = pd.DataFrame.from_records(dict_list)

writer = pd.ExcelWriter('Excel files/2022(1).xlsx', engine='xlsxwriter')
df.to_excel(writer, 'Sheet1')
writer.save()

print('Total amount: ' + str(file_count))