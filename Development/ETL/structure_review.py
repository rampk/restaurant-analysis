# Importing required libraries
import multiprocessing
from pymongo import MongoClient
import mysql.connector

# Processes running on parallel
def process_cursor(skip_n,limit_n):

    print('Starting process',skip_n//limit_n,'...')
    # Connect to the MongoDB
    collection = MongoClient().yelp_review.review_data
    cursor = collection.find({}).skip(skip_n).limit(limit_n)
 
    # Connect to the MySQL
    mydb = mysql.connector.connect(user='db_user',
                                   password='P@s$w0rd123!',
                                   database='yelp_review')
    mycursor = mydb.cursor()

    # Insert query
    sql = 'INSERT INTO review (review_id, business_id, text, stars) VALUES (%s, %s, %s, %s)'

    # Loop through the cursor
    for doc in cursor:
        # Insert values from MongoDB to MySQL
        val = (doc['review_id'], doc['business_id'], doc['text'], doc['stars'])
        mycursor.execute(sql, val)
        mydb.commit()

    print('Completed process',skip_n//limit_n,'...')


if __name__ == '__main__':
    n_cores = 4
    collection_size = 8635403 
    # Size of batches
    batch_size = round(collection_size/n_cores+0.5)
    # Generator to skip the cursors 
    skips = range(0, n_cores*batch_size, batch_size)

    # Creating multiple process to run on parallel
    processes = [ multiprocessing.Process(target=process_cursor, args=(skip_n,batch_size)) for skip_n in skips]

    for process in processes:
        process.start()

    for process in processes:
        process.join()
