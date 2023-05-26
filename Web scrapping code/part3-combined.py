from faker import Faker
import random

generator = Faker()

name = ""
username = ""
email = ""
b_date = ""
gender = ""
review = ""
adIDs = [196177476, 196532831, 196155871, 194426965, 195996251,196472402, 196538066, 196541431, 196511758, 196496996] #any selected ad IDs

for i in range(1,500):
    name = generator.name()
    username = generator.user_name()
    email = generator.email()
    b_date = generator.date()
    value  = random.randint(0,1)
    if value == 1:
        gender = "M"
    else:
        gender = "F"
    price = random.randint(200000, 1500000)
    review = generator.text()
    rate = random.randint(1,5)
    randIndex = random.randint(0,9) #choose random index from 0 to 9
    adID = adIDs[randIndex]
    file = open("fakeDataLatest.csv","a")
    file.write(username+","+email+","+name+","+gender+","+b_date+"\n")
    file.close()
    file = open("fakeSalesLatest.csv","a")
    file.write(email+","+str(adID)+","+str(price)+","+'"'+review+'"'+","+str(rate)+"\n")
    file.close()