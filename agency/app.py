import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Movies, Actors
from auth.auth import AuthError, requires_auth


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app,  resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true'
        )
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PATCH,POST,DELETE,OPTIONS'
        )
        return response

    # ROUTES

    # GET /Movies.. / Actors..
    # GET /Movies..  /Actors by id
    # it should be a public endpoint
    @app.route('/movies')
    def get_movies():
        try:
            movie = Movies.query.all()
            movie_form = [movies.format() for movies in movie]

            return jsonify({
                'success': True,
                'movies': movie_form,
                'total': len(movie_form)
            }), 200
        except BaseException:
            abort(404)

    @app.route('/actors')
    def get_actors():
        try:
            actor = Actors.query.all()
            actor_form = [actors.format() for actors in actor]

            return jsonify({
                'success': True,
                'actors': actor_form,
                'total': len(actor_form),
            }), 200
        except BaseException:
            abort(404)

    @app.route('/actors/<int:id>')
    def get_actor_by_id(id):
        try:
            actor = Actors.query.get(id)
            return jsonify({
                "success": True,
                "actor": actor.format()
            }), 200
        except BaseException:
            abort(404)

    @app.route('/movies/<int:id>')
    def get_movie_by_id(id):
        try:
            movie = Movies.query.get(id)
            return jsonify({
                "success": True,
                "movie": movie.format()
            }), 200
        except BaseException:
            abort(404)

    # POST /Movies.. /actors..
    # it create a new row in the Movies table
    # it require the 'post:movies' permission
    @app.route('/movies', methods=['POST'])
    # only authorized users can perform this post.
    @requires_auth('post:movies')
    def create_movie(payload):
        body = request.get_json()
        if "title" not in body:
            abort(422)
        try:
            new_movie = Movies(title=body["title"],
                               release_date=body["release_date"])
            new_movie.insert()
            return jsonify({
                'success': True,
                'movie': new_movie.format()
            }), 200
        except BaseException:
            abort(400)

    @app.route('/actors', methods=['POST'])
    # only authorized users can perform this post.
    @requires_auth('post:actors')
    def create_actor(payload):
        body = request.get_json()
        if "name" not in body:
            abort(422)
        try:
            new_actor = Actors(name=body['name'],
                               age=body['age'], gender=body['gender'])
            new_actor.insert()
            actor_form = new_actor.format()
            return jsonify({
                'success': True,
                'actor': actor_form
            }), 200
        except BaseException:
            abort(400)
    # PATCH /movies/<int:id>.. /actors/<int:id>
    # where <id> is the existing model id
    # it respond with a 404 error if <id> is not found
    # it update the corresponding row for <id>
    # it require the 'patch:movies' permission

    @app.route('/movies/<int:id>', methods=['PATCH'])
    # only authorized users can perform this patch.
    @requires_auth('patch:movies')
    def update_movies(payload, id):
        movie = Movies.query.get_or_404(id)
        if movie is None:
            abort(404)
        body = request.get_json()
        try:
            if "title" in body:
                movie.title = body["title"]
            if "release_date" in body:
                movie.release_date = body["release_date"]
            movie.update()
            return jsonify({
                'success': True,
                'movies': movie.format(),
            }), 200

        except BaseException:
            abort(422)

    @app.route('/actors/<int:id>', methods=['PATCH'])
    # only authorized users can perform this patch.
    @requires_auth('patch:actors')
    def update_actors(payload, id):
        actor = Actors.query.get_or_404(id)
        if actor is None:
            abort(404)
        body = request.get_json()
        try:
            if "name" in body:
                actor.name = body['name']
            if "age" in body:
                actor.age = body['age']
            if "gender" in body:
                actor.gender = body['gender']
            actor.update()
            return jsonify({
                'success': True,
                'actors': actor.format(),
            }), 200

        except BaseException:
            abort(422)
    # DELETE /movies/<int:id>.. /actors/<int:id>
    # where <id> is the existing model id
    # it should respond with a 404 error if <id> is not found
    # it should delete the corresponding row for <id>
    # it should require the 'delete:movies' permission

    @app.route('/movies/<int:id>', methods=['DELETE'])
    # only authorized users can perform this delete.
    @requires_auth('delete:movies')
    def delete_movie(payload, id):
        try:
            movie = Movies.query.get(id)
            if movie is None:
                abort(404)
            movie.delete()
            return jsonify({
                'success': True,
                'deleted Movie id': id,
            }), 200

        except BaseException:
            abort(422)

    @app.route('/actors/<int:id>', methods=['DELETE'])
    # only authorized users can perform this delete.
    @requires_auth('delete:actors')
    def delete_actor(payload, id):
        try:
            actor = Actors.query.get(id)
            if actor is None:
                abort(404)
            actor.delete()
            return jsonify({
                'success': True,
                'deleted actor id': id,
            }), 200

        except BaseException:
            abort(422)

    # Error Handling

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not Found"
        }), 404

    @app.errorhandler(400)
    def badRequest(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    return app


app = create_app()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
