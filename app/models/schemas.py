from app import ma
from .user import User
from .restaurant import Restaurant

class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id","email", "name", "username", "usertype_id")

class RestaurantSchema(ma.Schema):
    class Meta:
        # Fields to expose, add more if needed.
        fields = ("id", "name", "userid")

class UserTypeSchema(ma.Schema):
    class Meta:
        # Fields to expose, add more if needed.
        fields = ("id", "type")