from flask import Flask, jsonify
from db import init_db, get_db_conn

app = Flask(__name__)

init_db()

@app.route('/health', methods=['GET'])
def health_check():
    try:
        with get_db_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT 1;')
                output  = cursor.fetchone()
                print(f"output: {output}")
                return jsonify({"status": "healthy", "database":"connected"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "unhealthy", "error": "Something is wrong. Please check logs"}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)