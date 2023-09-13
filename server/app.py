#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.filter(Animal.id == id).first()

    if not animal:
        response_body = '<ul>404 Error. Animal not found.</ul>'
        status_code = 404
        return make_response(response_body, status_code)

    response_body = f"""
    <ul>ID: {animal.id}</ul>
    <ul>Name {animal.name}</ul>
    <ul>Species:  {animal.species}</ul>
    <ul>Zookeeper: {animal.zookeeper.name}</ul>
    <ul>Enclosure: {animal.enclosure.environment}-{animal.enclosure.id}</ul>
    """
    status_code = 200
    return make_response(response_body, status_code)

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.filter(Zookeeper.id == id).first()

    if not zookeeper:
        response_body = '<ul>404 Error. Zookeeper not found.</ul>'
        status_code = 404
        return make_response(response_body, status_code)

    response_body = f"""
    <ul>ID: {zookeeper.id}</ul>
    <ul>Name: {zookeeper.name}</ul>
    <ul>Birthday: {zookeeper.birthday}</ul>
    """

    animals = [animal for animal in zookeeper.animals]
    if not animals:
        response_body += '<ul>This zookeeper does not have any animals in their care at this time</ul>'
    else:
        for animal in animals:
            response_body += f'<ul>Animal: {animal.name} the {animal.species}</ul>'

    status_code = 200
    return make_response(response_body, status_code)

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.filter(Enclosure.id == id).first()

    if not enclosure:
        response_body = '<ul>404 Error. Enclosure not found.</ul>'
        status_code = 404
        return make_response(response_body, status_code)

    response_body = f"""
    <ul>ID: {enclosure.id}</ul>
    <ul>Environment:  {enclosure.environment}</ul>
    <ul>Open to visitors: {"True" if enclosure.open_to_visitors else "False"}</ul>
    """

    animals = [animal for animal in enclosure.animals]
    if not animals:
        response_body += '<ul>This enclosure does not have any residents at this time</ul>'
    else:
        for animal in animals:
            response_body += f'<ul>Animal: {animal.name} the {animal.species}</ul>'

    status_code = 200
    return make_response(response_body, status_code)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
