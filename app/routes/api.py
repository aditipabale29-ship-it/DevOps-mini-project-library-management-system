from flask import Blueprint, jsonify, request

from app.services.library_service import LibraryService

api = Blueprint("api", __name__, url_prefix="/api")
library = LibraryService()


@api.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


@api.route("/dashboard", methods=["GET"])
def dashboard():
    return jsonify({
        "total_books": len(library.books),
        "total_users": len(library.users),
        "total_loans": len(library.loans)
    })


@api.route("/books", methods=["GET"])
def get_books():
    return jsonify(library.list_books())


@api.route("/books", methods=["POST"])
def add_book():
    data = request.get_json(silent=True) or {}

    if not all(data.get(key) for key in ("title", "author", "isbn")):
        return jsonify({"error": "Title, author and ISBN are required"}), 400

    try:
        copies = int(data.get("copies", 1))
        if copies < 1:
            raise ValueError
    except (TypeError, ValueError):
        return jsonify({"error": "Copies must be a positive integer"}), 400

    book = library.add_book(
        data["title"], data["author"], data["isbn"], copies
    )
    return jsonify(book), 201


@api.route("/users", methods=["GET"])
def get_users():
    return jsonify(library.list_users())


@api.route("/users", methods=["POST"])
def add_user():
    data = request.get_json(silent=True) or {}

    if not data.get("name") or not data.get("email"):
        return jsonify({"error": "Name and email are required"}), 400

    user = library.add_user(
        data["name"], data["email"], data.get("role", "Student")
    )
    return jsonify(user), 201


@api.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = library.users.get(user_id)

    if user is None:
        return jsonify({"error": "User not found"}), 404

    if user.active_loans > 0:
        return jsonify({"error": "User has active loans"}), 400

    del library.users[user_id]
    return jsonify({"message": "User deleted successfully"})


@api.route("/loans", methods=["GET"])
def get_loans():
    return jsonify(library.list_loans())


@api.route("/borrow", methods=["POST"])
def borrow_book():
    data = request.get_json(silent=True) or {}

    try:
        book_id = int(data["book_id"])
        user_id = int(data["user_id"])
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Valid book_id and user_id are required"}), 400

    result = library.borrow_book(book_id, user_id)

    if "error" in result:
        return jsonify(result), 400

    return jsonify(result), 201


@api.route("/return", methods=["POST"])
def return_book():
    data = request.get_json(silent=True) or {}

    try:
        loan_id = int(data["loan_id"])
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Valid loan_id is required"}), 400

    result = library.return_book(loan_id)

    if "error" in result:
        status_code = 404 if result["error"] == "Loan not found" else 400
        return jsonify(result), status_code

    return jsonify(result), 200
