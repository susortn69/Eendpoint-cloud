class Endpoints:
    REGISTER = "/register"
    ROOT = "/"
    HEALTH = "/health"
    LOGIN = "/login"
    USER_INFO = "/info"
    USER_DELETE = "/delete"


class ResponseMessages:
    WELCOME = "Welcome to the Voting App!"
    HEALTH_OK = "The service is up and running!"
    USER_CREATED = "User successfully created."
    LOGIN_SUCCESS = "Login successful."
    USER_DELETED = "User deleted successfully."
    USER_ALREADY_EXISTS = "User with this email already exists."
    USER_NOT_FOUND = "User with this email does not exist."
    USER_INACTIVE = "User is inactive and cannot vote."
    INVALID_PASSWORD = "The password provided is incorrect."
    INVALID_TOKEN_MISSING_EMAIL = "Invalid token: missing email"
    INVALID_TOKEN_MISSING_USER = "Invalid token: missing user"
    INVALID_TOKEN = "Invalid token"
