from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login


class User(UserMixin):
    def __init__(self, id, email, firstname, lastname, address, balance):
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.address = address
        self.balance = balance

    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
SELECT password, id, email, firstname, lastname, address, balance
FROM Users
WHERE email = :email
""",
                              email=email)
        if not rows:  # email not found
            return None
        elif not check_password_hash(rows[0][0], password):
            # incorrect password
            return None
        else:
            return User(*(rows[0][1:]))

    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
SELECT email
FROM Users
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

    @staticmethod
    def register(email, password, firstname, lastname, address):
        try:
            rows = app.db.execute("""
INSERT INTO Users(email, password, firstname, lastname, address, balance)
VALUES(:email, :password, :firstname, :lastname, :address, 0.0)
RETURNING id
""",
                                  email=email,
                                  password=generate_password_hash(password),
                                  firstname=firstname,
                                  lastname=lastname,
                                  address=address)
            id = rows[0][0]
            return User.get(id)
        except Exception:
            # likely email already in use; better error checking and
            # reporting needed
            print("couldn't register")
            return None

    @staticmethod
    @login.user_loader
    def get(id):
        rows = app.db.execute("""
SELECT id, email, firstname, lastname, address, balance
FROM Users
WHERE id = :id
""",
                              id=id)
        return User(*(rows[0])) if rows else None

    @staticmethod
    def get_info():
        rows = app.db.execute('''
SELECT id, firstname, lastname, address
FROM Users
''')
        return rows


    # update user info with the passed values, but id is same as before to find table entry
    @staticmethod
    def edituser(id, email, password, firstname, lastname, address, balance):
        try:
            rows = app.db.execute("""
UPDATE Users
SET email = '{}', password = '{}', firstname = '{}', lastname = '{}', address = '{}', balance ={}
WHERE id = {}
RETURNING *
""".format(
                                  email,
                                  generate_password_hash(password),
                                  firstname,
                                  lastname,
                                  address,
                                  balance,
                                  id))
            return rows
        except Exception:
            print("couldn't update user")
            return None

    @staticmethod
    def get_name(uid):
        # Returns uid's first and last name
        rows = app.db.execute('''
    SELECT firstname, lastname
    FROM Users
    WHERE id=:uid
    ''', 
                            uid=uid)
        return f"{rows[0][0]} {rows[0][1]}"