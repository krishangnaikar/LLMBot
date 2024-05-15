from flask import Flask
try:
    from views import views
except ModuleNotFoundError:
    from website.views import views


app = Flask(__name__)
app.register_blueprint(views, url_prefix="/")
app.secret_key = 'set a secret key'




if __name__ == "__main__":
    app.run(debug=True, port=8000)

