#Program to scrape astronautix website and get all relevant information regarding solid rocket motors
#Josh Beltrame
#EGR 101

import requests
from bs4 import BeautifulSoup
import xlsxwriter
import string

URL = "http://www.astronautix.com/s/solid.html"
r = requests.get(URL)

soup = BeautifulSoup(r.content, 'html5lib') 

rockets=[]
linksList = []
slicedList = []
subWebpages = []
importantData = ["", "", "", "", "", "", "", "", "", ""] 

badWords = ['0', 'Home', 'Search', 'Browse', 'here', 'Back to top of page', 'Contact', '© / Conditions for Use']

tables = (soup.findAll('table'))
links = soup.findAll("a")


for i in links:
    if(len(i.get_text())<2):
        continue
    elif(i.get_text() in badWords):
        continue
    else:
        rockets.append(i.get_text())


for i in tables:
    for j in range(len(rockets)):
        if rockets[j] in i.get_text():
            linksList.append(i)
            break

for i in range(len(linksList)):
    remv = linksList[i].findChild("a")['href']
    sliced = remv[2:]
    slicedList.append(sliced)

for i in range(len(slicedList)):
    subWebpages.append("http://www.astronautix.com" + slicedList[i])

    
##################################################################################

iterator = 1

workbook = xlsxwriter.Workbook('rocketData.xlsx')
worksheet = workbook.add_worksheet("Rocket Data")

for elem in range(len(subWebpages)):
    print(subWebpages[elem])
    importantData[0] = rockets[elem]
    req = requests.get(subWebpages[elem])
    soup1 = BeautifulSoup(req.content, 'html5lib') 

    abc = (soup1.findAll('p'))

    chunks = []
    for i in abc:
        a = i.get_text().split(' ')
        chunks.append(a)

    for i in range(len(chunks)):
        for j in range(len(chunks[i])):
        
            if((chunks[i][j]) == "Gross") and ((chunks[i][j+1]) == "mass:"):
                importantData[1] =(chunks[i][j] + " "+ chunks[i][j+1] + " "+ chunks[i][j+2] + chunks[i][j+3])
                importantData[7] = (float((chunks[i][j+2].replace(",", "")))) * 9.8
                importantData[7] = str(importantData[7]).replace('.','')
            
            if((chunks[i][j]) == "Unfuelled") and ((chunks[i][j+1]) == "mass:"):
                importantData[2] = (chunks[i][j] + " "+ chunks[i][j+1] + " " + chunks[i][j+2] + chunks[i][j+3])
            
            if(chunks[i][j]) == "Thrust:":
                importantData[3] = (chunks[i][j] + " "+ chunks[i][j+1] + chunks[i][j+2])
                try:
                    importantData[8] = (float((chunks[i][j+1].replace(",", "")))) * 1000
                    importantData[8] = str(importantData[8]).replace('.','')
                except ValueError:
                    print("Error not Numer")
                    importantData[8] = 'error'
                
            
            if((chunks[i][j]) == "Specific") and ((chunks[i][j+1]) == "impulse:"):
                importantData[4] = (chunks[i][j] + " "+chunks[i][j+1] +" "+ chunks[i][j+2] + chunks[i][j+3])
            
            if((chunks[i][j]) == "Specific") and ((chunks[i][j+1]) == "impulse") and ((chunks[i][j+2]) == "sea") and ((chunks[i][j+3]) == "level:"):
                importantData[5] = (chunks[i][j] + " "+chunks[i][j+1] +" "+ chunks[i][j+2] + " "+chunks[i][j+3]  +" "+chunks[i][j+4] + chunks[i][j+5])

            if(chunks[i][j]) == "Diameter:":
                importantData[6] = (chunks[i][j] + " " +chunks[i][j+1] + chunks[i][j+2])


    if ((len(importantData[7]) > 0) and (len(importantData[8]) > 0)):
        print(importantData[8])
        print(importantData[7])
        importantData[9] = int(importantData[8])/int(importantData[7])  
        


    alphabet_string = string.ascii_uppercase
    alphabet_list = list(alphabet_string)

    for i in range(len(importantData)):
        currPlace = alphabet_list[i] + str(iterator)
        print(currPlace + "->"+ str(importantData[i]))
        worksheet.write(currPlace, str(importantData[i]))

    iterator = iterator + 1
    importantData = ["", "", "", "", "", "", "", "", "", ""] 


workbook.close()