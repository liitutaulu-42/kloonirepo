from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# from dotenv import load_dotenv
# from os import getenv
#
# load_dotenv()
#
# test_env = getenv("TEST_ENV") == "true"
# print(f"Test environment: {test_env}")
#
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://postgres:postgres@localhost:5432/postgres"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
