import requests
import csv
import time
from bs4 import BeautifulSoup
import pandas
import random

file = open("links-new.txt", "r")
lines = file.readlines()
file.close()
counter = 1
for line in lines:
    print("Parsing ad no. "+str(counter))
    url = "https://www.olx.com.eg"+line
    webpage = requests.get(url)
    currPage = BeautifulSoup(webpage.content, "html5lib")
    name = ""
    sellerInfo = currPage.find_all("span", class_="_261203a9 _2e82a662")
    try:
        name = sellerInfo[1].text.strip()
        print(name)
    except:
        print("Cannot get name")
        name = "ERROR"
    print("Working on URl: "+url)
    sellerFinalID = ""
    sellerID = currPage.find_all("div", class_="_1075545d d059c029")
    for data in sellerID:
        for link in data.find_all('a'):
            sellerFinalID = link['href']
    print("Seller link: "+sellerFinalID)
    title = ""
    try:
        title = currPage.find("h1", class_="a38b8112")
        print("Title of ad is: "+title.get_text(' ', strip=True))
    except:
        title = "ERROR_In_Title" #title = none in case no title is found
    detailsOfCar = currPage.find_all("div", class_="b44ca0b3") ##needs to be split
    print("data lengthh: "+str(len(detailsOfCar)))
    carBrand = ""
    carModel = ""
    adType = ""
    fuelType = ""
    carPrice = ""
    priceType = ""
    paymentOptions = ""
    carYear = ""
    kilometers = ""
    kilometersSplit = []
    transmissionType = ""
    carCondition = ""
    carColor = ""
    bodyType = ""
    engineCC = ""
    engineCCSplit = []
    engineFrom = ""
    engineTo = ""
    engineFlag = 0
    video = ""
    virtualTour = ""

    for i in detailsOfCar:
        if "Brand" in i.get_text(' ', strip=True):
            carBrand = i.contents[1].get_text(' ', strip=True)
        elif "Model" in i.get_text(' ', strip=True):
            carModel = i.contents[1].get_text(' ', strip=True)
        elif "Ad Type" in i.get_text(' ', strip=True):
            adType = i.contents[1].get_text(' ', strip=True)
        elif "Fuel Type" in i.get_text(' ', strip=True):
            fuelType = i.contents[1].get_text(' ', strip=True)
        elif "Price Type" in i.get_text(' ', strip=True):
            priceType = i.contents[1].get_text(' ', strip=True)
        elif "Price" in i.get_text(' ', strip=True):
            carPrice = i.contents[1].get_text(' ', strip=True)
            print(carPrice)
        elif "Payment Options" in i.get_text(' ', strip=True):
            paymentOptions = i.contents[1].get_text(' ', strip=True)
        elif "Year" in i.get_text(' ', strip=True):
            carYear = i.contents[1].get_text(' ', strip=True)
        elif "Kilometers" in i.get_text(' ', strip=True):
            kilometers = i.contents[1].get_text(' ', strip=True)
            kilometersSplit = kilometers.split("to")
        elif "Transmission Type" in i.get_text(' ', strip=True):
            transmissionType = i.contents[1].get_text(' ', strip=True)
        elif "Condition" in i.get_text(' ', strip=True):
            carCondition = i.contents[1].get_text(' ', strip=True)
        elif "Color" in i.get_text(' ', strip=True):
            carColor = i.contents[1].get_text(' ', strip=True)
        elif "Body Type" in i.get_text(' ', strip=True):
            bodyType = i.contents[1].get_text(' ', strip=True)
        elif "Engine Capacity (CC)" in i.get_text(' ', strip=True):
            engineCC = i.contents[1].get_text(' ', strip=True)
            engineCCSplit = engineCC.split("-")
            engineFlag = 0 #if 0, we have 2 values, otherwise: we have 1 value only
            try:
                engineFrom = engineCCSplit[0]
                engineTo = engineCCSplit[1]
            except:
                engineFlag = 1
        elif "Video" in i.get_text(' ', strip=True):
            video = i.contents[1].get_text(' ', strip=True)
        elif "Virtual Tour" in i.get_text(' ', strip=True):
            virtualTour = i.contents[1].get_text(' ', strip=True)
    extraFeatures = currPage.find_all("span", class_="_66b85548") #get extra features 100% great using text.strip()
    description = currPage.find_all("div", class_="_0f86855a")
    #adID = ""
    adIDSplit = []
    adIDFinal = ""
    adID = currPage.find("div", class_="_171225da")
    print(adID.get_text(' ',strip=True))
    adIDSplit = adID.get_text(' ', strip=True).split(" ")
    adIDFinal = adIDSplit[2]
    area = ""
    city = ""
    location = currPage.find_all("span", class_="_8918c0a8")
    creationDate = currPage.find_all("span", class_="_8918c0a8")
    joinedDate = currPage.find_all("span", class_= "_34a7409b")
    #print(location[0].get_text(' ', strip=True))
    location = location[0].get_text(' ', strip=True)
    finalLocation = location.split(", ")
    try:
        area = finalLocation[0]
        city = finalLocation[1]
    except:
        print("No location")
    print("Area: "+area)
    print("City: "+city)
    print(creationDate[1].get_text(' ', strip=True))
    date = joinedDate[1].get_text(' ', strip=True)
    keyword = "Commercial"
    if keyword in date:
        date = joinedDate[2].get_text(' ', strip=True) #to handle commercial ID which is displayed rather than the "Member Since" part
    print(date)
    try:
        print(adID.get_text(' ', strip=True))
    except:
        adID = "ErrorInAD_iD"

    #write in csv files
    file = open('seller.csv', 'a', encoding='utf-8-sig') #seller table
    file.write(sellerFinalID+",")
    file.write(name+",")
    file.write(date)
    file.write('\n')
    file.close()

    file = open('ad.csv', 'a', encoding='utf-8-sig') #ad table
    file.write(adIDFinal+",")
    file.write(sellerFinalID+",")
    file.write(name+",")
    file.write('"'+title.get_text(' ', strip=True)+'"'+",")
    file.write(location+",")
    file.write(adType+",")
    file.write(creationDate[1].get_text(' ', strip=True))
    file.write('\n')
    file.close()

    function = [{"ad_id": adIDFinal, "description":description[0].get_text(' ', strip=True)}]
    table = pandas.DataFrame(function)
    table.to_csv("carDesc.csv", sep = ',', encoding = 'UTF-8-sig', mode='a', index = False, header = False)

    file = open('car.csv', 'a', encoding='utf-8-sig') #car table
    file.write(adIDFinal+",")
    file.write(carBrand+",")
    file.write(carModel+",")
    file.write(adType+",")
    file.write(fuelType+",")
    file.write('"'+carPrice+'"'+",")
    file.write(priceType+",")
    file.write(paymentOptions+",")
    file.write(carYear+",")
    file.write(transmissionType+",")
    file.write(carCondition+",")
    file.write(carColor+",")
    if len(kilometersSplit) == 1:
        file.write(kilometersSplit[0]+",")
        file.write(" ")
        file.write(",")
    else:
        file.write(kilometersSplit[0]+",")
        file.write(kilometersSplit[1]+",")
    if engineFlag == 0:
        file.write(engineFrom+",")
        file.write(engineTo+",")
    else:
        file.write(engineFrom+",")
        file.write(" ")
        file.write(",")
    file.write(bodyType+",")
    file.write(video+",")
    file.write(virtualTour+",")
    file.write('\n')
    file.close()

    file = open('extraFeatures.csv', 'a', encoding='utf-8-sig') #extra features table
    if len(extraFeatures) != 0:
        for i in extraFeatures:
            file.write(adIDFinal+",")
            file.write(i.get_text(' ', strip=True))
            file.write("\n")
    file.close()

    #OLD Functions
    '''file = open('KMs.csv', 'a', encoding='utf-8-sig') #kilometers table
    file.write(adIDFinal+",")
    if len(kilometersSplit) == 1:
        file.write(kilometersSplit[0])
        file.write("\n")
    else:
        file.write(kilometersSplit[0]+",")
        file.write(kilometersSplit[1])
        file.write("\n")
    file.close()'''

    '''file = open('engineCC.csv', 'a', encoding='utf-8-sig') #engine CC table
    file.write(adIDFinal+",")
    if engineFlag == 0:
        file.write(engineFrom+",")
        file.write(engineTo)
        file.write("\n")
    else:
        file.write(engineFrom)
        file.write("\n")
    file.close()'''

    '''file = open('newDescr.csv', 'a', encoding='utf-8-sig') #description table
    file.write(adIDFinal+",")
    file.write('"'+description[0].text+'"')
    file.write('\n')
    file.close()'''
    print("Finished parsing ad no. "+str(counter))
    counter = counter + 1
