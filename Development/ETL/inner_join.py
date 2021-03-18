import mysql.connector
mydb1 = mysql.connector.connect(user='db_user',
                               password='P@s$w0rd123!',
                               database='yelp_review')
mydb2 = mysql.connector.connect(user='db_user',
                               password='P@s$w0rd123!',
                               database='yelp_review')
mycursor1 = mydb1.cursor()
mycursor2 = mydb2.cursor()
#mycursor.execute('select * from business limit 5')
mycursor1.execute('SELECT b.business_id,b.name,b.city,r.review_id,r.text,r.stars FROM business b INNER JOIN review r ON b.business_id=r.business_id')

i = 0
for business_id,name,city,review_id,text,stars in mycursor1:
    values = (business_id,name,city,review_id,text,stars)
    query = 'INSERT INTO restaurant VALUES(%s,%s,%s,%s,%s,%s)'
    mycursor2.execute(query,values)
    mydb2.commit()
    
    i += 1

    if i %10000 == 0:
        print(f'Inserted {i} rows')
