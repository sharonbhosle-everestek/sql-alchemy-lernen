from one_2_many import session, User, Address

obj = session.query(User).filter(User.user_id==1).one_or_none()
obj2 = session.query(User).filter(User.user_id==2).one_or_none()

print([i.place for i in  obj.address])

print(obj2.address[0].country)

add = session.query(Address).filter(Address.user_id==1).all()
print([i.user.name for i in add])