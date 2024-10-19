from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modules import User
import bcrypt

DATABASE_URI = 'mysql+pymysql://Abhi:Abhi123@localhost/drugdb'

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

def register(name, username, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = User(name=name, username=username, password=hashed_password.decode('utf-8'))
    session.add(new_user)
    session.commit()

def login(username, password):
    user = session.query(User).filter_by(username=username).first()
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return True
    return False
