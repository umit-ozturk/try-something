"""Models for the auth API."""
from flask_sqlalchemy import SQLAlchemy  # type: ignore

db = SQLAlchemy()


class Users(db.Model):  # type: ignore
    __tablename__ = "users"
    account = db.Column(db.String, primary_key=True)
    active = db.Column(db.Boolean, nullable=False, default=False)
    scopes = db.Column(db.ARRAY(db.String))
    data = db.Column(db.JSON)

    def __repr__(self):
        return "<Users account=%r, active=%r, scopes=%r, data=%r>" % (  # pragma: nocover
            self.account,
            self.active,
            self.scopes,
            self.data
        )
