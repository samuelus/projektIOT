import connexion
from flask_cors import CORS
from swagger_server import encoder
from swagger_server.frontend_routing.routes import setup_routes

if __name__ == '__main__':
    app = connexion.App(__name__, specification_dir='swagger_server/swagger/')
    flask_app = app.app
    flask_app.template_folder = 'ui'
    flask_app.static_folder = 'ui'
    CORS(flask_app)
    flask_app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'IOT Project - OpenAPI 3.0'}, pythonic_params=True)
    setup_routes(flask_app)

    app.run(port=8080)
