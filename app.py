import sqlite3, os, requests
from flask import Flask, jsonify, render_template, request, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/mycloset")
def my_closet():
    return render_template("my_closet.html")

#Purpose: selects all clothing from closet_list.db based on type
#Param: type(string)
#Return: clothing object properties
@app.route("/clothing/search/type")
def search_clothing_type():
    type_param = request.args.get("type")
    if not type_param:
        return jsonify({"error": "Missing type_param"})
    print(f"Recieved type: {type_param}")
    query = "SELECT id,name,img_path FROM closet WHERE type = ?"
    params = (type_param)

    try:
        conn = sqlite3.connect("closet_list.db")
        cursor = conn.cursor()
        result = cursor.execute(query, params).fetchall()
        conn.close()
        print(f"Query result: {result}")
        if not result:
            return jsonify({"error" : "no clothing found"})
        
        clothing_list = [
            {"id":row[0],"name": row[1], "path": row[2]}
            for row in result
        ]
        return jsonify(clothing_list)
    except Exception as e:
        return jsonify({"error": "error searching closet_list.db"})

#Purpose: selects a clothing from closet_list.db
#Param: type(string) (optional: weather(string))
#Return: clothing object properties
@app.route("/clothing/search/weather")
def search_clothing_weather():
    type_param = request.args.get("type")
    if not type_param:
        return jsonify({"error": "Missing type_param or weather_param"})
    query = "SELECT id,name,img_path FROM closet WHERE type = :type"
    params = {"type": type_param}

    weather_param = request.args.get("weather")
    if weather_param:
        query += " AND (weather = :weather OR weather = 'ALL')"
        params["weather"] = weather_param 

    query += " ORDER BY RANDOM() LIMIT 1"
    
    try:
        conn = sqlite3.connect("closet_list.db")
        cursor = conn.cursor()
        result = cursor.execute(query, params).fetchone()
        conn.close()

        print(f"Query result: {result}")
        if not result:
            return jsonify({"error" : "no clothing found"})
        clothing_id, clothing_name,clothing_path = result
        print(f"Id: {clothing_id} |Name: {clothing_name} | Path: {clothing_path}")
        return jsonify({"id": clothing_id,"name" : clothing_name,"path": clothing_path})
    except Exception as e:
        return jsonify({"error": "error searching closet_list.db"})
    
#Purpose:connects to OpenWeather API to get the temperature
#Param: (lat(int) & lon(int)) OR (zipcode(int))
#Return: Temp(int) in F
@app.route("/weather/get")
def get_temperature():
    #weather_api_key = os.getenv("OPENWEATHER_API_KEY")
    #demo key from publicly provided by geeksforgeeks is used so
    #i can publicly share this project without making other require .env
    weather_api_key = "6d055e39ee237af35ca066f35474e9df"
    lat_coord = request.args.get("lat")
    lon_coord = request.args.get("lon")
    zipcode = request.args.get("zipcode")

    if lat_coord and lon_coord:
        url = (f"https://api.openweathermap.org/data/2.5/weather?"
            f"lat={lat_coord}&lon={lon_coord}&appid={weather_api_key}&units=imperial")
        print(f"Recieved lat: {lat_coord}, lon: {lon_coord}")
    elif zipcode:
        url = (f"https://api.openweathermap.org/data/2.5/weather?"
            f"zip=29607&appid={weather_api_key}&units=imperial")
        print(f"Recieved zipcde:{zipcode}")
    else:
        return jsonify({"error": "Must provide lat/lon or zipcode"})

    try:
        response  = requests.get(url,timeout = 5)
        if response.status_code == 200:
            result = response.json()
            return jsonify({"temp": result["main"]["feels_like"]})
        else: 
            return jsonify({"error": f"Openweather returned: {response.status_code}"})
    except Exception as e:
        return jsonify({"error": "error fetching data from OpenWeather API"})

if __name__ == '__main__':
    app.run(debug=True)