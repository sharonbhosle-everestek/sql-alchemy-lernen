from one_2_many import session, User, Address

# Creating users
user1 = User(name="sharon", age=33)
user2 = User(name="aaron", age=32)

add1 = Address(user_id=1, country="USA", place="rhode island")
add2 = Address(user_id=1, country="USA", place="houston")
add3 = Address(user_id=2, country="USA", place="new jersey")

session.add_all([user1, user2, add1, add2, add3])
session.commit()