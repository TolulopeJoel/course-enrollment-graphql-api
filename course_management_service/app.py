#!/usr/bin/env python
from flask import Flask
from flask_graphql import GraphQLView

from .database import db_session, init_db
from .schema import schema

app = Flask(__name__)
app.debug = True


app.add_url_rule(
    "/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.cli.command("init-db")
def init_db_command():
    init_db()


if __name__ == "__main__":
    try:
        init_db()
    except Exception as e:
        print(f"Failed to initialize the database: {e}")
    app.run()
