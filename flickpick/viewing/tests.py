from time import sleep

from django.contrib.auth.models import User, Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from movies.tests import make_movie
from movies.models import Movie
from viewing.models import Viewing


class TestViewingModel(TestCase):

    def setUp(self):
        self.user = User.objects.create_user("test", "test@example.com", "test")
        self.other_user = User.objects.create_user("other", "other@example.com", "other")

        for i in range(3):
            make_movie("test movie {}".format(i))

    def test_get_user(self):
        """
        Verify that ViewingManager.get_user() returns the correct user when accessed through a User instance,
        otherwise raises an exception
        """
        test_movie = Movie.objects.all()[0]

        with self.assertRaises(ValueError):
            Viewing.objects.get_user()
        self.assertEqual(self.user, self.user.seen_movies.get_user())

        with self.assertRaises(ValueError):
            Viewing.objects.add_movie(test_movie)
        self.user.seen_movies.add_movie(test_movie)  # no exception

    def test_has_perm(self):
        """
        Verify that the two has_perm methods report correctly
        """
        test_movie = Movie.objects.all()[0]

        self.assertFalse(Viewing.objects.user_has_seen_movie(self.user, test_movie))
        self.assertFalse(self.user.seen_movies.has_seen_movie(test_movie))

        self.user.seen_movies.add_movie(test_movie)

        self.assertTrue(Viewing.objects.user_has_seen_movie(self.user, test_movie))
        self.assertTrue(self.user.seen_movies.has_seen_movie(test_movie))

    def test_all_movies(self):
        """
        Verify that the two all_movies() methods return the full set of movies seen by a user, ordered by
        how recently the viewing record was created
        """
        movie1, movie2, movie3 = Movie.objects.all()

        self.user.seen_movies.add_movie(movie2)
        sleep(0.1)
        self.user.seen_movies.add_movie(movie3)
        sleep(0.1)
        self.user.seen_movies.add_movie(movie1)

        self.assertEqual(self.user.seen_movies.all_movies(), [movie1, movie3, movie2])
        self.assertEqual(Viewing.objects.all_movies_for_user(self.user), [movie1, movie3, movie2])

    def test_grant_perm(self):
        """
        Verify that the two grant_perm methods correctly create permissions
        """
        movie1, movie2, movie3 = Movie.objects.all()

        self.assertEqual(0, Viewing.objects.count())

        Viewing.objects.add_movie_to_user(self.user, movie1)
        self.assertEqual(1, Viewing.objects.count())

        self.user.seen_movies.add_movie(movie2)
        self.assertEqual(2, Viewing.objects.count())

        Viewing.objects.add_movie_to_user(self.user, movie2)
        self.assertEqual(2, Viewing.objects.count())

    def test_bulk_add_movies(self):
        """
        Verify that bulk_add_movies adds all permissions in the proper order
        """
        movie1, movie2, movie3 = Movie.objects.all()
        self.user.seen_movies.bulk_add_movies(movies=[movie1, movie3, movie2], max_retries=1)
        for movie in Movie.objects.all():
            self.assertTrue(self.user.seen_movies.has_seen_movie(movie))
        self.assertEqual(self.user.seen_movies.all_movies(), [movie2, movie3, movie1])

        self.assertEqual(3, Viewing.objects.count())

        Viewing.objects.add_movie_to_user(self.user, movie2)
        self.assertEqual(3, Viewing.objects.count())

    def test_bulk_add_movies_to_user(self):
        """
        Verify that bulk_add_movies_to_user adds all permissions in the proper order
        """
        movie1, movie2, movie3 = Movie.objects.all()
        Viewing.objects.bulk_add_movies_to_user(self.user, [movie1, movie3, movie2])
        for movie in Movie.objects.all():
            self.assertTrue(self.user.seen_movies.has_seen_movie(movie))
        self.assertEqual(self.user.seen_movies.all_movies(), [movie2, movie3, movie1])

        self.assertEqual(3, Viewing.objects.count())

        Viewing.objects.add_movie_to_user(self.user, movie2)
        self.assertEqual(3, Viewing.objects.count())

    def test_bulk_re_grant(self):
        """
        Verify that bulk_add_movies grants still work when a user already has already seen something in it
        """
        movie1, movie2, movie3 = Movie.objects.all()
        self.user.seen_movies.add_movie(movie2)
        self.user.seen_movies.bulk_add_movies([movie1, movie2, movie3])

        self.assertListEqual(self.user.seen_movies.all_movies(), [movie3, movie1, movie2])

    def test_revoke_perm(self):
        """
        Verify that the two revoke_viewing methods remove Viewing for the given book from the given user
        """
        movie1, movie2, movie3 = Movie.objects.all()
        self.user.seen_movies.bulk_add_movies([movie1, movie3, movie2])
        self.other_user.seen_movies.bulk_add_movies([movie1, movie3, movie2])

        self.assertEqual(6, Viewing.objects.count())

        self.user.seen_movies.revoke_viewing(movie2)
        self.assertEqual(5, Viewing.objects.count())
        self.assertFalse(self.user.seen_movies.has_seen_movie(movie2))
        self.assertTrue(self.other_user.seen_movies.has_seen_movie(movie2))

        Viewing.objects.revoke_viewing_from_user(self.user, movie1)
        self.assertEqual(4, Viewing.objects.count())
        self.assertFalse(self.user.seen_movies.has_seen_movie(movie1))
        self.assertTrue(self.other_user.seen_movies.has_seen_movie(movie1))
