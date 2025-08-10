import sqlite3
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/clothing/search")
def search_clothing():
    type_param = request.args.get("type")
    weather_param = request.args.get("weather")
    print(f"Recieved type: {type_param}, weather:{weather_param}")
    #print("hello world")
    query = "SELECT id,img_path FROM closet WHERE type = ? AND weather = ? LIMIT 1"
    params = (type_param,weather_param)

    try:
        conn = sqlite3.connect("closet_list.db")
        cursor = conn.cursor()
        result = cursor.execute(query, params).fetchone()
        conn.close()

        print(f"Query result: {result}")
        #print("hello world")
        if not result:
            return jsonify({"error" : "no clothing found"})
        clothing_id, clothing_path = result
        print(f"Id: {clothing_id}")
        return jsonify({"id": clothing_id})
    except Exception as e:
        return jsonify({"error": "error searching closet_list.db"})
    


if __name__ == '__main__':
    app.run(debug=True)