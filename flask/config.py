class Config:
    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "33510jaswal"  # Your MySQL password
    MYSQL_DB = "wealthyinfyme"
    MYSQL_PORT = 3306  # Default MySQL port
    MYSQL_UNIX_SOCKET = '/path/to/your/mysql/socket'  # Only needed for Unix socket connections
    SECRET_KEY = "This_is_a_super_secret_key"
    MYSQL_CURSORCLASS = 'DictCursor'
