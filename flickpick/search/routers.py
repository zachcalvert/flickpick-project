from haystack import DEFAULT_ALIAS
from haystack.routers import BaseRouter


class FlickpickSearchRouter(BaseRouter):

    def for_read(self, **hints):
        return DEFAULT_ALIAS

    def for_write(self, **hints):
        return DEFAULT_ALIAS
