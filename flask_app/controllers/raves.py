from flask import render_template, session,flash,redirect, request
from flask_app import app
from flask_app.models.user import User
from flask_app.models.rave import Rave
import os,requests


@app.route('/new/rave') # route to create rave
def new_rave():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('new_rave.html',user=User.get_by_id(data))


@app.route('/create/rave/ajax',methods=['POST'])  #create new rave
def create_rave():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Rave.validate_rave(request.form):
        return redirect('/new/rave')
    data = {
        "name": request.form["name"],
        "djs": request.form['djs'],
        "address": request.form["address"],
        "city":request.form['city'],
        "state":request.form['state'],
        "date": request.form["date"],
        "user_id": session["user_id"]
    }
    Rave.save(data)
    return redirect('/dashboard')

@app.route('/edit/rave/<int:id>') # route to edit rave
def edit_rave(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_rave.html",edit=Rave.get_one(data),user=User.get_by_id(user_data))

@app.route('/update/rave/<int:id>',methods=['POST']) #update rave
def update_rave(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Rave.validate_rave(request.form):
        return redirect(f'/edit/rave/{id}')
    data = {
        "id": request.form['id'],
        "name": request.form["name"],
        "djs": request.form["djs"],
        "adress": request.form["adress"],
        "city": request.form['city'],
        "state":request.form['state'],
        "date":request.form['date']
    }
    Rave.update(data)
    return redirect('/dashboard')


@app.route('/rave/<int:id>')
def show_rave(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    all_users= User.get_users_like_same_rave(data)
    rave = Rave.get_one(data)
    user = User.get_by_id(user_data)
    print (rave)
    address = rave.address
    city = rave.city
    api_key = os.environ.get("API_KEY")
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}{city}&key={api_key}"
    response = requests.get(url)
    map ={
            'lat': response.json()['results'][0]['geometry']['location']['lat'],
            'lng': response.json()['results'][0]['geometry']['location']['lng']
        }
    print(map)
    return render_template("detail.html",rave=rave,user=user,all_users=all_users,map=map)

@app.route('/rave/<int:rave_id>/join',methods = ['post'])
def join(rave_id):
    joiner_data ={
        'user_id':session['user_id'],
        "rave_id":rave_id
    }
    Rave.going_rave(joiner_data)
    return redirect('/dashboard')

@app.route('/rave/<int:rave_id>/quit',methods = ['post'])
def quit(rave_id):
    quiter_data ={
        'user_id':session['user_id'],
        "rave_id":rave_id
    }
    Rave.quit_rave(quiter_data)
    return redirect('/dashboard')



@app.route('/destroy/rave/<int:id>', methods = ['post']) #destroy rave
def destroy_rave(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Rave.destroy(data)
    return redirect('/dashboard')
