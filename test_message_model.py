"""Message model tests."""

# run these tests like:
#
#    python -m unittest test_message_model.py


import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Message, Follows

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app

db.create_all()


class MessageModelTestCase(TestCase):
    """Test messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            id= 999,
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        message = Message(
            text="Test message.",
            user_id= 999
        )

        db.session.add(u)
        db.session.add(message)
        db.session.commit()

        # User should have no messages & no followers
        self.assertNotEqual(message.timestamp, None)
        self.assertEqual(message.text, "Test message.")
        
    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()