from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
from datetime import date

class Rave:
    db = 'rave_event_reminder'

    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.djs = data['djs']
        self.address = data['address']
        self.city = data["city"]
        self.state = data['state']
        self.date = data['date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None #this is going to be where the user object will be put later
        self.joiner = []

    @classmethod  #save query new rave
    def save(cls,data):
        query = "INSERT INTO raves (name, djs, address, city,state,date, user_id) VALUES (%(name)s,%(djs)s,%(address)s,%(city)s,%(state)s,%(date)s,%(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod # get all from table raves
    def get_all_rave(cls):
        query ="select * from raves left join users on users.id = raves.user_id left join joins on raves.id = joins.rave_id left join users as joiner on joins.user_id = joiner.id;"        #goal:  turn a list of dict into a list of objects with each rave object associated with a user object
        results =  connectToMySQL(cls.db).query_db(query) #list of dict
        all_raves = [] # list of objects
        for row in results:
            new_rave = True
            joiner_data ={
                'id': row['joiner.id'],
                'first_name': row['joiner.first_name'],
                'last_name': row['joiner.last_name'],
                'email': row['joiner.email'],
                'password': row['joiner.password'],
                'created_at': row['joiner.created_at'],
                'updated_at': row['joiner.updated_at'],
            }
            if len(all_raves)>0 and all_raves[len(all_raves)-1].id == row['id']:
                all_raves[len(all_raves)-1].joiner.append(user.User(joiner_data))
                new_rave = False
            if new_rave:
                # make a class instance of rave
                this_rave = cls(row)
                # make a data dict for the user
                user_info ={
                    'id': row['users.id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'password': row['password'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at'],
                }
                # make a user insance 
                this_user = user.User(user_info)
                # add that user object to the rave attribute "user"
                this_rave.user = this_user
                if row['joiner.id'] is not None:
                    this_rave.joiner.append(user.User(joiner_data))
                all_raves.append(this_rave)
                print(all_raves)
        return all_raves

    @classmethod  #get one rave by id
    def get_one(cls,data):
        query = "SELECT * FROM raves WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls( results[0] )

    @classmethod  #update rave
    def update(cls, data):
        query = "UPDATE raves SET name=%(name)s, djs=%(djs)s, address=%(address)s, city=%(city)s,state=%(state)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod  #delete raves
    def destroy(cls,data):
        query = "DELETE FROM raves WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod #get raves that relate to user
    def get_user_raves(cls,data):
        query = 'select * from raves left join users on raves.user_id = users.id where users.id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query,data)
        raves = []
        for rave in results:
            raves.append(cls(rave))
        return raves

    @classmethod
    def going_rave(cls,data):
        query = 'insert into joins (user_id,rave_id) values(%(user_id)s, %(rave_id)s);'
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def quit_rave(cls,data):
        query = 'delete from joins where rave_id=%(rave_id)s and user_id =%(user_id)s;'
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def raves_user_joined(cls,data):
        raves_joined = []
        query = "SELECT rave_id FROM joins JOIN users on users.id= user_id where user_id=%(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        for result in results:
            raves_joined.append(result['rave_id'])
        return raves_joined


    @staticmethod
    def validate_rave(rave):
        is_valid = True
        today = str(date.today())
        print(today)
        if len(rave['name']) < 3:
            is_valid = False
            flash("Rave Name must be at least 3 characters","rave")
        if len(rave['address']) < 6:
            is_valid = False
            flash("Address must be full address","rave")
        if len(rave['address']) == '':
            is_valid = False
            flash("Address cannot blank","rave")
        if len(rave['city']) < 4:
            is_valid = False
            flash ("City too short",'rave')
        if rave['date'] ==  '':
            is_valid = False
            flash("Please enter a date","rave")
        if rave['date'] < today:
            is_valid = False
            flash('Event day cannot be in the past','rave')
        return is_valid
