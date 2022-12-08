import datetime
import os
import sqlite3

import jwt
from flask import Flask, request, g

server = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect("db.sqlite3")
    conn.row_factory = sqlite3.Row
    return conn


@server.route("/login/", methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "Missing credentials", 401

    # Check db for username and password
    cur = get_db_connection().cursor()
    res = cur.execute(
        f"SELECT email, password FROM users WHERE email=?", (auth.username,)
    )
    if res:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]

        if auth.username != email or auth.password != password:
            return "Invalid credentials", 401
        else:
            return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)
    else:
        return "Invalid credentials", 401


@server.route("/validate/", methods=["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]

    if not encoded_jwt:
        return "Missing credentials", 401

    encoded_jwt = encoded_jwt.split(" ")[1]

    try:
        decoded = jwt.decode(
            encoded_jwt,
            os.environ.get("JWT_SECRET"),
            algorithms=["HS256"],
        )
    except:
        return "Not authorize", 403
    return decoded, 200


def createJWT(username, secret, authz):
    return jwt.encode(
        {
            "username": username,
            "expiration": str(
                datetime.datetime.now(datetime.timezone.utc)
                + datetime.timedelta(days=1)
            ),
            "iat": datetime.datetime.utcnow(),
            "admin": authz,
        },
        secret,
        algorithm="HS256",
    )


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=4000)
