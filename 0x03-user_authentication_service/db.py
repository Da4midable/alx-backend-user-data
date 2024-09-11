#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, and_, tuple_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database"""
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
        except Exception:
            self.__session.rollback()
            new_user = None
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user based on filter criteria.
        """
        invalid_keys = [key for key in kwargs if not hasattr(User, key)]
        if invalid_keys:
            raise InvalidRequestError()

        filters = [getattr(User, key) == value for key,
                   value in kwargs.items()]

        result = self._session.query(User).filter(and_(*filters)).first()
        if result is None:
            raise NoResultFound()
        return result

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates a user's attributes based on the given keyword arguments.

        :param user_id: the ID of the user to update
        :param kwargs: attributes to update and their new values
        :raises NoResultFound: if the user with the given ID is not found
        :raises ValueError: if one of the given attributes does not exist
        :return: None
        """
        try:
            user = self.find_user_by(id=user_id)
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
                else:
                    raise ValueError
            self._session.commit()
        except NoResultFound:
            raise NoResultFound
        except InvalidRequestError as e:
            raise InvalidRequestError(e)
