import uuid

from sqlalchemy import Column, String, ForeignKey, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SubMenu(Base):
    __tablename__ = "submenus"

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String, index=True, unique=True)
    description = Column(String)
    menu_id = Column(UUID, ForeignKey("menus.id"))

    menu = relationship('Menu', back_populates='submenus')
    dishes = relationship('Dish', back_populates='submenu', cascade="all, delete-orphan")