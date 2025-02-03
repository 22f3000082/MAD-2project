#These configurations help us link our flask applications with various other extensions

class Config():
    DEBUG = False
    SQL_ALCHEMY_TRACK_MODIFICATIONS = True



class LocalDevelopmentConfig(Config):
    #The configuration for the local development environment(sqlite database)
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.sqlite3"
    DEBUG = True

    #The configuration for the security of the application
    SECURITY_PASSWORD_HASH = 'bcrypt'       #mechanism for hashing passwords
    SECURITY_PASSWORD_SALT = "hiddenkey"   # helps in hashingthe password
    SECRET_KEY = "hiddenkey"               #secret key for the application
    WTF_CSRF_ENABLED = False                #cross-site request forgery protection
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
    

    # cache specific
    # CACHE_TYPE =  "RedisCache"
    # CACHE_DEFAULT_TIMEOUT = 30
    # CACHE_REDIS_PORT = 6379

    # WTF_CSRF_ENABLED = False