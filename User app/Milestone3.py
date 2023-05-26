import mysql.connector
from tabulate import tabulate
import pandas as pd

def openConnection():
    print("Connecting to database...")
    mydb = mysql.connector.connect(
      host="db4free.net",
      port="3306",
      user="haashhish",
      password="databaseCourse2023",
      database="projectdb23"
      )
    print("Connected successfully!")
    return mydb

def topMakeModel():
    print("Provide year range: ")
    yearFrom = input("From: ")
    yearLimit = input("To: ")
    try:
        print("Checking make/models...")
        db = openConnection()
        cur = db.cursor()
        
        #for car make
        cur.execute("SELECT car_details.car_brand, COUNT(car_details.car_brand), AVG(car_details.price) from car_details inner join ad on ad.ad_id = car_details.car_id WHERE car_details.car_year >= "+yearFrom+" AND car_details.car_year <= "+yearLimit+" GROUP BY car_details.car_brand ORDER BY COUNT(car_details.car_brand) DESC LIMIT 5")
        result = cur.fetchall()
        print("\n")
        print("Top 5 car makes from year "+str(yearFrom)+" to year "+str(yearLimit)+":")
        print("----------------------------------------------------")
        for i in range(0,len(result)):
            print(str(i+1)+"- "+ result[i][0] + " with "+ str(result[i][1]) + " cars with average price: "+str(round(result[i][2], 3))+" LE.")

        #for car models
        cur.execute("SELECT car_details.car_model, COUNT(car_details.car_model), AVG(car_details.price) from car_details inner join ad on ad.ad_id = car_details.car_id WHERE car_details.car_year >= "+yearFrom+" AND car_details.car_year <= "+yearLimit+" GROUP BY car_details.car_model ORDER BY COUNT(car_details.car_model) DESC LIMIT 5")
        result = cur.fetchall()
        print("\n")
        print("Top 5 car models from year "+str(yearFrom)+" to year "+str(yearLimit)+":")
        print("-----------------------------------------------------")
        for i in range(0,len(result)):
            print(str(i+1)+"- "+ result[i][0] + " with "+ str(result[i][1]) + " cars with average price: "+str(round(result[i][2], 3))+" LE.")
        
        print("\n")
        db.close()
    except mysql.connector.Error:
        print("\nAn error has occured while connecting to the database\n")
        return

def showProperties():
    print("Enter user information:")
    print("-----------------------")
    print("Note: type NA in phone number IF NOT AVAILABLE!\n")
    name = input("Enter seller name: ")
    number = input("Enter phone number: ")
    result = []
    if(number == "na" or number == "NA"):
        try:
            print("Validating seller...")
            db = openConnection()
            cur = db.cursor()
            cur.execute("SELECT DISTINCT car_details.car_id, car_details.car_brand, car_details.car_model, car_details.price FROM ad INNER JOIN seller on ad.seller_name = seller.seller_name INNER JOIN car_details ON ad.ad_id = car_details.car_id WHERE seller.seller_name = '"+name+"'")
            result = cur.fetchall()
            db.close()
        except mysql.connector.Error as err:
            print("\nAn error has occured while connecting to the database\n")
            return
        if result == []:
            print("\nSeller not found!\n")
            return
        data = pd.DataFrame(result)
        print(tabulate(data, headers = 'keys', tablefmt = 'simple'))
        print("\n")

def topSellers():
    try:
        print("Checking sellers...")
        db = openConnection()
        cur = db.cursor()
        cur.execute("SELECT seller.seller_name, COUNT(seller.seller_url), AVG(car_details.price) from seller inner join ad on ad.seller_url = seller.seller_url INNER JOIN car_details ON ad.ad_id = car_id GROUP BY seller.seller_url ORDER BY COUNT(seller.seller_url) DESC LIMIT 5")
        result = cur.fetchall()
        print("\n")
        for i in range(0,len(result)):
            print(str(i+1)+"- "+ result[i][0] + " has "+ str(result[i][1]) + " ads with average price: "+str(round(result[i][2], 3))+" LE.")
        print("\n")
        db.close()
    except mysql.connector.Error:
        print("\nAn error has occured while connecting to the database\n")
        return

