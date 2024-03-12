import os
import json
import pandas as pd
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import numpy as np

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

            if len(file_content['contributors']) > 2 and 0 < len(file_content['commits']) < 4000 and file_content['Average collaboration value'] < 1000:
                index += 1

                dict1 = {'Commit count': len(file_content['commits']),
                         'Collaboration ratio': file_content['Average collaboration value']}

                dict_list.append(dict1)
                dict_list_mono.append(dict1)

""" *********************************************** Multi Repository (Front) ************************************************ """
total_count = len(os.listdir(address_folder_multi))

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

            for each_dev in file_content['Front Repositories']['branches']:
                if 'depend' not in each_dev['name']:
                    branches.append(each_dev['name'])

            for each_dev in file_content['Back Repositories']['branches']:
                if 'depend' not in each_dev['name']:
                    branches.append(each_dev['name'])

            for each_dev in file_content['Front Repositories']['contributors']:
                developers.append(each_dev['login'])

            for each_dev in file_content['Back Repositories']['contributors']:
                developers.append(each_dev['login'])

            branches = list(set(branches))
            unique_developers = list(set(developers))

            if len(unique_developers) > 2 and 0 < commit_count < 4000:
                dict1 = {'Commit count': commit_count,
                         'Collaboration ratio': file_content['Average collaboration value']}

                dict_list.append(dict1)
                dict_list_multi.append(dict1)

""" ************************************ Create Scatter Plot with correlation line ********************************* """
# # data = dict_list_mono
# data = dict_list_multi
#
# # Sort the data by 'Collaboration Ratio'
# sorted_data = sorted(data, key=lambda x: x['Collaboration ratio'])
#
# # Extract 'Commit Count' and 'Collaboration Ratio' after sorting
# commit_count = [entry['Commit count'] for entry in sorted_data]
# collaboration_ratio = [entry['Collaboration ratio'] for entry in sorted_data]
#
# # Calculate the correlation coefficient
# correlation_coefficient, _ = pearsonr(commit_count, collaboration_ratio)
#
# # Create the scatter plot
# plt.figure(figsize=(8, 6))
# plt.scatter(collaboration_ratio, commit_count, marker='o', label='Data Points', s=10)
#
# # Adding labels and title
# plt.xlabel('Collaboration Ratio')
# plt.ylabel('Commit Count')
# plt.title('Commit Count vs. Collaboration Ratio')
#
# # Add a correlation line
# z = np.polyfit(collaboration_ratio, commit_count, 1)
# p = np.poly1d(z)
# plt.plot(collaboration_ratio, p(collaboration_ratio), 'r--', label=f'Correlation Line (y={z[0]:.2f}x+{z[1]:.2f})')
#
# # Show the correlation coefficient on the chart
# plt.text(
#     0.7, 0.1,
#     f'Correlation Coefficient: {correlation_coefficient:.2f}',
#     transform=plt.gca().transAxes
# )
#
# # Show the chart
# plt.grid(True)
# plt.legend()
# plt.show()

""" ************************************ Create Scatter Plot with correlation line Mono vs Multi ******************* """

# Sort both datasets by 'Collaboration Ratio'
dict_list_mono = sorted(dict_list_mono, key=lambda x: x['Collaboration ratio'])
dict_list_multi = sorted(dict_list_multi, key=lambda x: x['Collaboration ratio'])

# Combine both datasets
combined_data = dict_list_mono + dict_list_multi

# Extract 'Commit Count' and 'Collaboration Ratio'
commit_count = [entry['Commit count'] for entry in combined_data]
collaboration_ratio = [entry['Collaboration ratio'] for entry in combined_data]

# Create the scatter plot with different markers for each dataset
plt.figure(figsize=(8, 6))

# Plot data from dict_list_mono with blue markers
plt.scatter(
    [entry['Collaboration ratio'] for entry in dict_list_mono],
    [entry['Commit count'] for entry in dict_list_mono],
    marker='o', color='blue', label='Mono Data', s=10
)

# Plot data from dict_list_multi with red markers
plt.scatter(
    [entry['Collaboration ratio'] for entry in dict_list_multi],
    [entry['Commit count'] for entry in dict_list_multi],
    marker='o', color='red', label='Multi Data', s=10
)

# Adding labels and title
plt.xlabel('Collaboration Ratio')
plt.ylabel('Commit Count')
plt.title('Scatter Plot of Commit Count vs. Collaboration Ratio (Combined Data)')

# Calculate and show the correlation coefficients for each dataset
correlation_coefficient_mono, _ = pearsonr(
    [entry['Collaboration ratio'] for entry in dict_list_mono],
    [entry['Commit count'] for entry in dict_list_mono]
)

correlation_coefficient_multi, _ = pearsonr(
    [entry['Collaboration ratio'] for entry in dict_list_multi],
    [entry['Commit count'] for entry in dict_list_multi]
)

# Create custom legend labels including dataset identifier and correlation coefficient
legend_labels = [
    f'Mono Data (Correlation: {correlation_coefficient_mono:.2f})',
    f'Multi Data (Correlation: {correlation_coefficient_multi:.2f})'
]

# Add regression lines for each dataset
z_mono = np.polyfit(
    [entry['Collaboration ratio'] for entry in dict_list_mono],
    [entry['Commit count'] for entry in dict_list_mono],
    1
)

z_multi = np.polyfit(
    [entry['Collaboration ratio'] for entry in dict_list_multi],
    [entry['Commit count'] for entry in dict_list_multi],
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
