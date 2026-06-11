manager = relationship(
    "ResourceManager",
    cascade="all, delete-orphan",
    uselist=False,
    primaryjoin="Resource.resource_id == ResourceManager.resource_id",
    foreign_keys="[ResourceManager.resource_id]", 
    passive_deletes=True
    )


ye upar k saare cheezo ka understanding lo , cascade kya hota hai and relationship mein kya kya use hota hai 

is_resource_manager = Column(
        "is_resource_manager", BOOLEAN, default=False, nullable=False
    )
    created_at = Column(
        "created_at", TIMESTAMP(timezone=True), default="NOW()", nullable=False
    )
    modified_at = Column(
        "modified_at",
        TIMESTAMP(timezone=True),
        default="NOW()",
        onupdate="NOW()",
        nullable=False,
    )

    ye functions kaise likhte hai and agar tumko koi custom function likhna hai toh tum kaise likhoge