def topAreas():
    choice = ""
    print("Provide car make/model information:")
    print("-----------------------------------")
    print("Either enter car make OR model")
    print("1- Car make")
    print("2- Car model")
    while True:
        choice = input("Your choice:")
        if(choice == "1" or choice == "2"):
            break
        else:
            print("Enter a valid option, either 1 or 2")
            continue
    if(choice == "1"):
        carMake = input("Enter car make: ")
        try:
            print("Checking areas with the corresponding car make...")
            db = openConnection()
            cur = db.cursor()
            cur.execute("SELECT ad.area, COUNT(ad.area), car_details.car_brand, AVG(car_details.price) from car_details inner join ad on ad.ad_id = car_details.car_id WHERE ad.city = 'Cairo' AND car_details.car_brand = '"+carMake+"' GROUP BY ad.area, car_details.car_brand ORDER BY COUNT(ad.area) DESC LIMIT 5")
            result = cur.fetchall()
            if(result == []):
                print("\nNo car make is found!\n")
                return
            print("\n")
            for i in range(0,len(result)):
                print(str(i+1)+"- "+ result[i][0] + " with "+ str(result[i][1]) + " Ads, average price is: "+str(round(result[i][3], 3))+" LE.")
            print("\n")
            db.close()
        except mysql.connector.Error:
            print("\nAn error has occured while connecting to the database\n")
            return
    elif(choice == "2"):
        carModel = input("Enter car model: ")
        try:
            print("Checking areas with the corresponding car model...")
            db = openConnection()
            cur = db.cursor()
            cur.execute("SELECT ad.area, COUNT(ad.area), car_details.car_brand, AVG(car_details.price) from car_details inner join ad on ad.ad_id = car_details.car_id WHERE ad.city = 'Cairo' AND car_details.car_model = '"+carModel+"' GROUP BY ad.area, car_details.car_brand ORDER BY COUNT(ad.area) DESC LIMIT 5")
            result = cur.fetchall()
            if(result == []):
                print("\nNo car make is found!\n")
                return
            print("\n")
            for i in range(0,len(result)):
                print(str(i+1)+"- "+ result[i][0] + " with "+ str(result[i][1]) + " Ads, average price is: "+str(round(result[i][3], 3))+" LE.")
            print("\n")
            db.close()
        except mysql.connector.Error:
            print("\nAn error has occured while connecting to the database\n")
            return  

def showUsedCars():
    try:
        file = open("possibleFeatures.txt", "r")
        lines = file.readlines()
        file.close()
    except:
        print("possibleFeatures.txt is not found!")
        return
    print("Please provide the details of the Car")
    print("-------------------------------------")
    area = input("Area: ")
    city = input("City: ")
    priceFrom = input("Starting price: ")
    priceLimit = input("Price limit: ")
    print("Select features by entering index of desired features separated by comma!")
    for i in range(0, len(lines)):
        print(str(i+1) + "- " +lines[i])
    print("\n")
    print("Select features by entering index of desired features separated by comma!")
    selectedIndexes = input("Selected features: ")
    selectedIndexes = selectedIndexes.split(',')
    selectedFeatures = []
    for i in selectedIndexes:
        feature = lines[int(i)-1].replace('\n',"")
        selectedFeatures.append(feature)
    try:
        print("Searching for car...")
        db = openConnection()
        placeholders = ','.join(['%s'] * len(selectedFeatures))
        query = "SELECT DISTINCT car_details.* FROM car_details INNER JOIN car_features ON car_details.car_id = car_features.car_id INNER JOIN ad ON car_features.car_id = ad.ad_id AND ad.area = '"+area+"' AND ad.city = '"+city+"' AND car_details.price >= "+priceFrom+" AND car_details.price <= "+priceLimit+" AND car_details.car_condition = 'Used' AND car_features.car_feature IN ({});".format(placeholders)
        cur = db.cursor()
        cur.execute(query,tuple(selectedFeatures))
        result = cur.fetchall()
        data = pd.DataFrame(result)
        print(tabulate(data, headers = 'keys', tablefmt = 'simple'))
        db.close()
    except mysql.connector.Error as error:
        print("\nAn error has occured while connecting to the database\n")
        return

def showSpecificCar():
    result = []
    avg = 0
    print("Please provide the details of the Car")
    print("-------------------------------------")
    brand = input("Enter car brand: ")
    body_type = input("Enter body type: ")
    year = input("Manufacture year: ")
    area = input("Area: ")
    city = input("City: ")
    try:
        print("Searching for car...")
        db = openConnection()
        cur = db.cursor()
        cur.execute("SELECT car_model, AVG(car_details.price), Count(car_model) FROM car_details INNER JOIN ad ON car_details.car_id = ad.ad_id AND ad.area = '"+area+"' AND ad.city = '"+city+"' AND car_details.car_brand = '"+brand+"' AND car_details.body_type = '"+body_type+"' AND car_details.car_year = "+year+" GROUP BY car_details.car_model")
        result = cur.fetchall()
        db.close()
    except mysql.connector.Error:
        print("\nAn error has occured while connecting to the database\n")
        return
    if result == []:
        print("\nCar not found!\n")
        return
    print("\n")
    print("Result:")
    print("-------")
    for i in range(0,len(result)):
        print(str(i+1)+"- Car Model: "+ result[i][0] + " with a total number of: "+str(result[i][2])+" cars, with average price: "+str(round(result[i][1], 3))+" LE.")
    print("\n")

