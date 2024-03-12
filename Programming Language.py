import os
import json
import pandas as pd
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from collections import Counter

address_folder_multi = "address for multi repository projects"
address_folder_mono = "address for mono repository projects"

count = 0
total_count = len(os.listdir(address_folder_multi))
index = 0

dict_list = []
dict_list_mono = []
dict_list_multi = []



""" *********************************************** Mono Repository ************************************************ """
# for each_file in os.listdir(address_folder_mono):
#     count += 1
#     print(total_count - count)
#
#     if '.json' in each_file:
#         commit_count = 0
#         # print(each_file)
#         with open(address_folder_mono + '/' + each_file, 'r', encoding="utf8") as file:
#             file_content = json.load(file)
#
#             if len(file_content['contributors']) > 2 and file_content['Average collaboration value'] < 500:
#                 index += 1
#
#                 dict1 = {'Programming language': file_content['languages'],
#                          'Collaboration ratio': file_content['Average collaboration value']}
#
#                 dict_list.append(dict1)
#                 dict_list_mono.append(dict1)

""" *********************************************** Multi Repository (Front) ************************************************ """

for each_file in os.listdir(address_folder_multi):
    count += 1
    print(total_count - count)

    if '.json' in each_file:
        commit_count = 0
        # print(each_file)
        with open(address_folder_multi + '/' + each_file, 'r', encoding="utf8") as file:
            file_content = json.load(file)

            developers = []

            for each_dev in file_content['Front Repositories']['contributors']:
                developers.append(each_dev['login'])

            for each_dev in file_content['Back Repositories']['contributors']:
                developers.append(each_dev['login'])

            unique_developers = list(set(developers))

            if len(unique_developers) > 2 and (file_content['Back Repositories']['languages'] != 'Jupyter Notebook' and
                                               file_content['Back Repositories']['languages'] != 'HTML'):
                dict1 = {'Programming language': file_content['Back Repositories']['languages'],
                         'Collaboration ratio': file_content['Average collaboration value']}

                dict_list.append(dict1)
                dict_list_multi.append(dict1)

""" ************************************ Create Scatter Plot with correlation line Mono vs Multi ******************* """
# data = dict_list_mono
#
# # Define the collaboration ratio ranges
# ranges = [0, 50, 100, 200, float('inf')]
# labels = ['0-50', '51-100', '101-200', '200+']
#
# # Initialize counters for each range and language
# counters = {language: np.zeros(len(ranges) - 1) for language in set(entry["Programming langauge"] for entry in data)}
#
# # Count data points within each range for each language
# for entry in data:
#     lang = entry["Programming langauge"]
#     ratio = entry["Collaboration ratio"]
#     for i in range(len(ranges) - 1):
#         if ranges[i] <= ratio < ranges[i + 1]:
#             counters[lang][i] += 1
#
# # Calculate total counts for each range
# total_counts = np.zeros(len(ranges) - 1)
# for language, counts in counters.items():
#     total_counts += counts
#
# # Create a stacked bar chart
# bottom = np.zeros(len(ranges) - 1)
# for language, counts in counters.items():
#     percentages = [count / total_count * 100 if total_count > 0 else 0 for count, total_count in zip(counts, total_counts)]
#     plt.bar(labels, counts, label=language, bottom=bottom)
#
#     # Add percentage labels inside the bars
#     for i, count in enumerate(counts):
#         if count > 0:
#             plt.text(i, bottom[i] + count / 2, f'{percentages[i]:.2f}%', ha='center', va='center')
#
#     bottom += counts
#
# # Add labels and title
# plt.xlabel('Collaboration Ratio Ranges')
# plt.ylabel('Count')
# plt.title('Programming Language Distribution by Collaboration Ratio Ranges')
#
# # Show the legend
# plt.legend()
#
# # Show the plot
# plt.show()

""" ************************************ Create Scatter Plot with correlation line Mono vs Multi ******************* """
# data = dict_list_multi
#
# # Define the collaboration ratio ranges
# ranges = [0, 50, 100, 200, float('inf')]
# labels = ['0-50', '51-100', '101-200', '200+']
#
# # Initialize counters for each range and language
# counters = {language: np.zeros(len(ranges) - 1) for language in set(entry["Programming language"] for entry in data)}
#
# # Count data points within each range for each language
# for entry in data:
#     lang = entry["Programming language"]
#     ratio = entry["Collaboration ratio"]
#     for i in range(len(ranges) - 1):
#         if ranges[i] <= ratio < ranges[i + 1]:
#             counters[lang][i] += 1
#
# # Calculate total counts for each range
# total_counts = np.zeros(len(ranges) - 1)
# for language, counts in counters.items():
#     total_counts += counts
#
# # Filter out languages with percentages lower than 2%
# filtered_counters = {language: counts for language, counts in counters.items() if any(count / total_count >= 0.02 for count, total_count in zip(counts, total_counts))}
#
# # Create a stacked bar chart
# bottom = np.zeros(len(ranges) - 1)
# for language, counts in filtered_counters.items():
#     percentages = [count / total_count * 100 if total_count > 0 else 0 for count, total_count in zip(counts, total_counts)]
#     plt.bar(labels, percentages, label=language, bottom=bottom)
#
#     # Add percentage labels inside the bars
#     for i, percentage in enumerate(percentages):
#         if percentage > 1:
#             plt.text(i, bottom[i] + percentage / 2, f'{percentage:.2f}%', ha='center', va='center')
#
#     bottom += percentages
#
# # Add labels and title
# plt.xlabel('Collaboration Ratio Ranges')
# plt.ylabel('Percentage')
# plt.title('Programming Language Distribution by Collaboration Ratio Ranges')
#
# # Show the legend with filtered languages
# plt.legend()
#
# # Show the plot
# plt.show()

print(dict_list_multi)


















