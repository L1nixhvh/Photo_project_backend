from app import app
from app.routes.auth import auth_Blueprint

app.register_blueprint(auth_Blueprint, url_prefix="/api/auth")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
