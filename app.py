from flask import Flask
from routes import urls_blueprint, login_manager

app = Flask(__name__)
app.register_blueprint(urls_blueprint)
app.config["SECRET_KEY"] = "paçoca"

login_manager.init_app(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0')