# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from modules import User
# import bcrypt

# DATABASE_URI = 'mysql+pymysql://Abhi:Abhi123@localhost/drugdb'

# engine = create_engine(DATABASE_URI)
# Session = sessionmaker(bind=engine)
# session = Session()

# def register(name, username, password):
#     hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
#     new_user = User(name=name, username=username, password=hashed_password.decode('utf-8'))
#     session.add(new_user)
#     session.commit()

# def login(username, password):
#     user = session.query(User).filter_by(username=username).first()
#     if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
#         return True
#     return False

from pymongo import MongoClient
import bcrypt
import ssl
import streamlit as st
# Connection URI
# MONGO_URI = "mongodb+srv://Abhishek:abhi123@drugdatacluster0.ko5uq.mongodb.net/Shelf_life_users?retryWrites=true&w=majority"
# Load MongoDB URI from Streamlit Secrets
# MONGO_URI = st.secrets["MONGO"]["URI"]
# Set up MongoDB connection
if "MONGO_URI" in st.secrets:
    MONGO_URI = st.secrets["MONGO_URI"]
else:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://Abhishek:abhi123@drugdatacluster0.ko5uq.mongodb.net/Shelf_life_users?retryWrites=true&w=majority")



# client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)
# db = client["Shelf_life_users"]
# users_collection = db["Users"]


# Set up MongoDB connection
try:
    client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)
    db = client["Shelf_life_users"]  # Replace with your actual database name
    users_collection = db["Users"]   # Replace with your actual collection name
    print("Connected to MongoDB Atlas successfully.")
except Exception as e:
    print("Failed to connect to MongoDB:", e)
    raise

# Register function
def register(name, username, password):
    if users_collection.find_one({"username": username}):
        raise ValueError("Username already exists.")
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = {
        "name": name,
        "username": username,
        "password": hashed_password.decode('utf-8')
    }
    result = users_collection.insert_one(new_user)
    return result.inserted_id

# Login function
def login(username, password):
    user = users_collection.find_one({"username": username})
    if user and bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
        return True
    return False
