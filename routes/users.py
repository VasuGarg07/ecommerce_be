from flask import Blueprint, request

from repositories.users_repo import create_user, get_single_user_details, get_users_list, toggle_user_active_status
from utils.utils import success_handler, ApiError

users_bp = Blueprint('users_bp', __name__)

@users_bp.route("/users", methods=['POST'])
def create_new_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    role = data.get('role')

    try:
        new_user_id = create_user(name, email, phone, role)
        return success_handler({"id": new_user_id}, message="User Created", status_code=201)
    except Exception as e:
        raise ApiError(str(e), 500)

@users_bp.route("/users", methods=['GET'])
def get_users():
    role = request.args.get('role')
    page_num = request.args.get('page_num')
    page_size = request.args.get('page_size')

    try:
        users = get_users_list(page_num, page_size, role)
        return success_handler(users)
    except Exception as e:
        raise ApiError(str(e), 500)

@users_bp.route("/users/<int:user_id>", methods=['GET'])
def get_user_details(user_id):
    try:
        user = get_single_user_details(user_id)
        return success_handler(user)
    except Exception as e:
        raise ApiError(str(e), 500)

@users_bp.route("/users/<int:user_id>", methods=['PATCH'])
def get_user_details(user_id):
    try:
        user = toggle_user_active_status(user_id)
        return success_handler(user, message="User Status Changed.")
    except Exception as e:
        raise ApiError(str(e), 500)