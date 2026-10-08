from flask import Flask, jsonify
from db import init_db, get_db_conn
from utils.utils import ApiError, error_handler
from routes.users import users_bp

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

app.register_blueprint(users_bp)

@app.errorhandler(ApiError)
def handle_api_error(error):
    return error_handler(
        error.message,
        error.status_code,
        error.errors
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)