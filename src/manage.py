'''
Created on 2018年4月23日

@author: sunrui
'''
import os
from app import create_app, db, mail
from app.models import User, Role, Post, Comment, Tag, Permission
from flask_script import Manager, Server, Shell
from flask_migrate import Migrate, MigrateCommand

app=create_app('default')
manager=Manager(app)
migrate=Migrate(app, db)
manager.add_command("server", Server())
manager.add_command("db", MigrateCommand)

def follow_self():
    for user in User.query.all():
        if not user.is_following(user):
            user.follow(user)
            db.session.add(user)
    db.session.commit()

@manager.shell
def make_shell_context():
    return dict(app=app,
                db=db,
                User=User,
                Role=Role,
                Post=Post,
                Comment=Comment,
                Tag=Tag,
                Permission=Permission,
                mail=mail,
                fo = follow_self
                )

@manager.command
def test():
    """Run the unit test."""
    import unittest
    tests=unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
