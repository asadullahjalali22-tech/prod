from flask import Flask , jsonify

import mysql.connector

import os

app =Flask(__name__)

def get_db_connection():
	return mysql.connector.connect(
		host=os.getenv("DB_HOST", "mysql"),
		user=os.getenv("DB_USER", "root"),
		password=os.getenv("DB_PASSWORD", "prod123"),
		database=os.getenv("DB_NAME", "prod"),
		)
@app.route("/")
def home():
	return "prod is now live"
@app.route("/health")
def health():
	return "ok"
@app.route("/products")
def products():
	try:
		conn = get_db_connection()
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM products;")
		result = cursor.fetchall()
		products_list = []
		for row in result:
			products_list.append({
				"id": row[0],
				"name": row[1],
				"price": float(row[2])

				})

		cursor.close()
		conn.close()
		return jsonify (products_list)
	except Exception as e:
		return str(e) , 500

@app.route("/db")
def db():
	try:
		conn = get_db_connection()
		cursor = conn.cursor()
		cursor.execute("SELECT DATABASE();")
		result = cursor.fetchone()



		cursor.close()
		conn.close()
		return f"connected to database{result[0]}"
	except Exception as e:
		return str(e)
if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000)
