"""This module contains custom methods for the test client.

Used to interact with the API when creating automatic tests.
"""

from rest_framework.test import APIClient


class Client:
    """This class contains custom methods about the test client itself.

    Such as when to return authenticated client with an API key, JWT key
    or other authentication methods. It may be extended for more
    operations on the test client class.
    """

    @staticmethod
    def get_client(
        authenticated_client: APIClient = APIClient(),
        authenticate: bool = False,
    ) -> APIClient:
        """If authenticate is True, return authenticated client, otherwise
        return a new client.

        This is useful when it's possible to iterate over booleans, for example when
        parameterizing tests.

        :param authenticated_client: An authenticated client with API key, JWT token, or
            other authentication measures.
        :param authenticate: If true return authenticated client otherwise return
            unauthenticated client.
        :return: Authenticated APIClient authenticate is True, otherwise new APIClient
        """
        return authenticated_client if authenticate else APIClient()
