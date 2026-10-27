def init_db(app):
    """Initialize the database for the application."""
    app.config.setdefault("DATABASE_INITIALIZED", False)
    app.config["DATABASE_INITIALIZED"] = True
