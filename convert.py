import csv
import re

# Text output from the pipe
output = '''
Legend:
- #STEPS: Number of steps taken.
- SEC/STEP, $/STEP: Average time (cost) per step.
- EST(hr), EST($): Estimated total time (cost) to complete the benchmark.

CLUSTER               RESOURCES              STATUS    DURATION  SPENT($)  #STEPS  SEC/STEP  $/STEP  EST(hr)  EST($)  
sky-bench-mybench2-0  1x AWS(m6i.large)      FINISHED  < 1s      0.0000    -       -         -       -        -       
sky-bench-mybench2-1  1x GCP(n2-standard-2)  FINISHED  < 1s      0.0000    -       -         -       -        -       
SkyCallback logs are not found in this benchmark. Consider using SkyCallback to get more detailed information in real time.
'''

# Extract lines that contain relevant data
data_lines = [line.strip() for line in output.split('\n') if re.match(r'^sky-bench', line)]

# Define the CSV header
header = ['CLUSTER', 'RESOURCES', 'STATUS', 'DURATION', 'SPENT($)', '#STEPS', 'SEC/STEP', '$/STEP', 'EST(hr)', 'EST($)']

# Extract data from each line
data = [re.split(r'\s{2,}', line) for line in data_lines]

# Write data to a CSV file
with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    writer.writerows(data)

print('The output has been saved as output.csv')
