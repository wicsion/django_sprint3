from sanic import Sanic
from .routes import init_routes


def create_app():
    app = Sanic("PaymentAPI")
    init_routes(app)
    return app