'''
Created on 2018年5月4日

@author: sunrui
'''
import unittest
from models import (User,
                    Role,
                    Permission,
                    AnonymousUser)

class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        u = User.password('cat')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password = 'cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_salts_are_random(self):
        u = User(password='cat')
        u2 = User(password='cat')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_roles_and_permissions(self):
        Role.insert_roles()
        u = User(email='john@example.com', password='cat')
        self.assertTrue(u.can(Permission.WRITE))
        self.assertFalse(u.can(Permission.MODERATE_COMMENTS))

    def test_anonymous_user(self):
        u = AnonymousUser
        self.assertFalse(u.can(Permission.FOLLOW))