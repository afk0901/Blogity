import unittest
from unittest.mock import MagicMock, patch

import google_crc32c

from GoogleClouds.secrets_utils import GoogleCloudsSecretManager


class SecretAccess(unittest.TestCase):
    # Expecting that the app is authenticated to Google clouds

    mock = MagicMock()
    checksum_mock = MagicMock()
    checksum = google_crc32c.Checksum()
    checksum_mock.return_value = google_crc32c.Checksum()
    mock_client = mock.return_value.access_secret_version.return_value = MagicMock(
        payload=MagicMock(data=b"MySecret")
    )

    @patch(
        "GoogleClouds.secrets_utils.secretmanager.SecretManagerServiceClient", new=mock
    )
    @patch("GoogleClouds.secrets_utils.google_crc32c.Checksum", new=checksum_mock)
    def test_successful_retrieval(self):
        self.checksum.update(b"MySecret")
        self.mock_client.payload.data_crc32c = int(self.checksum.hexdigest(), 16)

        result = GoogleCloudsSecretManager().access_secret(
            self.mock_client, "my_secret"
        )
        self.assertEqual("MySecret", result)

    @patch(
        "GoogleClouds.secrets_utils.secretmanager.SecretManagerServiceClient", new=mock
    )
    def test_invalid_checksum(self):
        self.mock_client.payload.data_crc32c = 0
        result = GoogleCloudsSecretManager().access_secret(
            self.mock_client, "my_secret"
        )
        self.assertEqual("Data corruption detected.", result)


if __name__ == "__main__":
    unittest.main()
