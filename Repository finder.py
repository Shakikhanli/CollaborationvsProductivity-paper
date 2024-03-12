import requests
import json
import time

client_id = ''  # you have to write your own id
client_secret = ''  # you have to write your own secret
item_count = 0
data = []
json_string = ''
name = ''
html_url = ''
search_query = 'backend_javascript'


def internet_on(url):
    try:
        lp = requests.get(url, timeout=5)
        return True
    except requests.ConnectionError:
        print("No internet connection !!!")
        return False


def collect_page(search_date):
    items_list = []
    first_url = 'https://api.github.com/search/repositories?q=frontend+language:javascript+created:' + search_date + \
                '..' + search_date + '&?client_id=' + client_id + '&client_secret=' + \
                client_secret + 'per_page=45&page=1'
    if internet_on(first_url):
        res = requests.get(first_url)
        file_content = res.json()
        items_list.append(file_content['items'])
    else:
        print('Application going to sleep for 65 seconds...')
        time.sleep(65)
    print(first_url)
    while 'next' in res.links.keys():  # taking all url through pagination until it ends
        if internet_on(first_url):
            try:
                res = requests.get(first_url)
                file_content = res.json()
                items_list.append(file_content['items'])
                first_url = res.links['next']['url']
            except:
                time.sleep(70)
                print('Api ratio is exceed. Application going to sleep for 70 seconds...')
                break
        else:
            print('Application going to sleep for 65 seconds...')
            time.sleep(65)
        print(first_url)

    print("All repository pages are collected...")
    return items_list


def define_date(start_year, start_month, start_day):
    end_year = '2023'
    end_month = '12'
    end_day = '30'
    dates = []
    condition = True
    while condition:
        if (int(end_day) <= 31) and (int(end_day) > 10):
            end_day = str(int(end_day) - 1)

        if (int(end_day) <= 10) and (int(end_day) > 0):
            end_day = '0' + str(int(end_day) - 1)

        if int(end_day) == 0:
            end_day = '31'
            if (int(end_month) <= 12) and (int(end_month) > 10):
                end_month = str(int(end_month) - 1)
            if (int(end_month) <= 10) and (int(end_month) > 0):
                end_month = '0' + str(int(end_month) - 1)
            if int(end_month) == 0:
                end_month = '12'
                end_year = str(int(end_year) - 1)
        date = end_year + '-' + end_month + '-' + end_day
        dates.append(date)
        date = ''
        if (end_day == start_day) and (end_month == start_month) and (end_year == start_year):
            condition = False
            print('All dates between duration is collected.')
    return dates


for date in define_date('2023', '01', '01'):
    print('Processing of pages for date:' + date + ' is started.')
    try:
        for each_item_list in collect_page(date):
            for each_item in each_item_list:
                try:
                    name = each_item['owner']['login']
                    html_url = each_item['owner']['html_url']
                    json_string = json_string + '{"owner_name":"' + name + '","owner_url":"' + html_url + '"}'
                    json_file = json.loads(json_string)
                    data.append(json_file)
                    json_string = ''
                except:
                    print('Api ratio is exceed. Application going to sleep for 65 seconds...')
                    time.sleep(65)
                    continue
    except:
        print('There is an ERROR !!!   Application going to sleep for 60 seconds')
        time.sleep(60)
        continue
    print('All items of current page are collected.')
    print('')

# df = pd.DataFrame.from_dict(json_normalize(data), orient='columns')
# result = df.sort_values('owner_name')
# Export = df.to_json('/Json files/' + '2019/09/01' + r'.json')

with open('/Json files/' + '(2023-01-01)---(2023-12-30).json', 'w') as file:
    json.dump(data, file)