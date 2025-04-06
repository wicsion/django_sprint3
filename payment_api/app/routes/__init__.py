from .users import user_bp
from .admin import admin_bp
from .payments import payment_bp

def init_routes(app):
    app.blueprint(user_bp)
    app.blueprint(admin_bp)
    app.blueprint(payment_bp)
