# import flask and its components
from flask import Flask, request, jsonify
import os
from flask_cors import CORS
import pymysql

# create flask app
app = Flask(__name__)
CORS(app)

app.config["UPLOAD_FOLDER"] = "static/images"


# =========================
# SIGN UP
# =========================
@app.route("/api/signup", methods=["POST"])
def signup():
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    phone = request.form["phone"]

    connection = pymysql.connect(
        host="mysql-ramogi-web.alwaysdata.net",
        user="ramogi-web",
        password="modcom1234",
        database="ramogi-web_sokogarden"
    )

    cursor = connection.cursor()

    sql = "INSERT INTO users(username,email,phone,password) VALUES(%s,%s,%s,%s)"
    data = (username, email, phone, password)

    cursor.execute(sql, data)
    connection.commit()

    return jsonify({"message": "User registered successfully"})


# =========================
# SIGN IN
# =========================
@app.route("/api/signin", methods=["POST"])
def signin():
    email = request.form["email"]
    password = request.form["password"]

    connection = pymysql.connect(
        host="mysql-ramogi-web.alwaysdata.net",
        user="ramogi-web",
        password="modcom1234",
        database="ramogi-web_sokogarden"
    )

    cursor = connection.cursor(pymysql.cursors.DictCursor)

    sql = "SELECT * FROM users WHERE email=%s AND password=%s"
    data = (email, password)

    cursor.execute(sql, data)

    if cursor.rowcount == 0:
        return jsonify({"message": "Login failed"})
    else:
        user = cursor.fetchone()
        return jsonify({"message": "Login successful", "user": user})


# =========================
# ADD PRODUCT
# =========================
@app.route("/api/add_product", methods=["POST"])
def add_product():

    product_name = request.form["product_name"]
    product_description = request.form["product_description"]
    product_cost = request.form["product_cost"]
    product_photo = request.files["product_photo"]

    filename = product_photo.filename
    photo_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    product_photo.save(photo_path)

    connection = pymysql.connect(
        host="mysql-ramogi-web.alwaysdata.net",
        user="ramogi-web",
        password="modcom1234",
        database="ramogi-web_sokogarden"
    )

    cursor = connection.cursor()

    sql = """
    INSERT INTO product_details(product_name, product_description, product_cost, product_photo)
    VALUES (%s, %s, %s, %s)
    """

    data = (product_name, product_description, product_cost, filename)

    cursor.execute(sql, data)
    connection.commit()

    return jsonify({"message": "Product added successfully"})


# =========================
# GET PRODUCTS
# =========================
@app.route("/api/get_products")
def get_products():

    connection = pymysql.connect(
        host="mysql-ramogi-web.alwaysdata.net",
        user="ramogi-web",
        password="modcom1234",
        database="ramogi-web_sokogarden"
    )

    cursor = connection.cursor(pymysql.cursors.DictCursor)

    cursor.execute("SELECT * FROM product_details")
    products = cursor.fetchall()

    return jsonify(products)


# =========================
# M-PESA PAYMENT
# =========================
import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth


@app.route('/api/mpesa_payment', methods=['POST'])
def mpesa_payment():

    amount = request.form['amount']
    phone = request.form['phone']

    consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
    consumer_secret = "amFbAoUByPV2rM5A"

    api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    data = r.json()

    access_token = "Bearer " + data['access_token']

    timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
    passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
    business_short_code = "174379"

    password_str = business_short_code + passkey + timestamp
    password = base64.b64encode(password_str.encode()).decode('utf-8')

    payload = {
        "BusinessShortCode": business_short_code,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": business_short_code,
        "PhoneNumber": phone,
        "CallBackURL": "https://modcom.co.ke/api/confirmation.php",
        "AccountReference": "account",
        "TransactionDesc": "payment"
    }

    headers = {
        "Authorization": access_token,
        "Content-Type": "application/json"
    }

    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    response = requests.post(url, json=payload, headers=headers)

    return jsonify({"message": "Check your phone to complete payment"})


# =========================
# CONTACT US (NEW FIXED API)
# =========================
@app.route("/api/contact", methods=["POST"])
def contact():
    try:
        name = request.form["name"]
        email = request.form["email"]
        subject = request.form["subject"]
        message = request.form["message"]

        connection = pymysql.connect(
            host="mysql-ramogi-web.alwaysdata.net",
            user="ramogi-web",
            password="modcom1234",
            database="ramogi-web_sokogarden"
        )

        cursor = connection.cursor()

        sql = """
        INSERT INTO contact_messages(name, email, subject, message)
        VALUES (%s, %s, %s, %s)
        """

        data = (name, email, subject, message)

        cursor.execute(sql, data)
        connection.commit()

        return jsonify({"message": "Message sent successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# RUN APP (IMPORTANT FOR LOCAL ONLY)
# =========================
# app.run(debug=True)