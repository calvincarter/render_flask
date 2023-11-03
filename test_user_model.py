"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test users."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
        
    def test_repr(self):
        """Does the repr function work?"""
        
        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        
        db.session.add(u)
        db.session.commit()
        
        self.assertEqual(u.email, "test@test.com")
        self.assertEqual(u.username, "testuser")
        self.assertEqual(u.password, "HASHED_PASSWORD")
        
    def test_is_following(self):
        """Does the program detect when someone is following someone else?"""
        
        user1 = User(
            email="user1@user1.com",
            username="user1",
            password="HASHED_PASSWORD"
        )
        
        user2 = User(
            email="user2@user2.com",
            username="user2",
            password="HASHED_PASSWORD"
        )
        
        user1.following.append(user2)
        
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        
        self.assertTrue(user1.is_following(user2))
        
    def test_is_not_following(self):
        """Does the program detect when someone is not following someone else?"""
        
        user1 = User(
            email="user1@user1.com",
            username="user1",
            password="HASHED_PASSWORD"
        )
        
        user2 = User(
            email="user2@user2.com",
            username="user2",
            password="HASHED_PASSWORD"
        )
        
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        
        self.assertFalse(user1.is_following(user2))
        
    def test_is_followed_by(self):
        """Does the program detect when someone is being followed someone else?"""
        
        user1 = User(
            email="user1@user1.com",
            username="user1",
            password="HASHED_PASSWORD"
        )
        
        user2 = User(
            email="user2@user2.com",
            username="user2",
            password="HASHED_PASSWORD"
        )
        
        user2.following.append(user1)
        
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        
        self.assertTrue(user1.is_followed_by(user2))
        
    def test_is_not_followed_by(self):
        """Does the program detect when someone is not being followed someone else?"""
        
        user1 = User(
            email="user1@user1.com",
            username="user1",
            password="HASHED_PASSWORD"
        )
        
        user2 = User(
            email="user2@user2.com",
            username="user2",
            password="HASHED_PASSWORD"
        )
        
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        
        self.assertFalse(user1.is_followed_by(user2))
        
    def test_create_user(self):
          """Test that a user can be created."""
          
          test_user = User.signup("test_user", "testuser@testuser.com", "Password", None)
          new_id = 999
          test_user.id = new_id
          
          db.session.commit()
          
          user = User.query.get(new_id)
          self.assertEqual(user.id, new_id)
          self.assertEqual(user.username, "test_user")
          self.assertEqual(user.email, "testuser@testuser.com")
          self.assertNotEqual(user.password, "Password")
          self.assertTrue(user.password.startswith('$2b$'))
          
    def test_bad_create_user(self):
        """Test that a bad user is rejected."""
          
        bad_user = User.signup(None, "testuser@testuser.com", "Password", None)
        new_id = 999
        bad_user.id = new_id
        
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()
          
    def test_authenticate(self):
        """Check if authenticate is working properly."""
        
        test_user = User.signup("test_user", "testuser@testuser.com", "Password", None)
        new_id = 999
        test_user.id = new_id
          
        db.session.commit()
        
        self.assertEqual(User.authenticate("test_user", "Password"), test_user)
        
    def test_invalid_username(self):
        """Check if authenticate doesn't work properly with invalid username."""
        
        test_user = User.signup("test_user", "testuser@testuser.com", "Password", None)
        db.session.commit()
        
        self.assertFalse(User.authenticate("wrong_user", "Password"))
        
    def test_invalid_password(self):
        """Check if authenticate doesn't work properly with invalid password."""
        
        test_user = User.signup("test_user", "testuser@testuser.com", "Password", None)
        db.session.commit()
        
        self.assertFalse(User.authenticate("test_user", "wrongPassword"))
        
    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()
        
