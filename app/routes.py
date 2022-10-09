from app import db
from flask import current_app as app, request
from flask_restx import Api, Resource
from . import models
from sqlalchemy import or_

api = Api(app)
movies_ns = api.namespace('movies')
directors_ns = api.namespace('directors')
genres_ns = api.namespace('genres')

movies_scheme = models.MovieSchema(many=True)
movie_scheme = models.MovieSchema()
directors_scheme = models.DirectorSchema(many=True)
director_scheme = models.DirectorSchema()
genres_scheme = models.DirectorSchema(many=True)
genre_scheme = models.DirectorSchema()


@movies_ns.route('/')
class MoviesView(Resource):
    def get(self):
        director_id = None
        genre_id = None
        args = request.args

        if "director_id" in args:
            director_id = args.get("director_id")

        if "genre_id" in args:
            genre_id = args.get("genre_id")

        data = db.session.query(models.Movie)

        if director_id is not None:
            data = data.filter(models.Movie.director_id == director_id)

        if genre_id is not None:
            data = data.filter(models.Movie.genre_id == genre_id)

        return movies_scheme.dump(data.all()), 200

    def post(self):
        req_json = request.json
        model = models.Movie(**req_json)
        with db.session.begin():
            db.session.add(model)

        return "", 201


@movies_ns.route('/<int:id>')
class MovieView(Resource):
    def get(self, id: int):
        try:
            data = db.session.query(models.Movie).filter(models.Movie.id == id).one()
            return movie_scheme.dupm(data), 200
        except Exception as e:
            return str(e), 404

    def put(self, id: int):
        model = db.session.query(models.Movie).get(id)
        req_json = request.json

        model.title = req_json.get("title")
        model.trailer = req_json.get("trailer")
        model.description = req_json.get("description")
        model.raiting = req_json.get("raiting")
        model.genre_id = req_json.get("genre_id")
        model.director_id = req_json.get("director_id")

        db.session.add(model)
        db.session.commit()

        return "", 204

    def patch(self, id: int):
        model = db.session.query(models.Movie).get(id)
        req_json = request.json

        if "title" in req_json:
            model.title = req_json.get("title")
        if "trailer" in req_json:
            model.trailer = req_json.get("trailer")
        if "description" in req_json:
            model.description = req_json.get("description")
        if "raiting" in req_json:
            model.raiting = req_json.get("raiting")
        if "genre_id" in req_json:
            model.genre_id = req_json.get("genre_id")
        if "director_id" in req_json:
            model.director_id = req_json.get("director_id")

        db.session.add(model)
        db.session.commit()

        return "", 204

    def delete(self, id: int):
        model = db.session.query(models.Movie).get(id)

        db.session.delete(model)
        db.session.commit()

        return "", 204


@directors_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        data = db.session.query(models.Director).all()
        return directors_scheme.dump(data), 200

    def post(self):
        req_json = request.json
        model = models.Director(**req_json)
        with db.session.begin():
            db.session.add(model)

        return "", 201


@directors_ns.route('/<int:id>')
class DirectorView(Resource):
    def get(self, id: int):
        try:
            data = db.session.query(models.Director).filter(models.Director.id == id).one()
            return genre_scheme.dupm(data), 200
        except Exception as e:
            return str(e), 404

    def put(self, id: int):
        model = db.session.query(models.Director).get(id)
        req_json = request.json

        model.name = req_json.get("name")

        db.session.add(model)
        db.session.commit()

        return "", 204

    def delete(self, id: int):
        model = db.session.query(models.Director).get(id)

        db.session.delete(model)
        db.session.commit()

        return "", 204

@genres_ns.route('/')
class GenresView(Resource):
    def get(self):
        data = db.session.query(models.Genre).all()
        return genres_scheme.dump(data), 200

    def post(self):
        req_json = request.json
        model = models.Genre(**req_json)
        with db.session.begin():
            db.session.add(model)

        return "", 201


@genres_ns.route('/<int:id>')
class GenreView(Resource):
    def get(self, id: int):
        try:
            data = db.session.query(models.Genre).filter(models.Genre.id == id).one()
            return genre_scheme.dupm(data), 200
        except Exception as e:
            return str(e), 404

    def put(self, id: int):
        model = db.session.query(models.Genre).get(id)
        req_json = request.json

        model.name = req_json.get("name")

        db.session.add(model)
        db.session.commit()

        return "", 204

    def delete(self, id: int):
        model = db.session.query(models.Genre).get(id)

        db.session.delete(model)
        db.session.commit()

        return "", 204

