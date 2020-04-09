import pandas as pd
import requests
import  numpy as np
# make a csv of top 1000 players for visualization

data = pd.read_csv("data.csv")
data.drop(["Unnamed: 0"], inplace=True, axis=1)
data = data.sort_values(by ='Overall', ascending=False)
new_data = data[:1001]
new_data.to_csv (r'data_1000_top_players.csv', index = False, header=True)


data = data.sort_values(by ='Overall' , ascending=False)
new_data = data[:1001]

new_data["Photo"]= new_data["Photo"].str.replace("/4/19/", "/10/20/", case = False)
new_data["Photo"]= new_data["Photo"].str.replace(".org/", ".com/", case = False)


for i, row in new_data.iterrows():
    r = requests.get(row.Photo, allow_redirects=True)
    with open('top_1000_players/'+row.Photo.split("/")[-1], 'wb') as f:
        f.write(r.content)


for i, row in data.iterrows():
    r = requests.get(row.Flag, allow_redirects=True)
    with open('flags/'+row.Photo.split("/")[-1], 'wb') as f:
        f.write(r.content)


flist = ['LS', 'ST', 'RS', 'LW', 'LF', 'CF', 'RF', 'RW',
         'LAM', 'CAM', 'RAM', 'LM', 'LCM', 'CM', 'RCM', 'RM', 'LWB', 'LDM',
         'CDM', 'RDM', 'RWB', 'LB', 'LCB', 'CB', 'RCB', 'RB']
data = pd.read_csv("data.csv")
data = data.replace(np.NaN ,0)

for i, row in data.iterrows():
    for column in flist:
        data.at[i, column] = eval(str(row[column]))


data = pd.read_csv("data.csv")
data["Club Logo"]
data["Club Logo"]= data["Club Logo"].str.replace(".org/", ".com/", case = False)
data["Club Logo"]= data["Club Logo"].str.replace("/2/", "/5/", case = False)
data = data.sort_values(by ='Overall' , ascending=False)
new_data = data[:1001]
"""
for i, row in new_data.iterrows():
    r = requests.get(row["Club Logo"], allow_redirects=True)
    with open('top_1000_clubs/'+row["Club Logo"].split("/")[-1], 'wb') as f:
        f.write(r.content)
"""

data = pd.read_csv("data.csv")
data["Flag"]= data["Flag"].str.replace(".org/", ".com/", case = False)
data = data.sort_values(by ='Overall' , ascending=False)
new_data = data[:1001]
"""
for i, row in new_data.iterrows():
    r = requests.get(row.Flag, allow_redirects=True)
    with open('top_1000_flags/'+row.Flag.split("/")[-1], 'wb') as f:
        f.write(r.content)
"""

