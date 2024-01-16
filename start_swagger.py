import connexion
from flask_cors import CORS
from swagger_server import encoder

if __name__ == '__main__':
    app = connexion.App(__name__, specification_dir='swagger_server/swagger/')
    CORS(app.app)
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'IOT Project - OpenAPI 3.0'}, pythonic_params=True)
    app.run(port=8080)