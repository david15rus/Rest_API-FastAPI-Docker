import uuid

from sqlalchemy import Column, String, Float, ForeignKey, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Dish(Base):
    __tablename__ = "dishes"

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String, index=True, unique=True)
    description = Column(String)
    price = Column(Float, index=True)
    submenu_id = Column(UUID, ForeignKey('submenus.id'))

    submenu = relationship('SubMenu', back_populates='dishes')
