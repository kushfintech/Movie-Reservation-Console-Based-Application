import unittest
from controllers.movie_controller import add_movie, remove_movie


class TestMovieController(unittest.TestCase):

    def test_add_movie(self):
        result = add_movie(title="New Movie", duration="120")
        self.assertTrue(result)

    def test_remove_movie(self):
        result = remove_movie(movie_id=1)  # Use an appropriate movie_id
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
