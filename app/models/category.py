from flask import current_app as app


class Category:
    def __init__(self, category):
        self.category = category


    @staticmethod
    def get():
        rows = app.db.execute('''
SELECT *
FROM Category
''')
        return rows
