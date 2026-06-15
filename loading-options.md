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