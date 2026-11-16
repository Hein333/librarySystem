import os
from flask import Flask,render_template,request
import oracledb

app = Flask(__name__)
#Database Login#
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_DSN = os.environ.get("DB_DSN")


#connecting database and getting the datas
#database format (BOOKNAME,WRITERNAME,BOOKCODE)
def connectDatabase():
    try:
        with oracledb.connect(user=DB_USER,password=DB_PASSWORD,dsn = DB_DSN) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM bookdata")
                #get data from the database as list like this[(),(),()]
                rows = cursor.fetchall()
                print(rows)
                print(cursor)
                return rows

    except Exception as e:
        print(f"Database Error{e}",flush=True)

datalist = connectDatabase()

#MethodsUsedInWebPages

#checking the data and this function is shortened with the help of AI so I need to look into this very specifically
def check_field(value, datalist, column_index, field_name):
    # Extract the specific column values from the datalist
    column_list = [row[column_index] for row in datalist]
    
    if value in column_list:
        print(f"Your {field_name} is already in the database")
        return False
    else:
        print(f"{field_name} added successfully")
        return True

def checkTheDataInTheDatabase(BookName, WriterName, BookCode, datalist):
    # Check each piece of data using the helper function
    # Index 0 = BookName, Index 1 = WriterName, Index 2 = BookCode
    is_book_unique = check_field(BookName, datalist, 0, "BookName")
    is_writer_unique = check_field(WriterName, datalist, 1, "WriterName")
    is_code_unique = check_field(BookCode, datalist, 2, "BookCode")
    
    # Returns True  if one of the  items is unique
    return is_book_unique or is_writer_unique or is_code_unique
#the upper one need to be walk through again




def UserNameOrWriterNameOrBookCodeCheckInDatabase(BookName,WriterName,BookCode,datalist):
    result = False
    result = checkTheDataInTheDatabase(BookName,WriterName,BookCode,datalist)
    return result
           
def dataAnalysis(BookName,WriterName,BookCode,datalist):
    return UserNameOrWriterNameOrBookCodeCheckInDatabase(BookName,WriterName,BookCode,datalist)


#WebPagesManageMent
@app.route("/")
def home():
    return render_template("choose.html")


#updating books
@app.route("/BookUpdate",methods=["post"])
def BookUpdate():
    BookName = request.form["BookName"]
    WriterName = request.form["WriterName"]
    BookCode = request.form["BookCode"]
    #check the BookName,WriterName,BookCode in the database 
    checkOk = checkTheDataInTheDatabase(BookName,WriterName,BookCode,datalist)
    if checkOk:
        #update the database 
        try:
            with oracledb.connect(user=DB_USER,password=DB_PASSWORD,dsn = DB_DSN) as connection:
                with connection.cursor() as cursor:
                        sql = "INSERT INTO BOOKDATA(BookName,WriterName,BookCode) VALUES(:1,:2,:3)"
                        cursor.execute(sql, (BookName,WriterName,BookCode))
                        cursor.execute("COMMIT")
        
                        rows = cursor.fetchall()
                        return "book added into the database"
                           
        
        except Exception as e:
            print(f"Database Error{e}",flush=True)
            return "ERROR in the BookUpdate Function"
    else:
        return "The book is already in the database"
