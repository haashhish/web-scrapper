#FOR EACH AD:
#------------
#class _261203a9 _2e82a662 returns an array. Seller name is in index 1. ->span
#class _59317dec fih details, description, extra features ->div
#class _676a547f fih details metrawa2a, use [arrayName].get_text(' ', strip=True). Keda el details mazbouta bel spaces. ->span
#class _0f86855a fih el description. ->div
#class _27f9c8ac fih el extra features ->span
#class _66b85548 fih el extra features 100% tamam. ->span
#class _1075545d d059c029 fih el ID/link of each user. ->div
#class _171225da has the ad ID. ->div
#To get location:
#location = currPage.find_all("span", class_="_8918c0a8")
    #print(location[0].get_text(' ', strip=True)+"\n")
#To get creation date:
#creationDate = currPage.find_all("span", class_="_8918c0a8")
    #print(location[1].get_text(' ', strip=True)+"\n")

#Date of joining olx:
#joinedDate = soup.find_all("span", class_= "_34a7409b")
#print(joinedDate[1].get_text(' ', strip=True))

#To get ad title:
'''try:
        title = currPage.find("h1", class_="a38b8112")
        print(title.get_text(' ', strip=True))
    except:
        title = "None"
'''

#For seller unique id/link:
'''
sellerID = soup.find_all("div", class_="_1075545d d059c029")
for data in sellerID:
    for link in data.find_all('a'):
        print(link['href'])
'''

#For seller name:
'''
sellerInfo = soup.find_all("span", class_="_261203a9 _2e82a662")
name = sellerInfo[1].text.strip()
'''


#TO GET ALL ADS:
#---------------
#class c46f3bfe returns an array of ads+info from the search/filtering page ->li


#To get all ads links from search/filter page:
#-----------------------------
#find_all("a", href=True)
#print(a['href'])



#To get all ads link from the search/filter results:
#---------------------------------------------------
#ads = soup2.find_all("li", class_="c46f3bfe")
#for ad in ads:
#    for a in ad.find_all('a'):
#        print(a['href'])
#

import requests
from bs4 import BeautifulSoup
counter = 1
while counter <= 85:
    startPage = "https://www.olx.com.eg/en/vehicles/cars-for-sale/cairo/?filter=new_used_eq_2%2Cyear_between_2000_to_2023"
    URL = "https://www.olx.com.eg/en/ad/%D8%B3%D9%83%D9%88%D8%AF%D8%A7-%D9%83%D9%88%D8%AF%D9%8A%D8%A7%D9%83-%D8%AF%D9%8A%D9%86%D8%A7%D9%85%D9%8A%D9%83-%D9%A5-%D8%B1%D8%A7%D9%83%D8%A8-%D8%AE%D9%84%D9%8A%D8%AC%D9%89-%D9%85%D9%88%D8%AF%D9%8A%D9%84-2021-%D9%88%D8%A7%D9%84%D8%B3%D8%B9%D8%B1-%D9%82%D8%A7%D8%A8%D9%84-%D9%84%D9%84%D8%AA%D9%81%D8%A7%D9%88%D8%B6-ID195093210.html"
    cont = "https://www.olx.com.eg/en/vehicles/cars-for-sale/cairo/?page="+str(counter)+"&filter=new_used_eq_2%2Cyear_between_2000_to_2023"
    page = requests.get(URL)
    if(counter == 1):
        print("Current Page: 1")
        page2 = requests.get(startPage)
    else:
        print("Current Page: "+ str(counter))
        page2 = requests.get(cont)

    soup = BeautifulSoup(page.content, "html.parser")
    soup2 = BeautifulSoup(page2.content, "html5lib")


    sellerInfo = soup.find_all("span", class_="_261203a9 _2e82a662")
    sellerID = soup.find_all("div", class_="_1075545d d059c029")
    '''for data in sellerID:
        for link in data.find_all('a'):
            print(link['href'])'''
    #name = sellerInfo[1].text.strip()
    #print(name)
    detailsOfCar = soup.find_all("div", class_="_676a547f")
    extraFeatures = soup.find_all("span", class_="_66b85548") #get extra features 100% great using text.strip()
    description = soup.find_all("div", class_="_0f86855a")
    allInfo = soup.find_all("div", class_="_59317dec")
    #joinedDate = soup.find_all("span", class_= "_34a7409b")
    #print(joinedDate[1].get_text(' ', strip=True))

    #for item in description:
        #print(item.get_text(' ', strip = True))

    arrayOfLinks = []
    finalLinks = []

    ads = soup2.find_all("li", class_="c46f3bfe")
    #for info in description:
    #    print(info.get_text(' ', strip=True))

    #for adName in ads:
        #print(adName.get_text(' ', strip = True))

    for ad in ads:
        for a in ad.find_all('a'):
            arrayOfLinks.append(a)

    for item in arrayOfLinks: #removing duplicates while preserving order of links with ads
            if item not in finalLinks:
                finalLinks.append(item)

    #for link in finalLinks:
        #print(link['href'])
    file = open("links.txt", "a",encoding='utf-8')
    for line in finalLinks:
        file.write(line['href'])
        file.write('\n')
    file.close()
    print("Page "+str(counter)+" is finished")
    counter = counter+1