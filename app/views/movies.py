from flask import request
from flask_restx import Resource, Namespace

from app.db_init import db
from app.models import MovieSchema, Movie

movie_ns = Namespace('movies')
movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        try:
            genre_id = request.args.get('genre_id')
            director_id = request.args.get('director_id')
            if director_id and genre_id:
                movies = Movie.query.filter(Movie.director_id == director_id).filter(Movie.genre_id == genre_id)
                return movies_schema.dump(movies)
            if genre_id:
                movies_by_genre = Movie.query.filter(Movie.genre_id == genre_id)
                return movies_schema.dump(movies_by_genre)
            if director_id:
                movies_by_director = Movie.query.filter(Movie.director_id == director_id)
                return movies_schema.dump(movies_by_director)
            else:
                all_movies = Movie.query.all()
                return movies_schema.dump(all_movies), 200
        except Exception as e:
            return 'неверное значение', 404

    def post(self):
        request_json = request.json
        new_movie = Movie(**request_json)

        with db.session.begin():
            db.session.add(new_movie)
        return "", 201


@movie_ns.route('/<int:id>')
class MovieView(Resource):
    def get(self, id):
        movie = Movie.query.get(id)
        if not movie:
            return "", 404
        return movie_schema.dump(movie), 200

    def put(self, id):
        updated_figures = db.session.query(Movie).filter(Movie.id == id).update(request.json)
        if updated_figures != 1:
            return "", 400

        db.session.commit()

        return "", 204

    def delete(self, id):
        deleted_figures = db.session.query(Movie).get(id)

        if not deleted_figures:
            return "", 400

        db.session.delete(deleted_figures)
        db.session.commit()

        return "", 204
