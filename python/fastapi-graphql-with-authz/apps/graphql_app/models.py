import datetime

from fastapi_authz.db import (
    BaseModel,
    Column,
    BigInteger,
    Integer,
    Unicode,
    DateTime,
    UniqueConstraint,
    ForeignKey,
    Table,
    relationship,
)


association_table = Table(
    "user_userrole_association",
    BaseModel.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("userrole_id", ForeignKey("userroles.id")),
)


class User(BaseModel):
    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True,
    )
    username = Column(Unicode(20), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )
    token = Column(Unicode(255), nullable=True)

    roles = relationship("UserRole", secondary=association_table)

    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("username", name="uq_user_username"),)
    __mapper_args__ = {"eager_defaults": True}


class UserRole(BaseModel):
    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True,
    )
    name = Column(Unicode(250), nullable=False)

    __tablename__ = "userroles"
    __table_args__ = (UniqueConstraint("name", name="uq_user_roles_name"),)
    __mapper_args__ = {"eager_defaults": True}
