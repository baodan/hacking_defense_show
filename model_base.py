from app.database import db
from datetime import date, datetime
from decimal import Decimal

class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)

    def to_dict(self):
        def convert_datetime(value):
            if value:
                return value.strftime("%Y-%m-%d %H:%M:%S")
            else:
                return ""
    
        for col in self.__table__.columns:
            if isinstance(col.type, datetime):
                value = convert_datetime(getattr(self, col.name))
            elif isinstance(col.type, Decimal):
                value = float(getattr(self, col.name))
            else:
                value = getattr(self, col.name, None)
            yield (col.name, value)


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified_at = db.Column(db.DateTime, default=db.func.current_timestamp(),
                            onupdate=db.func.current_timestamp())

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}