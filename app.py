# import flask and its components
from flask  import *

#import pymysql module - It helps to create a connection between python flask and mysql database
import pymysql

#create a flask application and give it a name
app = Flask(__name__)

# Below is the sign up route
@app.route("/api/signup" , methods= ["POST"])
def signup():
    if request.method =="POST":
    #extract the different details entered on the phone
        username= request.form["username"]
        email =request.form["email"]
        password =request.form["password"]
        phone =request.form["phone"]

        # by use of the print function lets print all those details  sent with the upcoming request
        #print(username, email, password, phone)

    # establih a connection btwn flask/python and mysql
    connection =pymysql.connect(host="localhost", user="root", password="", database="sokogardenonline")

    #create a cursor to execute the sql queries
    cursor = connection.cursor()

    # structure an sql to insert the details received from the form
    # The %s is a placeholder -> it stands in places of actual values
    sql = "INSERT INTO users(username,email,phone,password) VALUES(%s,%s,%s,%s)"

    #create a tuple that will hold all the data content from the form
    data = (username, email,phone,password)

    # By use of the cursor execute the sql as you replace the placeholder with the actual values
    cursor.execute(sql,data)

    #commit the changes to the database
    connection.commit()

        
    return jsonify({"message" :"User registered successfully."})


#below is the login/sign in route
@app.route("/api/signin", methods=["POST"])
def signin():
    if request.method=="POST":
        #extract the two details entered on the form
        email = request.form["email"]
        password =request.form["password"]

        #print out the details entered
        #print(email, password)

        #create/establish a connection to the database
        connection =pymysql.connect(host="localhost", user="root", password="", database="sokogardenonline")

        #create a cursor
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        #structure the sql query that will check weather the email and the password entered are correct
        sql ="SELECT * FROM users WHERE email = %s AND password = %s"

        #put the data received from the form into a tuple
        data = (email, password)

        #by use of the cursor executs the tuple
        cursor.execute(sql,data)

        # Check whether the rows returned and store the same as variable
        count= cursor.rowcount

        #If there are records returned it means the password and the email are correct otherwise it means they are wrong
        if count==0:
            return jsonify({"message":" Login failed"})
        else:
            # There must be a user so we create avariable that will hold the details of the users fetched from the database
            user=cursor.fetchone()
            #return the deatials to the front end as well as the message
            return jsonify({"message": "User logged in successfully", "user":user})









#run the application
app.run(debug=True)