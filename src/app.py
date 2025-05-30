from flask import Flask
from flask_migrate import Migrate
from src.models import db
from src.routes import api
from src.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)
    app.register_blueprint(api, url_prefix='/')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)