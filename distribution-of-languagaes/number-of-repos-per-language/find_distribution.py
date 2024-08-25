import csv
import matplotlib.pyplot as plt

def count_unique_values(list):
    count_dict = {}
    for item in list:
        if item in count_dict:
            count_dict[item] += 1
        else:
            count_dict[item] = 1
    return count_dict

repos=[]
with open("projects-accepted-revised.txt") as file1:
    lines = file1.readlines()
    for line in lines:
        repos.append(line.strip())
      
occurance=[]   
with open ("ghs_results.csv") as file2:
    reader = csv.reader(file2)
    next(reader)
    for row in reader:
            #if repo is in accepted projects
            if row[1] in repos:
                #add the programming language of project
                occurance.append(row[7])
occurance_dict = count_unique_values(occurance)
print(occurance_dict)