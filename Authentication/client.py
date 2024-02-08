from rest_framework.test import APIClient


class Client:
    @staticmethod
    def get_client(
        authenticated_client: APIClient = APIClient(), authenticate_client: bool = False
    ):
        """

        :param authenticated_client:
        :param authenticate_client:
        :return: Authenticated APIClient if asked for, otherwise just APIClient
        """
        return authenticated_client if authenticate_client else APIClient()
