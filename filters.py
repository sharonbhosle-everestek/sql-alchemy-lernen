from sqlalchemy import and_, not_, or_

from app import User, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

# filter
# this one works like a filter, duh ? as if it takes a criteria and apply filter
# users = session.query(User).filter(User.name=="Iron Man").all()

'''This is more LIKE A WHERE clause but NOT A WHERE clause bcoz it does NOT takes conditional vlaues  like filter() instead takes **kwargs or dict key-val pairs
Hence ...'''
# This will give TypeError:  Query.filter_by() takes 1 positional argument but 2 were given
# users = session.query(User).filter_by(User.name=="Iron Man").all()

# but this
# users = session.query(User).filter_by(name="Iron Man").all() # also you don't need to use Class.attribute name just directly go for attribute 

# multiple filters
# users = session.query(User).filter_by(name="Iron Man", age=19).all()


# WHERE method accepts conditions as well like filter() + filter_by() ==> where()
# users = session.query(User).where(User.name=="Hulk", User.age>=50) >>> No results

# users = session.query(User).where(User.name=="Hulk", User.age>=14) 

# for i in users:
#     print(i.id, i.name, i.age)


# AND, OR and NOT

# by default where uses AND operator so both the name and age conditions must be true, hence the below 2 queries gives same results
# users1 = session.query(User).where(User.name=="Hulk", User.age>=14).all() 
# users2 = session.query(User).where(and_(User.name=="Hulk", User.age>=14)).all() 
# print("🟠", users1==users2)   # Outputs : True 
#

# in this only one of the conditions needs to be true 
# users = session.query(User).where(or_(User.name=="Hulk", User.age>=14)).all() 

# this is the negation or NOT operator, IT TAKES ONLY ONE ARGUMENT. So if you have multiple request u gotta bundle them in parenthesis like this, this also proves u can use these these operators within each other
# users = session.query(User).where(not_(and_(User.name=="Hulk", User.age>=14))).all()


# alternate ways of writing the same queries 
# users = session.query(User).where((User.name=="Hulk") & (User.age>=14)).all()
# users = session.query(User).where(or_(User.name=="Hulk") | (User.age>=14)).all() 
users = session.query(User).where(~((User.name=="Hulk") & (User.age>=14))).all()

for i in users:
    print(i.id, i.name, i.age)