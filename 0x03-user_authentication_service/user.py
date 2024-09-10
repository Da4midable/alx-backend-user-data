#!/usr/bin/env python3
"""
This module defines a SQLAlchemy ORM model for a User.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for declarative SQLAlchemy models.

    This class uses the DeclarativeBase from SQLAlchemy ORM to provide
    a base for declarative class definitions.
    """
    pass


class User(Base):
    """
    SQLAlchemy ORM model representing a user in the database.

    This class defines the structure and constraints of the 'users' table
    in the database.
    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250))
    reset_token = Column(String(250))
