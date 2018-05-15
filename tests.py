from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Post

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='jitendra')
        u.set_password('jitrajput')
        self.assertFalse(u.check_password('jitendrarajput'))
        self.assertTrue(u.check_password('jitrajput'))

    def test_avatar(self):
        u = User(username='sujay', email='apale.sujay@gmail.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/5dcca68d70293669feb43a84e1ae0b08?d=retro&s=128'))

    def test_follow(self):
        u1 = User(username='sujay', email='apale.sujay@gmail.com')
        u2 = User(username='jitendra', email='jitendra.rajput@gmail.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'jitendra')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'sujay')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):
        # create four users
        u1 = User(username='sujay', email='apale.sujay@gmail.com')
        u2 = User(username='jitendra', email='jitendra.rajput@gmail.com')
        u3 = User(username='aditya', email='aditya.kaul@gmail.com')
        u4 = User(username='saurav', email='saurav.maity@gmail.com')
        db.session.add_all([u1, u2, u3, u4])

        # create four posts
        now = datetime.utcnow()
        p1 = Post(body="post from sujay", author=u1,
                  timestamp=now + timedelta(seconds=1))
        p2 = Post(body="post from jitendra", author=u2,
                  timestamp=now + timedelta(seconds=4))
        p3 = Post(body="post from aditya", author=u3,
                  timestamp=now + timedelta(seconds=3))
        p4 = Post(body="post from saurav", author=u4,
                  timestamp=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # setup the followers
        u1.follow(u2)  # sujay follows jitendra
        u1.follow(u4)  # sujay follows saurav
        u2.follow(u3)  # jitendra follows aditya
        u3.follow(u4)  # aditya follows saurav
        db.session.commit()

        # check the followed posts of each user
        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])

if __name__ == '__main__':
    unittest.main(verbosity=2)