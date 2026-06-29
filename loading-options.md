selectinload(): Runs a separate, optimized second query utilizing an IN clause to fetch related collections. Best for one-to-many and many-to-many relationships.

joinedload(): Automatically creates an outer join in the primary SQL query to fetch parent and child objects at once. Best for many-to-one and one-to-one relationships.

subqueryload(): Generates a second query containing the original query statement nested as a subquery.

lazyload(): Default strategy. It does not fetch related data until you explicitly access the attribute in your Python script, which triggers a fresh database hit.raiseload()



5. Concurrency ParadigmsSQLAlchemy supports two distinct execution patterns based on your application stack:Synchronous: The classic operational mode where database requests block the execution thread until a response is received.Asynchronous (asyncio): Enables non-blocking queries using Python's async/await pattern. It is widely used alongside modern web frameworks like FastAPI to build high-concurrency applications


_______________________________________________________________________________________________ 

# Difference between cascade=delete and cascade=delete-orphan

1. The Core Difference
cascade="delete" (Parent-Centric)
When it triggers: Only when the Parent object itself is deleted via session.delete(parent).

Action: It cascades the delete operation to all associated child records in the database.

What it ignores: If you just remove a child from a parent's collection list 
(e.g., parent.children.remove(child)), 
cascade="delete" does nothing. The child remains in the database with its foreign key set to NULL (it becomes an orphan).

cascade="delete-orphan" (Collection-Centric + Parent-Centric)
When it triggers: It triggers in two scenarios:

When the Parent object is deleted (same as cascade="delete").
When a Child is disconnected/severed from the parent (e.g., removing it from a list, or setting child.parent = None).

Action: It completely deletes the child from the database the moment it loses its relationship with the parent.

2. Code Example Breakdown
Imagine a User (Parent) has a One-to-Many relationship with Address (Child).

Scenario A: Removing an item from a list

# Assume user 1 has address A and address B
user = session.get(User, 1)
address_a = user.addresses[0]

# Disconnecting Address A from the User
user.addresses.remove(address_a)
session.commit()

If using cascade="delete": Address A stays in the database. Its user_id column simply becomes NULL. It is now an "orphan" record eating up database space.If using cascade="delete-orphan": SQLAlchemy recognizes that Address A no longer has a parent. It automatically emits a DELETE FROM address WHERE id = A; query.

Scenario B: Deleting the entire parent object

user = session.get(User, 1)
session.delete(user)
session.commit()

If using cascade="delete": The user is deleted, and all of their addresses are deleted from the database too.If using cascade="delete-orphan": Exactly the same thing happens. The user and all of their addresses are deleted.



_______________________________________________________________________________________________ 
Some More Notes :
_______________________________________________________________________________________________ 

EAGER LOADING:
eager loading options save you extra trips to the DB. 
It fetches data for you in advance or as the name suggests eagerly loads data for you to use.
It does not necessarily optimize the query although you MIGHT(emphasis on might NOT ALWAYS) get it little more complicated as the data you are recieving are in lots if you are using backref/backpopulates the related data will come too.

If 2 tables have no relationship defined between them and if you try joinedload there you will get a cartesian product or a cartesian explosion.
Also once you do a joinedload and you want to use the filter then those filters will not work properly because of the following : 

## My prompt to the gemini: 
You said: "SQLAlchemy us filter ko main table (parent) par apply karta hai, na ki us table par jise aap load kar rahe ho."
So filter apply ho rha hai bas join lagne se pehle ho rha hai, so it still should work correct ? Lekin aisa nahi hota mujhe filtered data nahi milta , 

consider: 
results = session.query(User).\
    joinload(User.addresses).\
    filter(Address.city == 'Mumbai').\
    .all()

iska reason ye hai ki maine filter main query mein jo table hai uspe nahi lagaya(ie.User) and city column Address table mein hai , user table mein city column nahi hai and hence agar uspe filter lagta bhi hai toh usko column milega bhi nahi , it is as good as no filter. 

