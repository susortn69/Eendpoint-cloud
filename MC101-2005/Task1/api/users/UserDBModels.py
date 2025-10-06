from pydantic import BaseModel, EmailStr

class UserDBModel(BaseModel):
    id: int = 0
    name: str
    email: EmailStr
    hashed_password: str
    is_active: bool = True

# key: an uid, value: UserDBModel
UsersDB= {}

def get_users_db():
    """
    Get the UsersDB dictionary.
    """
    global UsersDB
    return UsersDB

def get_the_next_user_id():
    """
    Get the next user ID.
    """
    UsersDB = get_users_db()
    if UsersDB:
        return max(UsersDB.keys()) + 1
    return 1

def get_user_by_email(email: str):
    """
    Get a user by their email address.
    """
    UsersDB = get_users_db()
    for user in UsersDB.values():
        if user.email == email:
            return user 
    # This does the same thing
    # return next((user for user in UsersDB.values() if user.email == email), None)

def add_user(user: UserDBModel):
    """
    Add a new user to the UsersDB.
    """
    UsersDB = get_users_db()
    user.id = get_the_next_user_id()
    UsersDB[user.id] = user
    return user
def delete_user(user_id: int) -> bool:
    """Remove a user by identifier."""
    UsersDB = get_users_db()
    if user_id in UsersDB:
        del UsersDB[user_id]
        return True
    return False
