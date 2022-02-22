from flask_app.models import burger
from flask_app.config.mysqlconnection import connectToMySQL

db = "burgers_many_to_many"

class Topping:
    def __init__( self , data ):
        self.id = data['id']
        self.topping_name = data['topping_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.on_burgers = []

    @classmethod
    def save( cls , data ):
        query = '''
        INSERT INTO toppings (topping_name)
        VALUES (%(topping_name)s);'''
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_topping_with_burgers( cls , data ):
        query = '''SELECT * FROM toppings
        LEFT JOIN add_ons ON add_ons.topping_id = toppings.id 
        LEFT JOIN burgers ON add_ons.burger_id = burgers.id 
        WHERE toppings.id = %(id)s;'''
        results = connectToMySQL(db).query_db( query , data )
        # results will be a list of topping objects with the burger attached to each row. 
        topping = cls( results[0] )
        for row_from_db in results:
            # Now we parse the topping data to make instances of toppings and add them into our list.
            burger_data = {
                "id" : row_from_db["burgers.id"],
                "name" : row_from_db["name"],
                "bun" : row_from_db["bun"],
                "calories" : row_from_db["calories"],
                "created_at" : row_from_db["toppings.created_at"],
                "updated_at" : row_from_db["toppings.updated_at"]
            }
            topping.on_burgers.append( burger.Burger( burger_data ) )
        return topping