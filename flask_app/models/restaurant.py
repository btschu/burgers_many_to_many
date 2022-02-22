from flask_app.models import burger
from flask_app.config.mysqlconnection import connectToMySQL

db = "burgers_many_to_many"

class Restaurant:
    def __init__( self , db_data ):
        self.id = db_data['id']
        self.name = db_data['name']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

        self.burgers = []

    @classmethod
    def save( cls , data ):
        query = '''
        INSERT INTO restaurants (name)
        VALUES (%(name)s);'''
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def get_all_restaurants(cls):
        query = 'SELECT * FROM restaurants;'
        restaurants_from_db = connectToMySQL(db).query_db(query)
        restaurants = []
        for row in restaurants_from_db:
            restaurants.append(cls(row))
        return restaurants

    @classmethod
    def get_restaurant_with_burgers( cls , data ):
        query = '''
        SELECT * FROM restaurants
        LEFT JOIN burgers ON burgers.restaurant_id = restaurants.id
        WHERE restaurants.id = %(id)s;'''
        results = connectToMySQL(db).query_db( query , data )
        # results will be a list of topping objects with the burger attached to each row. 
        restaurant = cls( results[0] )
        for row_from_db in results:
            # Now we parse the burger data to make instances of burgers and add them into our list.
            burger_data = {
                "id" : row_from_db["burgers.id"],
                "name" : row_from_db["burgers.name"],
                "bun" : row_from_db["bun"],
                "meat" : row_from_db["meat"],
                "calories" : row_from_db["calories"],
                "created_at" : row_from_db["burgers.created_at"],
                "updated_at" : row_from_db["burgers.updated_at"]
            }
            restaurant.burgers.append( burger.Burger( burger_data ) )
        return restaurant