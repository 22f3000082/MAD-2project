#These configurations help us link our flask applications with various other extensions

class Config():
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True



class LocalDevelopmentConfig(Config):
    #The configuration for the local development environment(sqlite database)
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.sqlite3"
    DEBUG = True

    #The configuration for the security of the application
    SECURITY_PASSWORD_HASH = 'bcrypt'       #mechanism for hashing passwords
    SECURITY_PASSWORD_SALT = "hiddenkey"   # helps in hashing the password
    SECRET_KEY = "hiddenkey"               #secret key for the application
    WTF_CSRF_ENABLED = False                #cross-site request forgery protection
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
    
    # Redis Cache Configuration
    REDIS_URL = 'redis://localhost:6379/0'
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = 'redis://localhost:6379/0'
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes default cache timeout


