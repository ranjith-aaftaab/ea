class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///events.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your-secret-key-here'  # Secret key for session management
    ADMIN_USERNAME = 'admin'  # Hardcoded admin username
    ADMIN_PASSWORD = 'password'  # Hardcoded admin password (Use hashed passwords in production)
