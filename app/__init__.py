from flask import Flask
from flask_login import LoginManager
from flask_babel import Babel, format_datetime
from .config import Config
from .db import DB


login = LoginManager()
login.login_view = 'users.login'
babel = Babel()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.db = DB(app)
    login.init_app(app)
    babel.init_app(app)

    from .index import bp as index_bp
    app.register_blueprint(index_bp)

    from .users import bp as user_bp
    app.register_blueprint(user_bp)

    from .inventory import bp as inventory_bp
    app.register_blueprint(inventory_bp)

    from .products import bp as products_bp
    app.register_blueprint(products_bp)

    from .cart import bp as cart_bp
    app.register_blueprint(cart_bp)

    @app.template_filter()
    def format_date(value, format='medium'):
        """
        Custom filter to help format dates in HTML
        """
        if format == 'full':
            format="EEEE, d. MMMM y 'at' HH:mm"
        elif format == 'medium':
            format="EE dd.MM.y HH:mm"
        elif format == 'standard':
            format="MMM d, y"
        return format_datetime(value, format)

    return app


    