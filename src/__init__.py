import os
from flask import  request , jsonify
from flask_jwt_extended import JWTManager
from src.db import app
from src.authRoutes import authRoutes
from src.templateRoutes import templateRoutes
from src.constants.http_status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from flasgger import Swagger, swag_from
from src.config.swagger import template, swagger_config

def create_app(test_config=None):


    if test_config is None:
         app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY'),
            MONGO_URI=os.environ.get('MONGO_URI'),

            SWAGGER={
                'title': "Bookmarks API",
                'uiversion': 3
            }

        )
    else:
        app.config.from_mapping(test_config)

    JWTManager(app)
    app.register_blueprint(authRoutes)
    app.register_blueprint(templateRoutes)

    Swagger(app, config=swagger_config, template=template)
    @app.get('/')
    def home():
        return "Sloovi API"

    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({'error': 'Not found'}), HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({'error': 'Something went wrong, we are working on it'}), HTTP_500_INTERNAL_SERVER_ERROR
    

    return app

