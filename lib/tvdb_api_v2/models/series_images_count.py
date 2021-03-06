# coding: utf-8

"""
    TheTVDB API v2

    API v2 targets v1 functionality with a few minor additions. The API is accessible via https://api.thetvdb.com and provides the following REST endpoints in JSON format.   How to use this API documentation ----------------   You may browse the API routes without authentication, but if you wish to send requests to the API and see response data, then you must authenticate. 1. Obtain a JWT token by `POST`ing  to the `/login` route in the `Authentication` section with your API key and credentials. 1. Paste the JWT token from the response into the \"JWT Token\" field at the top of the page and click the 'Add Token' button.   You will now be able to use the remaining routes to send requests to the API and get a response.   Language Selection ----------------   Language selection is done via the `Accept-Language` header. At the moment, you may only pass one language abbreviation in the header at a time. Valid language abbreviations can be found at the `/languages` route..   Authentication ----------------   Authentication to use the API is similar to the How-to section above. Users must `POST` to the `/login` route with their API key and credentials in the following format in order to obtain a JWT token.  `{\"apikey\":\"APIKEY\",\"username\":\"USERNAME\",\"userkey\":\"USERKEY\"}`  Note that the username and key are ONLY required for the `/user` routes. The user's key is labled `Account Identifier` in the account section of the main site. The token is then used in all subsequent requests by providing it in the `Authorization` header. The header will look like: `Authorization: Bearer <yourJWTtoken>`. Currently, the token expires after 24 hours. You can `GET` the `/refresh_token` route to extend that expiration date.   Versioning ----------------   You may request a different version of the API by including an `Accept` header in your request with the following format: `Accept:application/vnd.thetvdb.v$VERSION`. This documentation automatically uses the version seen at the top and bottom of the page.

    OpenAPI spec version: 2.1.2
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class SeriesImagesCount(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """


    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'fanart': 'int',
        'poster': 'int',
        'season': 'int',
        'seasonwide': 'int',
        'series': 'int'
    }

    attribute_map = {
        'fanart': 'fanart',
        'poster': 'poster',
        'season': 'season',
        'seasonwide': 'seasonwide',
        'series': 'series'
    }

    def __init__(self, fanart=None, poster=None, season=None, seasonwide=None, series=None):
        """
        SeriesImagesCount - a model defined in Swagger
        """

        self._fanart = None
        self._poster = None
        self._season = None
        self._seasonwide = None
        self._series = None

        if fanart is not None:
          self.fanart = fanart
        if poster is not None:
          self.poster = poster
        if season is not None:
          self.season = season
        if seasonwide is not None:
          self.seasonwide = seasonwide
        if series is not None:
          self.series = series

    @property
    def fanart(self):
        """
        Gets the fanart of this SeriesImagesCount.

        :return: The fanart of this SeriesImagesCount.
        :rtype: int
        """
        return self._fanart

    @fanart.setter
    def fanart(self, fanart):
        """
        Sets the fanart of this SeriesImagesCount.

        :param fanart: The fanart of this SeriesImagesCount.
        :type: int
        """

        self._fanart = fanart

    @property
    def poster(self):
        """
        Gets the poster of this SeriesImagesCount.

        :return: The poster of this SeriesImagesCount.
        :rtype: int
        """
        return self._poster

    @poster.setter
    def poster(self, poster):
        """
        Sets the poster of this SeriesImagesCount.

        :param poster: The poster of this SeriesImagesCount.
        :type: int
        """

        self._poster = poster

    @property
    def season(self):
        """
        Gets the season of this SeriesImagesCount.

        :return: The season of this SeriesImagesCount.
        :rtype: int
        """
        return self._season

    @season.setter
    def season(self, season):
        """
        Sets the season of this SeriesImagesCount.

        :param season: The season of this SeriesImagesCount.
        :type: int
        """

        self._season = season

    @property
    def seasonwide(self):
        """
        Gets the seasonwide of this SeriesImagesCount.

        :return: The seasonwide of this SeriesImagesCount.
        :rtype: int
        """
        return self._seasonwide

    @seasonwide.setter
    def seasonwide(self, seasonwide):
        """
        Sets the seasonwide of this SeriesImagesCount.

        :param seasonwide: The seasonwide of this SeriesImagesCount.
        :type: int
        """

        self._seasonwide = seasonwide

    @property
    def series(self):
        """
        Gets the series of this SeriesImagesCount.

        :return: The series of this SeriesImagesCount.
        :rtype: int
        """
        return self._series

    @series.setter
    def series(self, series):
        """
        Sets the series of this SeriesImagesCount.

        :param series: The series of this SeriesImagesCount.
        :type: int
        """

        self._series = series

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        if not isinstance(other, SeriesImagesCount):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
