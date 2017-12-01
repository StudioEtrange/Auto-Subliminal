import abc
import logging
from time import time

from imdb import IMDb
from tvdb_api_v2.client import TvdbClient

import autosubliminal
from autosubliminal import utils
from autosubliminal.db import ImdbIdCache, TvdbIdCache

log = logging.getLogger(__name__)


class Indexer(object):
    """
    Base class for all indexers.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def _query_api(self, title, year=None):
        pass


class ShowIndexer(Indexer):
    """
    Indexer for tv shows, which uses the TVDB api.
    """

    def __init__(self):
        self._client = TvdbClient(api_key=autosubliminal.TVDBAPIKEY)
        # Currently, the token expires after 24 hours, see https://api.thetvdb.com/swagger
        # Let's refresh it every 12h at our side
        self._token_expiration_interval = 24 * 60 * 60
        self._token_refresh_interval = 12 * 60 * 60
        self._token_generation_time = None
        self._token = None

    @property
    def _token_needs_refresh(self):
        """Check if authentication token needs refresh."""
        return time() > self._token_generation_time + self._token_refresh_interval

    @property
    def _token_expired(self):
        """Check if authentication has expired."""
        return time() >= self._token_generation_time + self._token_expiration_interval

    def _authenticate(self):
        """Authenticate or refresh token."""
        if not self._token or self._token_expired:
            self._token = self._client.authenticate()
            self._token_generation_time = time()
        elif self._token_needs_refresh:
            self._token = self._client.refresh_token()
            self._token_generation_time = time()

    def _query_api(self, title, year=None):
        name = title
        if year:
            name += " (" + str(year) + ")"
        log.info("Querying tvdb api for %s" % name)
        # Return a tvdb_api_v2.models.series_search.SeriesSearch object
        self._authenticate()
        series_search = self._client.search_series_by_name(name)
        for series_search_data in series_search.data:
            if series_search_data.series_name.lower() == name.lower():
                return series_search_data
            elif series_search_data.aliases:
                # If no match, fallback to aliases (if aliases are available)
                for alias in series_search_data.aliases:
                    if alias.lower() == name.lower():
                        return series_search_data
            else:
                continue

    def get_tvdb_id(self, title, year=None, force_search=False, store_id=True):
        tvdb_id = None
        name = title
        if year:
            name += " (" + str(year) + ")"
        log.debug("Getting tvdb id for %s" % name)
        # If not force_search, first check shownamemapping and tvdb id cache
        if not force_search:
            # Check shownamemapping
            tvdb_id = utils.show_name_mapping(name)
            if tvdb_id:
                log.debug("Tvdb id from shownamemapping %s" % tvdb_id)
                return int(tvdb_id)
            # Check tvdb id cache
            tvdb_id = TvdbIdCache().get_id(name)
            if tvdb_id:
                log.debug("Getting tvdb id from cache %s" % tvdb_id)
                if tvdb_id == -1:
                    log.error("Tvdb id not found in cache for %s" % name)
                    return
                return int(tvdb_id)
        # Search on tvdb
        try:
            show = self._query_api(title, year)
            if show:
                tvdb_id = show.id
        except Exception, e:
            log.error("Tvdb id not found for %s" % name)
            log.error(e)
            if store_id:
                TvdbIdCache().set_id(-1, name)
        if tvdb_id:
            log.debug("Tvdb id from api %s" % tvdb_id)
            if store_id:
                TvdbIdCache().set_id(tvdb_id, name)
                log.info("%s added to cache with %s" % (name, tvdb_id))
            return int(tvdb_id)


class MovieIndexer(Indexer):
    """
    Indexer for movies, which uses the IMDB api.
    """

    def _query_api(self, title, year=None):
        name = title
        if year:
            name += " (" + str(year) + ")"
        log.info("Querying imdb api for %s" % name)
        # Return a imdb.Movie object
        imdb_movies = IMDb().search_movie(title)
        # Find the first movie that matches the title (and year if present)
        for movie in imdb_movies:
            data = movie.data
            if data['kind'] == 'movie' and data['title'].lower() == title.lower():
                # If a year is present, it should also be the same
                if year:
                    if data['year'] == year:
                        return movie
                    else:
                        continue
                # If no year is present, take the first match
                else:
                    return movie

    def get_imdb_id_and_year(self, title, year=None, force_search=False, store_id=True):
        imdb_id = None
        name = title
        if year:
            name += " (" + str(year) + ")"
        log.debug("Getting imdb info for %s" % name)
        # If not force_search, first check movienamemapping and tvdb id cache
        if not force_search:
            imdb_id = utils.movie_name_mapping(title, year)
            if imdb_id:
                log.debug("Imdb id from movienamemapping %s" % imdb_id)
                return imdb_id, year
            imdb_id = ImdbIdCache().get_id(title, year)
            if imdb_id:
                log.debug("Getting imdb id from cache %s" % imdb_id)
                return imdb_id, year
        # Search on imdb
        try:
            movie = self._query_api(title, year)
            if movie:
                imdb_id = movie.movieID
                year = movie.data['year'] if not year else year
                log.debug("Getting imdb id from api %s" % imdb_id)
                if store_id:
                    ImdbIdCache().set_id(imdb_id, title, year)
                    log.info("%s added to cache with %s" % (name, imdb_id))
        except Exception, e:
            log.error("Imdb id not found for %s" % name)
            log.error(e)
        if not imdb_id:
            log.error("Imdb id not found for %s (%s)" % (title, year))
        return imdb_id, year
