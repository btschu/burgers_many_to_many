from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import topping

db = "burgers_many_to_many"

class Burger:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.bun = data['bun']
        self.meat = data['meat']
        self.calories = data['calories']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.restaurant_id = data['restaurant_id']

        self.toppings = []

    @classmethod
    def save(cls,data):
        query = '''
        INSERT INTO burgers (name, bun, meat, calories, restaurant_id)
        VALUES (%(name)s, %(bun)s, %(meat)s, %(calories)s, %(restaurant_id)s);'''
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def get_all_burgers(cls):
        query = 'SELECT * FROM burgers;'
        burgers_from_db =  connectToMySQL(db).query_db(query)
        burgers =[]
        for b in burgers_from_db:
            burgers.append(cls(b))
        return burgers

    @classmethod
    def get_one(cls,data):
        query = '''
        SELECT * FROM burgers
        WHERE burgers.id = %(id)s;'''
        burger_from_db = connectToMySQL(db).query_db(query,data)

        return cls(burger_from_db[0])

    @classmethod
    def get_burger_with_toppings( cls , data ):
        query = '''
        SELECT * FROM burgers
        LEFT JOIN add_ons ON add_ons.burger_id = burgers.id
        LEFT JOIN toppings ON add_ons.topping_id = toppings.id
        WHERE burgers.id = %(id)s;'''
        results = connectToMySQL(db).query_db( query , data )
        # results will be a list of topping objects with the burger attached to each row. 
        burger = cls( results[0] )
        for row_from_db in results:
            # Now we parse the topping data to make instances of toppings and add them into our list.
            topping_data = {
                "id" : row_from_db["toppings.id"],
                "topping_name" : row_from_db["topping_name"],
                "created_at" : row_from_db["toppings.created_at"],
                "updated_at" : row_from_db["toppings.updated_at"]
            }
            burger.toppings.append( topping.Topping( topping_data ) )
        return burger

    @classmethod
    def update(cls,data):
        query = '''
        UPDATE burgers
        SET name=%(name)s, bun=%(bun)s, meat=%(meat)s, calories=%(calories)s
        WHERE id = %(id)s;'''
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query = 'DELETE FROM burgers WHERE id = %(id)s;'
        return connectToMySQL(db).query_db(query,data)
