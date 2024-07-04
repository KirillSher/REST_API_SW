from datetime import datetime

import requests
from flask import render_template, request, redirect, flash, url_for, jsonify
from flask_login import login_user, login_required, logout_user, current_user
# from flask_sqlalchemy import session
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

from app import app, login_manager, Session
from app.models import User

session = Session()

@login_manager.user_loader
def load_user(user_id):
    user = session.query(User).filter(User.id == user_id).first()
    return user


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login/", methods=['GET', 'POST'])
def login():
    login = request.form.get("login")
    email = request.form.get("email")
    password = request.form.get("password")

    if login and password:
        user = session.query(User).filter_by(login=login).first()

        if user and check_password_hash(user.password, password):
            login_user(user)

            next = request.args.get("next")

            return redirect(next or url_for("index"))
        else:
            flash("Login or password is not correct")
    else:
        flash("error")

    return render_template("login.html")


@app.route("/register/", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        login = request.form["login"]
        email = request.form["email"]
        password = request.form["password"]
        password_repeat = request.form["password_repeat"]

        if not (login or email or password or password_repeat):
            flash("Please, fill all fields")
        elif password != password_repeat:
            flash("Password are not equal!")
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, email=email, password=hash_pwd, created_at=datetime.now())
            session.add(new_user)
            session.commit()

            return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/logout/", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect("index")


@app.errorhandler(404)
def page_not_found(e):
    if current_user.is_anonymous:
        return redirect(url_for("login", next=request.path))
    return "Page not found", 404


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 404:
        return redirect(url_for("login") + "?next=" + request.url)

    return response


def get_all_characters(type, page=1):
    characters = []
    swapi_url = f"https://swapi.dev/api/{type}/?page={page}"
    response = requests.get(swapi_url)

    if response.status_code == 200:
        data = response.json()
        characters = data['results']
        prev_page = data['previous'].split('=')[-1] if data['previous'] else None
        next_page = data['next'].split('=')[-1] if data['next'] else None

    return characters, prev_page, next_page


@app.route("/people/")
def people():
    page = int(request.args.get('page', 1))
    characters, prev_page, next_page = get_all_characters(type="people", page=page)
    return render_template('people.html', characters=characters, prev_page=prev_page,
                           next_page=next_page, page=page)


@app.route("/planets/")
def planets():
    page = int(request.args.get('page', 1))
    characters, prev_page, next_page = get_all_characters(type="planets", page=page)
    return render_template('planets.html', characters=characters, prev_page=prev_page,
                           next_page=next_page, page=page)


def delete_character():
    pass


@app.route("/starships/")
def starships():
    page = int(request.args.get('page', 1))
    characters, prev_page, next_page = get_all_characters(type="starships", page=page)
    return render_template('starships.html', characters=characters, prev_page=prev_page,
                           next_page=next_page, page=page)


def search_url(url, info_type, count):
    if info_type == 'film':
        res = []
        for i in range(count):
            response = requests.get(url[i])
            if response.status_code == 200:
                character = response.json()
                res.append(character['title'])
    else:
        res = []
        print(count)
        for i in range(count):
            if info_type == 'homeworld':
                response = requests.get(url)
            else:
                response = requests.get(url[i])
            if response.status_code == 200:
                character = response.json()
                res.append(character['name'])

    return res


@app.route("/info_character/")
def info_character():
    info_type = request.args.get('info_type', '')
    info_id = request.args.get('info_id', '')
    page = request.args.get('page', 1)
    swapi_url = f"https://swapi.dev/api/{info_type}/{info_id}/"
    response = requests.get(swapi_url)

    if response.status_code == 200:
        character = response.json()
        object_film = search_url(character["films"], 'film', len(character["films"]))

        if info_type == 'people':
            object_homeworld = search_url(character["homeworld"], 'homeworld', 1)
            object_vehicles = search_url(character["vehicles"], 'vehicles', len(character["vehicles"]))
            object_starships = search_url(character["starships"], 'starships', len(character["starships"]))
            return render_template('info_character.html', character=character, info_type=info_type,
                                   object_film=object_film, object_homeworld=object_homeworld,
                                   object_vehicles=object_vehicles, object_starships=object_starships, page=page)

        if info_type == 'planets':
            object_residents = search_url(character["residents"], 'residents', len(character["residents"]))

            return render_template('info_character.html', character=character, info_type=info_type,
                                   object_film=object_film, object_residents=object_residents, page=page)

        if info_type == 'starships':
            object_pilots = search_url(character["pilots"], 'pilots', len(character["pilots"]))

            return render_template('info_character.html', character=character, info_type=info_type,
                                   object_film=object_film, object_pilots=object_pilots, page=page)
    else:
        return jsonify(dict(error='Character not found')), 404
