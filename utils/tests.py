import unittest
from unittest.mock import MagicMock, patch

from utils.secrets_utils import GoogleCloudsSecretManager


class SecretAccess(unittest.TestCase):

    # Expecting that the app is authenticated to Google clouds

    def setUp(self):
        self.env = "DEV"

    @patch("utils.secrets_utils.secretmanager.SecretManagerServiceClient")
    @patch("utils.secrets_utils.config")
    def test_successful_retrieval(self, mock_config, mock_client_class):

        mock_config.return_value = "DEV"

        mock_client = mock_client_class.return_value
        mock_client.access_secret_version.return_value = MagicMock(
            payload=MagicMock(data=b"MySecret")
        )

        result = GoogleCloudsSecretManager().access_secret(mock_client, "my_secret")
        self.assertEqual(result, "MySecret")


if __name__ == "__main__":
    unittest.main()
