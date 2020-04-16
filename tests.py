from datetime import datetime, timedelta
import unittest
from app import db, create_app
from app.models import User, Word, Dictionary, UserWord
from config import TestConfig

class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_follow(self):
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'susan')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'john')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):
        # create four users
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        u3 = User(username='mary', email='mary@example.com')
        u4 = User(username='david', email='david@example.com')
        db.session.add_all([u1, u2, u3, u4])

        # create four posts
        now = datetime.utcnow()
        w1 = Word(name="cool")
        w2 = Word(name="sadie")
        w3 = Word(name="new")

        db.session.add_all([w1, w2, w3])
        db.session.commit()

        # users each have dictionary
        d1 = Dictionary(name='john dict', user_id=u1.id)
        d2 = Dictionary(name='susan dict', user_id=u2.id)
        d3 = Dictionary(name='mary dict', user_id=u3.id)
        d4 = Dictionary(name='david dict', user_id=u4.id)

        db.session.add_all([d1, d2, d3, d4])
        db.session.commit()

        # users add words to their dictionaries
        uw1 = UserWord(word_id=w1.id, user_id=u1.id, dictionary_id=d1.id)
        uw2 = UserWord(word_id=w1.id, user_id=u2.id, dictionary_id=d2.id)
        uw3 = UserWord(word_id=w1.id, user_id=u3.id, dictionary_id=d3.id)

        uw4 = UserWord(word_id=w2.id, user_id=u4.id, dictionary_id=d4.id)
        uw5 = UserWord(word_id=w3.id, user_id=u4.id, dictionary_id=d4.id)
        uw6 = UserWord(word_id=w2.id, user_id=u3.id, dictionary_id=d3.id)

        db.session.add_all([uw1, uw2, uw3, uw4, uw5, uw6])
        db.session.commit()

        # setup the followers
        u1.follow(u2)  # john follows susan
        u1.follow(u4)  # john follows david
        u2.follow(u3)  # susan follows mary
        u3.follow(u4)  # mary follows david
        db.session.commit()

        # check the followed posts of each user
        f1 = u1.friend_highlights().all() # john should see susan's and david dictionary words
        f2 = u2.friend_highlights().all() # susan should see mary words
        f3 = u3.friend_highlights().all()
        f4 = u4.friend_highlights().all()
        self.assertEqual(f1, [uw5, uw4, uw2])
        self.assertEqual(f2, [uw6, uw3])
        self.assertEqual(f3, [uw5, uw4])
        self.assertEqual(f4, [])

if __name__ == '__main__':
    unittest.main(verbosity=2)
