from sqlalchemy.orm import sessionmaker
from app import User, engine
import json

Session = sessionmaker(bind=engine)

session = Session()  # OR you can also do different name like ==> db_obj = Session()

# performing CRUD operation

# Create
# user1 = User(name="John Doe", age=33)
# session.add(user1)
# session.commit()

# user2 = User(name="sharon", age=99)
# user3 = User(name="prashant", age=10)
# user4 = User(name="komal", age=23)

# session.add_all([user2, user3, user4])
# session.commit()


# Read
# user = session.query(User).first()
# print((user)) # gives <app.User object at 0x00000231F234F230>

# user = session.query(User).all()
# print(user) 
# gives [<app.User object at 0x00000231F234F230>, <app.User object at 0x00000231F2273D90>, <app.User object at 0x00000231F2273ED0>, <app.User object at 0x00000231F22569E0>]

# for i in user:
#     print(f"User's name is {i.name} and age is {i.age}. ")



# Update
# new_user = User(name="sharon", age=2)
# session.add(new_user)
# session.commit()

# user_obj = session.query(User).filter(User.name=="Sharon").all()  >> gives empty [] becoz spelling mistake

# user_obj_all = session.query(User).filter(User.name=="sharon").all()
# print([f"for id {i.id} name is {i.name} and {i.age}" for i in user_obj_all])

# user_obj_first = session.query(User).filter(User.name=="sharon").first()
# print(user_obj_first.id, user_obj_first.name, user_obj_first.age)

# my_obj = session.query(User).filter(
#     User.id==2,
#     User.name=="Replaced Name"
# ).one_or_none()  
# #could have user first() too but figured i will get the one object or none if not found , the example below is for None

# print( "Example of one_or_none() == 👉", 
#     session.query(User).filter(User.name=="Sharon").one_or_none()
#     )

# my_obj.name = "Replaced Name again"
# my_obj.age = "300"

# print("Before commit ...")
# print(my_obj.name)
# print(my_obj.age)  #but the changes won't reflect bcoz we haven't commited yet

# session.commit()

# print("after commit >>>>", (session.query(User).filter(User.id==2).first()).name)
# print("after commit >>>>", (session.query(User).filter(User.id==2).first()).id)



# DELETE
# del_obj = session.query(User).filter(User.id==6).one_or_none()

# print("Before deletion >>> ",  
#     del_obj.id, del_obj.name, del_obj.age
# )
# session.delete(del_obj)
# session.commit()

# here the object is still available to us in memory of the ssesion once the session is complete it will release all the info it is holding on to
# print("After deletion and commit >>>>", del_obj, del_obj.id, del_obj.name, del_obj.age)