def viewSellerRating():
    sellerURL = input("Enter seller unique URL: ")
    result = []
    try:
        print("Validating Seller...")
        db = openConnection()
        cur = db.cursor()
        cur.execute("SELECT AVG(done_sale.rate), seller.seller_name FROM done_sale INNER JOIN ad on done_sale.ad_id = ad.ad_id INNER JOIN seller ON ad.seller_url = seller.seller_url WHERE seller.seller_url = '"+sellerURL+"';")
        result = cur.fetchall()
        db.close()
    except ConnectionError:
        print("\nAn error has occured while connecting to the database\n")
        return
    if result == []:
        print("\nNo ratings yet available for this seller!\n")
        return
    print("\nSeller name: "+ result[0][1] +"\nAverage rating: "+str(round(result[0][0], 3))+"\n")

def viewReviews():
    adID = input("Enter AD Reference ID: ")
    result = []
    try:
        print("Validating AD...")
        db = openConnection()
        cur = db.cursor()
        cur.execute("SELECT ad_id, review FROM done_sale WHERE ad_id = '"+adID+"'")
        result = cur.fetchall()
        db.close()
    except ConnectionError:
        print("\nAn error has occured while connecting to the database\n")
        return
    if result == []:
        print("\nAD not found!\n")
        return
    data = pd.DataFrame(result)
    print(tabulate(data, headers = 'keys', tablefmt = 'simple'))

def markSale():
    userEmail = input("Enter your email: ")
    result = []
    try:
        print("Validating user...")
        db = openConnection()
        cur = db.cursor()
        cur.execute("SELECT username FROM app_user WHERE email = '"+userEmail+"'")
        result = cur.fetchone()
        db.close()
    except mysql.connector.Error:
        print("\nAn error has occured while connecting to the database\n")
        return
    if result == []:
        print("\nUser not found!\n")
        return
    print("\nUsername: "+ result[0]+"\n")
    adID = input("AD Reference ID: ")
    try:
        print("Validating AD...")
        db = openConnection()
        cur = db.cursor()
        cur.execute("SELECT title from ad WHERE ad_id = '"+adID+"'")
        result = cur.fetchone()
        db.close()
    except ConnectionError:
        print("\nAn error has occured while connecting to the database\n")
        return
    if result == []:
        print("\nAd not found!\n")
        return
    print("\nAD Title: "+ result[0]+"\n")
    sellingPrice = input("Selling price: ")
    review = input("Write your review: ")
    rating = ""
    while True:
        rating = input("Rate the purchase: (1 to 5): ")
        if(int(rating) <= 5 and int(rating) >= 1):
            break
        else:
            print("Please enter a valid rating from 1 to 5")
            continue
    try:
        db = openConnection()
        mycursor = db.cursor()
        sql = "INSERT INTO done_sale (user_email, ad_id, price, review, rate) VALUES (%s, %s, %s, %s, %s)"
        val = (userEmail, adID, sellingPrice, review, rating)
        mycursor.execute(sql, val)
        db.commit()
        db.close()
        print("\nSale is marked done successfully!\n")
    except ConnectionError:
        print("\nAn error has occured while connecting to the database\n")

def createUser():
    print("Fill the required fields")
    print("-------------------------")
    username = input("Username: ")
    email = input("E-mail: ")
    name = input("Name: ")
    gender = input("Gender: ")
    b_date = input("Birthdate (YYYY-MM-DD): ")
    try:
        db = openConnection()
        mycursor = db.cursor()
        sql = "INSERT INTO app_user (username, email, name, gender, birthDate) VALUES (%s, %s, %s, %s, %s)"
        val = (username, email, name, gender, b_date)
        mycursor.execute(sql, val)
        db.commit()
        db.close()
        print("\nUser created successfully!\n")
    except ConnectionError:
        print("\nAn error has occured while connecting to the database\n")
    except:
        print("\nUser already exists!\n")

print("Welcome to car marketplace!")
print("---------------------------")
while True:
    print("Main Menu")
    print("----------")
    print("1- Register a new user")
    print("2- Mark a sale")
    print("3- View reviews of a specific AD")
    print("4- View average rating of a seller")
    print("5- Search for car in specific area")
    print("6- Show used cars in specific areas with features")
    print("7- Show top 5 areas in Cairo")
    print("8- Show top 5 sellers")
    print("9- Show all properties of a seller")
    print("10- Show top 5 make/models and average price for a year range")
    print("11- Exit")
    choice = input("Your choice: ")
    if(choice == "1"):
        createUser()
    elif(choice == "2"):
        markSale()
    elif(choice == "3"):
        viewReviews()
    elif(choice == "4"):
        viewSellerRating()
    elif(choice == "5"):
        showSpecificCar()
    elif(choice == "6"):
        showUsedCars()
    elif(choice == "7"):
        topAreas()
    elif(choice == "8"):
        topSellers()
    elif(choice == "9"):
        showProperties()
    elif(choice == "10"):
        topMakeModel()
    elif(choice == "11"):
        exit()
    else:
        print("\nEnter a valid choice\n")