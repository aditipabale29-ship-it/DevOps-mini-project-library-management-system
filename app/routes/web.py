from flask import Blueprint, render_template_string

web = Blueprint("web", __name__)


@web.route("/library")
def library_home():
    return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Library Management System</title>
        </head>
        <body>
            <h1>Library Management System</h1>
            <p>Welcome to the Library Management System.</p>
            <p>Use the API endpoints to manage books, users, and loans.</p>
        </body>
        </html>
    """)
