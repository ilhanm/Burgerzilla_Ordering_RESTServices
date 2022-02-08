from flask import current_app
from app.models.schemas import RestaurantSchema
from app.utils import err_resp,internal_err_resp,message
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.restaurant import Restaurant
from app import db


class RestaurantService:
    @staticmethod
    def get_by_id(restaurant_id):
        """
        get a restaurant by id"""
        if not (restaurant := Restaurant.query.get(restaurant_id)):
            return err_resp(message="Restaurant not found",status=400)
        from .utils import load_data
        try:
            restaurant_data = load_data(restaurant)
            resp=message(True,"Restaurant loaded successfully")
            resp["restaurant"]=restaurant_data
            return resp,200
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()

    @staticmethod
    def delete_by_id(restaurant_id):    
        """
        Delete a restaurant by id"""
        if not (restaurant := Restaurant.query.get(restaurant_id)):
            return err_resp(message="Restaurant not found",status=400)
        try:
            db.session.delete(restaurant)
            db.session.commit()
            return message(True,"Restaurant deleted successfully")
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()

    @staticmethod
    def create(user_id,restaurant_data):
        """
        Create a new restaurant"""
        try:
            from .utils import load_data
            current_user = get_jwt_identity()
            restaurant = Restaurant(name=restaurant_data["name"],userid=current_user)
            db.session.add(restaurant)
            db.session.commit()
            return message(True,"Restaurant created successfully")
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()

    @staticmethod
    def update_by_id(restaurant_id,restaurant_data):
        """
        update a restaurant by id"""
        if not (restaurant:=Restaurant.query.get(restaurant_id)):
            return err_resp(message="Restaurant not found",status=400)
        try:
            Restaurant.query.filter_by(id=restaurant_id).update(restaurant_data)
            db.session.commit()
            return message(True,"Restaurant updated successfully")
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()
        
    @staticmethod
    def get_all(user_id):
        """
        Get all restaurants of a specific user"""
        if not(restaurants := Restaurant.query.filter_by(userid=user_id)):
            return err_resp(message="restaurants not found",status=400)
        from .utils import load_data
        try:
            restaurants_data = [load_data(restaurant) for restaurant in restaurants]
            resp=message(True,"Restaurants loaded successfully")
            resp["restaurants"]=restaurants_data
            return resp,200
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()