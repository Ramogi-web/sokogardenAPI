# import flask and its components
from flask  import *
import os

#import pymysql module - It helps to create a connection between python flask and mysql database
import pymysql

#create a flask application and give it a name
app = Flask(__name__)

#configure the location to where your products images will be saved on you app
app.config["UPLOAD_FOLDER"] ="static/images"

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

#Below is the route for adding products
@app.route ("/api/add_product", methods=["POST"])
def Addproducts():
    if request.method=="POST":
        #extract the data entered from the phone
        product_name = request.form["product_name"]
        product_description =request.form["product_description"]
        product_cost = request.form["product_cost"]
        # for the product photo ,we shall fetch it from files as showm below
        product_photo = request.files["product_photo"]

        #extract the filename of the product photo
        filename= product_photo.filename

        #by use of the OS module ,we can extract the path where the image is currently saved
        photo_path = os.path.join(app.config["UPLOAD_FOLDER"],filename)

        #save the product photo image into the new location
        product_photo.save(photo_path)
        


        #print them out to test whether you are receiving the details
       # print(product_name,product_description,product_cost) 
        connection =pymysql.connect(host="localhost", user="root",password="", database="sokogardenonline")

        #create a cursor to execute the sql queries
        cursor = connection.cursor()

        # structure an sql to insert the product details in the database 
        # The %s is a placeholder -> it stands in places of actual values
        sql="INSERT INTO product_details(product_name, product_description, product_cost, product_photo) VALUES (%s, %s, %s, %s)"

        #create a tuple that will hold all the data content from the form
        data=(product_name, product_description,product_cost, filename)

        # use the cursor to execute the sqlas you replace the placeholders with the actual data
        cursor.execute(sql,data)

        #commit the changes to the database
        connection.commit()


        return jsonify({"message":"product added successfully"})









#run the application
app.run(debug=True)