from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from app import User, engine

Session = sessionmaker(bind=engine)
session = Session()

# user = session.query(User.name, func.count(User.name)).group_by(User.name).all()
# print(user)

# user = session.query(User.name, User.age, func.count(User.name)).group_by(User.age).all()
# for name, count, age in user:   #unpacking the tuple here cuz that's what it returns
#     print(f"there are {count} count of {name} with age {age}")


print('\nCHAINING METHODS')
users = session.query(User).filter(User.age > 24).filter(User.age < 50).all()

for user in users:
    print(f'{user.age = }')

# or like this
users_tuple = (
    session.query(User.age, func.count(User.id))
    .filter(User.age > 24)
    .order_by(User.age)
    .filter(User.age < 50)
    .group_by(User.age)
    .all()
)
for age, count in users_tuple:
    print(f'Age: {age} - Users: {count}')


# ========================================================================================
print('\nDELAY .all()')
only_iron_man = True
group_by_age = True

users = session.query(User)
if only_iron_man:
    users = users.filter(User.name == 'Iron Man')
if group_by_age:
    users = users.group_by(User.age)
users = users.all()
for user in users:
    print(f'User age: {user.age}, name: {user.name}')