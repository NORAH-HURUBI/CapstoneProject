import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movies, Actors



class AgencyTestCase(unittest.TestCase):
    """This class represents the Agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = "postgres://{}:{}@{}/{}".format(
            'postgres', 'misk', 'localhost:5432', "agency_test")
        self.director_jwt = os.environ['director_jwt']
        self.producer_jwt = os.environ['producer_jwt']
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_retrieve_movies(self):
        movie = Movies(title="test movie", release_date="10 oct 2009")
        movie.insert()

        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_retrieve_actors(self):
        actor = Actors(name="test name", age="45", gender="male")
        actor.insert()

        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        actors = Actors.query.all()
        self.assertEqual(len(data['actors']), len(actors))

    def test_create_movie_with_success_jwt(self):
        test_data = {
            'title': "test moviename",
            'release_date': "20 oct 2020",
        }
        res = self.client().post('/movies', json=test_data,
                                 headers={'Authorization': f'Bearer {self.producer_jwt}'})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_movie_with_failed_jwt(self):
        test_data = {
            'title': "test moviename",
            'release_date': "20 sep 2012",
        }
        res = self.client().post('/movies', json=test_data,
                                 headers={"Content-Type": "application/json",
                                          "Authorization": "Bearer" + self.director_jwt})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_create_actor_with_success_jwt(self):
        test_data = {
            'name': 'test',
            'age': '22',
            'gender': 'female'
        }
        res = self.client().post('/actors', json=test_data,
                                 headers={'Authorization': f'Bearer {self.director_jwt}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_movie_missing_fileds(self):

        test_data = {
            'release_date': "13 sep 2014"
        }
        res = self.client().post('/movies', json=test_data,
                                 headers={'Authorization': f'Bearer {self.producer_jwt}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_create_actor_missing_fileds(self):
        test_data = {
            'age': '22'
        }
        res = self.client().post('/actors', json=test_data,
                                 headers={'Authorization': f'Bearer {self.producer_jwt}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_delete_movie(self):
        test_movie = Movies(title='test title', release_date='20 oct 2020')
        test_movie.insert()
        test_movie_id = test_movie.id

        res = self.client().delete(f'/movies/{test_movie_id}',
                                   headers={'Authorization': f'Bearer {self.producer_jwt}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actor(self):
        test_actor = Actors(name="test name", age="55", gender="male")
        test_actor.insert()
        test_actor_id = test_actor.id

        res = self.client().delete(f'/actors/{test_actor_id}',
                                   headers={'Authorization': f'Bearer {self.director_jwt}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_movie_not_exist(self):

        res = self.client().delete('/movies/9980',
                                   headers={'Authorization': f'Bearer {self.producer_jwt}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_delete_actor_not_exist(self):

        res = self.client().delete('/actors/8888',
                                   headers={'Authorization': f'Bearer {self.producer_jwt}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_update_existing_actor_data(self):
        actor = Actors(name="test name", age="50", gender="female")
        actor.insert()
        test_actor_id = actor.id
        actor_update = {
            'gender': 'male'
        }
        res = self.client().patch(
            f'/actors/{test_actor_id}',
            json=actor_update,
            headers={'Authorization': f'Bearer {self.producer_jwt}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_not_update_actor__not_found(self):
        test_data = {
            'age': '23'
        }

        res = self.client().patch('/actors/8888', json=test_data,
                                  headers={'Authorization': f'Bearer {self.producer_jwt}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertFalse(data['success'])

    def test_update_existing_movie_data(self):
        movie = Movies(title="test title", release_date="3 jun 2012")
        movie.insert()

        movie_update = {
            'title': 'new test'
        }

        res = self.client().patch(f'/movies/{movie.id}', json=movie_update,
                                  headers={'Authorization': f'Bearer {self.producer_jwt}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_not_update_movie__not_found(self):
        test_data = {
            'title': 'test'
        }
        res = self.client().patch('/movies/8888', json=test_data,
                                  headers={'Authorization': f'Bearer {self.producer_jwt}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertFalse(data['success'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
