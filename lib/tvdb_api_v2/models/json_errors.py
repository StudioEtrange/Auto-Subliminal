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


class JSONErrors(object):
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
        'invalid_filters': 'list[str]',
        'invalid_language': 'str',
        'invalid_query_params': 'list[str]'
    }

    attribute_map = {
        'invalid_filters': 'invalidFilters',
        'invalid_language': 'invalidLanguage',
        'invalid_query_params': 'invalidQueryParams'
    }

    def __init__(self, invalid_filters=None, invalid_language=None, invalid_query_params=None):
        """
        JSONErrors - a model defined in Swagger
        """

        self._invalid_filters = None
        self._invalid_language = None
        self._invalid_query_params = None

        if invalid_filters is not None:
          self.invalid_filters = invalid_filters
        if invalid_language is not None:
          self.invalid_language = invalid_language
        if invalid_query_params is not None:
          self.invalid_query_params = invalid_query_params

    @property
    def invalid_filters(self):
        """
        Gets the invalid_filters of this JSONErrors.
        Invalid filters passed to route

        :return: The invalid_filters of this JSONErrors.
        :rtype: list[str]
        """
        return self._invalid_filters

    @invalid_filters.setter
    def invalid_filters(self, invalid_filters):
        """
        Sets the invalid_filters of this JSONErrors.
        Invalid filters passed to route

        :param invalid_filters: The invalid_filters of this JSONErrors.
        :type: list[str]
        """

        self._invalid_filters = invalid_filters

    @property
    def invalid_language(self):
        """
        Gets the invalid_language of this JSONErrors.
        Invalid language or translation missing

        :return: The invalid_language of this JSONErrors.
        :rtype: str
        """
        return self._invalid_language

    @invalid_language.setter
    def invalid_language(self, invalid_language):
        """
        Sets the invalid_language of this JSONErrors.
        Invalid language or translation missing

        :param invalid_language: The invalid_language of this JSONErrors.
        :type: str
        """

        self._invalid_language = invalid_language

    @property
    def invalid_query_params(self):
        """
        Gets the invalid_query_params of this JSONErrors.
        Invalid query params passed to route

        :return: The invalid_query_params of this JSONErrors.
        :rtype: list[str]
        """
        return self._invalid_query_params

    @invalid_query_params.setter
    def invalid_query_params(self, invalid_query_params):
        """
        Sets the invalid_query_params of this JSONErrors.
        Invalid query params passed to route

        :param invalid_query_params: The invalid_query_params of this JSONErrors.
        :type: list[str]
        """

        self._invalid_query_params = invalid_query_params

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
        if not isinstance(other, JSONErrors):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
