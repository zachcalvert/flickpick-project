from django.contrib.auth.models import User
from django.db import models, transaction, IntegrityError
from django.db.models import Q

from movies.models import Movie


class ViewingManager(models.Manager):
    """
    Custom manager which provides handy utility methods for determining who has seen what.

    When this manager is referenced through a User instance, the methods has_seen_movie() and add_movie()
    will automagically figure out the user in question.
    """

    def get_queryset(self):
        qs = super(ViewingManager, self).get_queryset()
        return qs

    def get_user(self):
        """
        return the user common to all viewings on this manager (namely if this is the related manager)
        Raises an exception if there is a number of users other than one
        """
        if isinstance(self, type(User().seen_movies)):
            return self.instance
        else:
            raise ValueError("This method is only available on a RelatedManager from User")

    def user_query(self, user):
        """
        returns a Q object which matches either the given user or the anonymous user (None)
        """
        if user and not user.is_anonymous():
        	return user

    def user_has_seen_movie(self, user, movie):
        """
        returns whether the current user has seen the given movie
        """
        return Viewing.objects.filter(user=user, movie=movie).exists()

    def has_seen_movie(self, movie):
        """
        returns whether the given user has seen the given movie
        """
        return self.user_has_seen_movie(self.get_user(), movie)

    @transaction.atomic
    def add_movie_to_user(self, user, movie):
        """
        Creates a Viewing between a movie and a user
        :param user: user who will have seen the movie
        :param movie: movie to add the viewing record for
        :return: new Viewing object
        """
        if user and user.is_anonymous():
            user = None
        viewing, created = self.get_or_create(user=user, movie=movie)
        return viewing

    def add_movie(self, movie):
        """
        Creates a Viewing between a movie and the current user
        :param movie: movie to add the viewing record for
        :return: new Viewing object
        """
        return self.add_movie_to_user(self.get_user(), movie)

    def bulk_add_movies_to_user(self, user, movies, max_retries=0):
        """
        Creates multiple Viewings using bulk_create
        :param user: user who will have seen the movies
        :param movies: movies to grant viewings to
        :param max_retries: The number of times to retry (useful in situations where race conditions might crop up)
        :return: queryset of new Viewing objects
        """
        # remove duplicates
        deduped_movies = []
        for movie in movies:
            if movie not in deduped_movies:
                deduped_movies.append(movie)
        movies = deduped_movies

        if user and user.is_anonymous():
            user = None

        viewings = []
        success = False
        fail_count = 0
        while not success:
            try:
                with transaction.atomic():
                    known_movies = {v.movie for v in
                                      Viewing.objects.filter(user=user,
                                                               movie__in=movies).select_related("movie")}
                    new_movies = [m for m in movies if m not in known_movies]

                    if new_movies:
                        Viewing.objects.bulk_create([
                            Viewing(user=user, movie=movie)
                            for movie in new_movies
                        ])
                    success = True
            except IntegrityError:
                if fail_count >= max_retries:
                    raise
                else:
                    fail_count += 1
        return viewings

    def bulk_add_movies(self, movies, max_retries=0):
        """
        Creates multiple Viewings using bulk_create
        :param movies: movies to grant viewing to
        :param max_retries: The number of times to retry (useful in situations where race conditions might crop up)
        :return: queryset of new Viewing objects
        """
        return self.bulk_add_movies_to_user(self.get_user(), movies, max_retries=max_retries)

    
    def revoke_viewing_from_user(self, user, movie):
        """
        Remove viewing from a user for a movie
        :param user: user for whom to revoke viewing
        :param movie: movie that user will no longer have seen
        """
        if user and user.is_anonymous():
            user = None
        try:
            Viewing.objects.get(user=user, movie=movie).delete()
        except Viewing.DoesNotExist:
            pass

    def revoke_viewing(self, movie):
        """
        Remove viewing from the current user for a movie
        :param movie: movie that user will no longer own
        """
        self.revoke_viewing_from_user(self.get_user(), movie)

    def all_movies_for_user_by_rating(self, user):
        """
        Returns a list of every Movie the given user has seen.
        """
        viewings = Viewing.objects.filter(user=user).order_by('-rating')
        movies = [v.movie for v in viewings]
        return movies

    def all_movies_for_user(self, user):
		"""
		Returns a list of every Movie the given user has seen.
		"""
		viewings = Viewing.objects.filter(user=user).order_by('-timestamp')
		movies = [v.movie for v in viewings]
		return movies

    def all_movies(self):
        """
        Returns a (cached) list of every Movie the current user has seen.
        """
        return self.all_movies_for_user(self.get_user())


class Viewing(models.Model):
    """
    A model mapping a User to a Movie, which proves that the user has seen that Movie.
    """
    user = models.ForeignKey(User, related_name='seen_movies', null=True)  # null user stands in for anonymous permissions
    movie = models.ForeignKey(Movie, related_name='viewers')
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    objects = ViewingManager()

    def __unicode__(self):
        return "user: {}, movie: {}".format(self.user, self.movie)

    class Meta:
        verbose_name = "Viewing"
        verbose_name_plural = "Viewing"
        unique_together = ['user', 'movie']
        db_table = "viewing"