if it was something like : 
results = session.query(User).\
    join(User.addresses).\
    filter(User.birthplace== 'Mumbai').\
    .all() 

then kya ye work karta  ? 

## Answer
Aapne bilkul pakda hai point ko, par ismein ek chhota sa twist hai jiski wajah se confusion hota hai. Chaliye dono cases ko step-by-step todte hain.

---

### Case 1: Aapka pehla query (Jo fail hota hai)

```python
results = session.query(User).\
    options(joinedload(User.addresses)).\
    filter(Address.city == 'Mumbai').\
    all()

```

**Yeh kaam kyun nahi karta?**
Aapka logic sahi hai ki `User` table mein `city` column nahi hai. Par jab aap SQL generate dekhoge, toh background mein `joinedload` ek `LEFT OUTER JOIN` toh lagata hai. Lekin twist yeh hai ki SQLAlchemy `joinedload` waale join ko **anonymous join** (ya aliased join) ki tarah treat karta hai.

SQLAlchemy ko pata hi nahi chalta ki aapne jo `filter(Address.city == 'Mumbai')` likha hai, use us `joinedload` waale table se connect karna hai. SQL query mein filter to lag jata hai (with a generic table name), par query breakdown ho jaati hai ya unexpected result deti hai kyunki SQLAlchemy use parent entity ka filter samajh hi nahi paata.

---

### Case 2: Aapka doosra query (Kya yeh kaam karega?)

```python
results = session.query(User).\
    join(User.addresses).\
    filter(User.birthplace == 'Mumbai').\
    all() 

```

**Haan, yeh 100% perfectly kaam karega!** Iske piche ka reason bohot simple hai:

1. **Column Validation:** `birthplace` column `User` table ka hi hissa hai.
2. **Main Query Filter:** SQLAlchemy `User` table par filter lagayega, jisse sirf wahi users fetch honge jinka `birthplace == 'Mumbai'` hai.
3. **No Conflict:** Kyunki aap relationship (`User.addresses`) par koi filter nahi laga rahe ho, SQLAlchemy aapse koi shikayat nahi karega.

#### Lekin ek chhota sa "Catch" hai...

Is query mein aapne `.join(User.addresses)` likha hai. Isse SQL mein `INNER JOIN` banega.

* Agar koi aisa user hai jiska `birthplace == 'Mumbai'` hai, **par uska koi address nahi hai**, toh woh user result mein **nahi aayega** (kyunki `INNER JOIN` dono sides data maangta hai).
* Agar aap chahte hain ki address ho ya na ho, user aana chahiye agar uska birthplace Mumbai hai, toh aapko `.outerjoin(User.addresses)` use karna chahiye.

---

### Golden Rule Jo Aapko Yaad Rakhna Hai 💡

* **`filter()`** hamesha un tables par kaam karta hai jo aapne `.query()`, `.join()`, ya `.outerjoin()` mein **explicitly (safely)** likhe hain.
* **`joinedload()`** ke andar chal rahe table/join par aap bahar se `filter()` **nahi** laga sakte. Agar joined table par filter chahiye, toh aankh band karke **`contains_eager`** ka use kijiye.







___________________________________________

Option: lazyload
Kya karta hai? :   Zarurat padne par fetch karta hai.
Performance Impact: N+1 ka khtra, latency badhti hai loops mein.

Option: joinedload / selectinload
Kya karta hai: Saath mein data utha lata hai.
Performance Impact: Best hai agar aapko related data chahiye hi chahiye.

Option: raiseload
Kya karta hai?: Lazy load karne par Error deta hai.
Performance Impact: Best for safety, taaki galti se query na fire ho.

Option: load_only
Kya karta hai? : Sirf selected columns lata hai.
Performance Impact: Network payload aur RAM memory dono kam karta hai (Super Fast).

Ek aur Option bhi hai called DEFER: 
defer: Yeh load_only ka ulta hai. Agar aapko saare columns chahiye bas note jaisa bada text column nahi chahiye, toh aap use defer kar sakte ho: options(defer(Resource.note)).