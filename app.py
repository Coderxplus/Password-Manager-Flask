# # import string
# # import random
# # from cryptography.fernet import Fernet



# # def generate_password():
# #     password = random.choices(string.ascii_letters+string.digits+string.punctuation, k=13)
# #     return "".join(password)

# # def encrypt_password(password):
# #     key = Fernet.generate_key()
# #     with open("key.key", 'wb') as f:
# #         f.write(key)
# #     fi = Fernet(key)
# #     cipher_text = fi.encrypt(password)
# #     return cipher_text

# # def decrypt_password(cipher_text):
# #     with open("key.key", 'r') as f:
# #         key = f.read()
# #     fi = Fernet(key)
# #     plain_text = fi.decrypt(cipher_text)
# #     return plain_text.decode('utf-8')


# # cipher  = encrypt_password(generate_password().encode('utf-8'))

# # print("Encrypted Password:", cipher)
# # plain = decrypt_password(cipher)
# # print("Decrypted Password:", plain)

# from sqlalchemy import create_engine
# # from sqlalchemy.pool import NullPool
# from dotenv import load_dotenv
# import os

# # Load environment variables from .env
# load_dotenv()

# # Fetch variables
# USER = os.getenv("user")
# PASSWORD = os.getenv("password")
# HOST = os.getenv("host")
# PORT = os.getenv("port")
# DBNAME = os.getenv("dbname")

# # Construct the SQLAlchemy connection string
# DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

# # Create the SQLAlchemy engine
# engine = create_engine(DATABASE_URL)
# # If using Transaction Pooler or Session Pooler, we want to ensure we disable SQLAlchemy client side pooling -
# # https://docs.sqlalchemy.org/en/20/core/pooling.html#switching-pool-implementations
# # engine = create_engine(DATABASE_URL, poolclass=NullPool)

# # Test the connection
# try:
#     with engine.connect() as connection:
#         print("Connection successful!")
# except Exception as e:
#     print(f"Failed to connect: {e}")



from sqlalchemy import create_engine
# from sqlalchemy.pool import NullPool
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Fetch variables
USER = "postgres.yjiurgdscvhvqagahbgr"
PASSWORD = "coderxplus1955"
HOST = "aws-0-eu-central-1.pooler.supabase.com"
PORT = 6543 
DBNAME = "postgres"


DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as connection:
        print("Connection successful!")
except Exception as e:
    print(f"Failed to connect: {e}")

