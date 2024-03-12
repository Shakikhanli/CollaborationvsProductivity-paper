import os
import json
import pandas as pd
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

address_folder_multi = "address for multi repository projects"
address_folder_mono = "address for mono repository projects"

count = 0
total_count = len(os.listdir(address_folder_mono))
index = 0

dict_list = []
dict_list_mono = []
dict_list_multi = []

one_branch = 0
between_50_100 = 0
between_100_200 = 0
more_than_200 = 0



""" *********************************************** Mono Repository ************************************************ """
for each_file in os.listdir(address_folder_mono):
    count += 1
    print(total_count - count)

    if '.json' in each_file:
        commit_count = 0
        # print(each_file)
        with open(address_folder_mono + '/' + each_file, 'r', encoding="utf8") as file:
            file_content = json.load(file)

            start = datetime.fromisoformat(file_content['created_at'][:-1])
            end = datetime.fromisoformat(file_content['last_update'][:-1])

            dev_period = (end - start).days

            if len(file_content['contributors']) > 2 and file_content['Average collaboration value'] < 500 and 60 < dev_period < 2500:
                index += 1

                dict1 = {'Development Period': dev_period,
                         'Collaboration ratio': file_content['Average collaboration value']}

                dict_list.append(dict1)
                dict_list_mono.append(dict1)

""" *********************************************** Multi Repository (Front) ************************************************ """
total_count = len(os.listdir(address_folder_multi))
count = 0

for each_file in os.listdir(address_folder_multi):
    count += 1
    print(total_count - count)

    if '.json' in each_file:
        commit_count = 0
        # print(each_file)
        with open(address_folder_multi + '/' + each_file, 'r', encoding="utf8") as file:
            file_content = json.load(file)

            branches = []
            developers = []

            commit_count = len(file_content['Front Repositories']['commits']) + len(file_content['Back Repositories']['commits'])

            start_front = datetime.fromisoformat(file_content['Front Repositories']['created_at'][:-1])
            end_front = datetime.fromisoformat(file_content['Front Repositories']['last_update'][:-1])

            start_back = datetime.fromisoformat(file_content['Back Repositories']['created_at'][:-1])
            end_back = datetime.fromisoformat(file_content['Back Repositories']['last_update'][:-1])

            start = start_front if start_front < start_back else start_back
            end = end_front if end_front > end_back else end_back

            dev_period = (end - start).days

            for each_dev in file_content['Front Repositories']['contributors']:
                developers.append(each_dev['login'])

            for each_dev in file_content['Back Repositories']['contributors']:
                developers.append(each_dev['login'])

            # branches = list(set(branches))
            unique_developers = list(set(developers))

            if len(unique_developers) > 2 and 60 < dev_period < 2500:
                dict1 = {'Development Period': dev_period,
                         'Collaboration ratio': file_content['Average collaboration value']}

                dict_list.append(dict1)
                dict_list_multi.append(dict1)

""" ************************************ Create Scatter Plot with correlation line Mono vs Multi ******************* """

# Sort both datasets by 'Collaboration Ratio'
dict_list_mono = sorted(dict_list_mono, key=lambda x: x['Collaboration ratio'])
dict_list_multi = sorted(dict_list_multi, key=lambda x: x['Collaboration ratio'])

# Combine both datasets
combined_data = dict_list_mono + dict_list_multi

# Extract 'Commit Count' and 'Collaboration Ratio'
commit_count = [entry['Development Period'] for entry in combined_data]
collaboration_ratio = [entry['Collaboration ratio'] for entry in combined_data]

# Create the scatter plot with different markers for each dataset
plt.figure(figsize=(8, 6))

# Plot data from dict_list_mono with blue markers
plt.scatter(
    [entry['Collaboration ratio'] for entry in dict_list_mono],
    [entry['Development Period'] for entry in dict_list_mono],
    marker='o', color='blue', label='Mono Data', s=10
)

# Plot data from dict_list_multi with red markers
plt.scatter(
    [entry['Collaboration ratio'] for entry in dict_list_multi],
    [entry['Development Period'] for entry in dict_list_multi],
    marker='o', color='red', label='Multi Data', s=10
)

# Adding labels and title
plt.xlabel('Collaboration Ratio')
plt.ylabel('Development Period')
plt.title('Scatter Plot of Development Period vs. Collaboration Ratio (Combined Data)')

# Calculate and show the correlation coefficients for each dataset
correlation_coefficient_mono, _ = pearsonr(
    [entry['Collaboration ratio'] for entry in dict_list_mono],
    [entry['Development Period'] for entry in dict_list_mono]
)

correlation_coefficient_multi, _ = pearsonr(
    [entry['Collaboration ratio'] for entry in dict_list_multi],
    [entry['Development Period'] for entry in dict_list_multi]
)

# Create custom legend labels including dataset identifier and correlation coefficient
legend_labels = [
    f'Mono Data (Correlation: {correlation_coefficient_mono:.2f})',
    f'Multi Data (Correlation: {correlation_coefficient_multi:.2f})'
]

# Add regression lines for each dataset
z_mono = np.polyfit(
    [entry['Collaboration ratio'] for entry in dict_list_mono],
    [entry['Development Period'] for entry in dict_list_mono],
    1
)

z_multi = np.polyfit(
    [entry['Collaboration ratio'] for entry in dict_list_multi],
    [entry['Development Period'] for entry in dict_list_multi],
    1
)

p_mono = np.poly1d(z_mono)
p_multi = np.poly1d(z_multi)

plt.plot(
    [entry['Collaboration ratio'] for entry in dict_list_mono],
    p_mono([entry['Collaboration ratio'] for entry in dict_list_mono]),
    'b--',
    label=f'Mono Data Line (y={z_mono[0]:.2f}x+{z_mono[1]:.2f})'
)

plt.plot(
    [entry['Collaboration ratio'] for entry in dict_list_multi],
    p_multi([entry['Collaboration ratio'] for entry in dict_list_multi]),
    'r--',
    label=f'Multi Data Line (y={z_multi[0]:.2f}x+{z_multi[1]:.2f})'
)

# Show the legend with custom labels
plt.legend(legend_labels)

# Show the chart
plt.grid(True)
plt.show()





























