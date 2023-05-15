####
#### SQLAlchemy provides a powerful and flexible toolkit for working with databases in Python, whether you prefer using an ORM or writing SQL queries directly. 
#### It allows you to abstract away the complexities of database interactions and focus on writing Python code to interact with the data.
####
#### SQLachemy code for understanding of how it import Python library to create RDBMS engine, table, column , creates MySQL engine,  
#### Create Sessoin, Create MySQL Table,  Create MySQL User, Delet MySQl user
#### 

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create the engine for connecting to the MySQL database
engine = create_engine('mysql+mysqlconnector://username:password@host/database_name')

# Create a session factory
Session = sessionmaker(bind=engine)
session = Session()

# Create a base class for declarative models
Base = declarative_base()

# Define a sample model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255))

# Create the table if it does not exist
Base.metadata.create_all(engine)

# Create a new MySQL user
new_user = User(name='Sam Star', email='sam.star@example.com')
session.add(new_user)
session.commit()

# Query all MySQL users
users = session.query(User).all()
for user in users:
    print(user.name, user.email)

# Update a MySQL user
user = session.query(User).filter_by(name='John Doe').first()
user.email = 'new_email@example.com'
session.commit()

# Delete a MySQL user
user = session.query(User).filter_by(name='Sam Star').first()
session.delete(user)
session.commit()

####### 
