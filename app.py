from cassandra.cluster import Cluster
cluster = Cluster(contact_points=['172.17.0.2'],port=9042)
session = cluster.connect()


from random import randint
from time import strftime
from flask import Flask, render_template, flash, request, jsonify
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import requests
import time
from time import gmtime, strftime

insert_data = session.prepare("INSERT INTO recipe.stats (Time, Recipe, Ingredients) VALUES(?,?,?)")

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'SjdnUends821Jsdlkvxh391ksdODnejdDw'

class ReusableForm(Form):
    Recipe = TextField('Recipe:', validators=[validators.required()])
    Seconds = TextField('Seconds:', validators=[validators.required()])


@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)

    if request.method == 'POST':
        
        Recipe=request.form['Recipe']
        Ingredients=request.form['Seconds']

        url = "http://www.recipepuppy.com/api/"
        data = {
            'i': str(Ingredients),
            'q': str(Recipe)          
            }

        resp = requests.get(url, params=data)       
        if resp.ok:
            data = resp.json()
            for i in range (1,len(data['results'])):
                Title = data['results'][i]['title']
                link =  str(data['results'][i]['href']) 
                ingredients = str(data['results'][i]['ingredients'])       
                Time = str(strftime("%a, %d %b %Y %H:%M:%S", gmtime()))
                
                flash(f'####{Title}#### ---> {str(ingredients)} ####Recipe#### ---> {link}')
                session.execute(insert_data,[Time,Recipe,Ingredients])
        else:
            print(resp.reason)    

    return render_template('index.html', form=form)

##Through URL
@app.route("/recipes", methods=['GET']) #REST api Get method
def profile():
    boxes = session.execute( 'Select * From recipe.stats')
    recipes=[]
    for box in boxes:
        recipes.append(box.recipe)
    return (str(recipes))

##remaining three via curl
@app.route("/recipes", methods=['POST']) #REST api POST method
def create():
    time = str(strftime("%a, %d %b %Y %H:%M:%S", gmtime()))
    session.execute(f"INSERT INTO recipe.stats(recipe, time, ingredients) VALUES('{request.json['Recipe']}','{time}', '{request.json['Ingredients']}');")
    return jsonify({'message': 'created: /recipes/{}'.format(request.json['Recipe'])}), 201

@app.route('/recipes',  methods=['PUT']) #REST api PUT method
def update():
    time = str(strftime("%a, %d %b %Y %H:%M:%S", gmtime()))
    session.execute(f"UPDATE recipe.stats SET time = '{time}', ingredients = '{request.json['Ingredients']}' WHERE recipe = '{request.json['Recipe']}'")
    return jsonify({'message': 'updated: /recipes/{}'.format(request.json['Recipe'])}), 200

@app.route('/recipes',  methods=['DELETE']) #REST api DELETE method
def delete():
    session.execute("""DELETE FROM recipe.stats WHERE Recipe= '{}'""".format(request.json['Recipe']))    
    return jsonify({'message': 'deleted: /recipes/{}'.format(request.json['Recipe'])}), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=443,ssl_context=('cert.pem', 'key.pem'))
    #app.run(host='0.0.0.0',port=80) for http