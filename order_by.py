import random

from app import User, engine
from sqlalchemy.orm import sessionmaker


Session = sessionmaker(bind=engine)
session = Session()

# names = ["Batman", "SuperMan", "Iron Man", "Black Widow", "Hulk", "Vegeterian Hulk", "Peter Griffin"]

# ages = list(range(11, 33))

# for i in range(20):
#     user = User(
#         name = random.choice(names), 
#         age = random.choice(ages)
#     )

#     session.add(user)

# session.commit()


# obj = session.query(User).order_by(User.age.desc()).all()

'''this case first it will order by age in descending, then among the group of duplicates it will order by name and from those duplicates it will order by id and this will be better understood by this query ''' 
obj = session.query(User).filter(User.name=="Hulk").order_by(User.age.desc(), User.name, User.id).all()

for i in obj:
    print(f"{i.id}   {i.name}    {i.age}")