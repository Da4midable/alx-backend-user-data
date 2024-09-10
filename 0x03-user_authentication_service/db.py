#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
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
        self._engine = create_engine("sqlite:///a.db", echo=True)
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
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Finds a user by keyword arguments.

        :param kwargs: Arbitrary keyword arguments to filter the user
        :return: User object
        :raises NoResultFound: If no user is found
        :raises InvalidRequestError: If invalid query arguments are passed
        """
        session = self._session

        try:
            query = session.query(User).filter_by(**kwargs)
            user = query.one()

            if user is None:
                raise NoResultFound()

            return user

        except NoResultFound:
            raise NoResultFound()

        except Exception:
            raise InvalidRequestError()

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
