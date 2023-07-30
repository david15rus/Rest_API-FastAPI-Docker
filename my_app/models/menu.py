import uuid

from sqlalchemy import Column, String, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Menu(Base):
    __tablename__ = "menus"

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String, index=True, unique=True)
    description = Column(String)

    submenus = relationship('SubMenu', back_populates='menu', cascade="all, delete-orphan")