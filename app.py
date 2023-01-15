from flask import *
from mysql.connector.pooling import MySQLConnectionPool
import boto3
import os
from dotenv import load_dotenv
from mysql.connector import Error
import uuid

load_dotenv()

app = Flask(__name__, static_folder="static", static_url_path="/static")

pool = MySQLConnectionPool(
    pool_name = "pooling",
    pool_size = 10,
    pool_reset_session = True,
    host = os.getenv("host"),
    user = os.getenv("user"),
    password = os.getenv("password"),
    database = os.getenv("database")
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/headshot", methods=["GET", "POST"])
def upload_headshot():
    try:
        connection_object = pool.get_connection()
        cursor = connection_object.cursor(buffered = True, dictionary = True)
        client = boto3.client(
            "s3",
            region_name = os.getenv("AWS_REGION_NAME"),
            aws_access_key_id = os.getenv("AWS_ACCESS_KEY_id"),
            aws_secret_access_key = os.getenv("AWS_SCREAT_KEY")
        )
        BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
        file = request.files.get("headshot")
        if request.method == "GET":
            cursor.execute("SELECT * FROM `data`;")
            cur = cursor.fetchall()
            photo_list=[]
            if cur:
                for detail in cur:
                    photo_list.append({
                        "text": detail["description"],
                        "photo": detail["images"]
                    })
                return jsonify({"data": photo_list})
            else:
                return jsonify({"data": None})

        if request.method == "POST":
            text = request.form["word"]
            if file is None:
                return jsonify({
                    "error": True,
                    "message": "請選擇要上傳的圖片"
                })
            if text is None:
                return jsonify({
                    "error": True,
                    "message": "請輸入訊息文字"
                })
            file_name = str(uuid.uuid4())
            client.upload_fileobj(
                file,
                BUCKET_NAME,
                file_name
            )
            cursor.execute("INSERT INTO `data` (`images`, `description`) VALUES (%s, %s);",[file_name, text])
            connection_object.commit()
            return jsonify({
                "text": text,
                "photo": file_name
            })

    except Error as e:
        print("Error", e)
        return jsonify({
            "error": True,
            "message": "伺服器內部錯誤"
        }),500

    finally:
        if (connection_object.is_connected()):
            cursor.close()
            connection_object.close()

app.run(host="0.0.0.0", port=5000, debug=True)