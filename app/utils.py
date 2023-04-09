from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password:str):
    
    """
    Hashes a password using the default hashing algorithm and returns the hashed value.
    """
    return pwd_context.hash(password)
    
def verify(plain_password,hashed_password):

    """
    Verifies whether a plain text password matches the hashed password.
    Returns True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password,hashed_password)