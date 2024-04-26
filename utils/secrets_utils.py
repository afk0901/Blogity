from decouple import config
from google.cloud import secretmanager

# See here:
# https://cloud.google.com/secret-manager/docs/
# access-secret-version#secretmanager-access-secret-version-python


class GoogleCloudsSecretManager:
    def __init__(self):
        self.client = secretmanager.SecretManagerServiceClient()

    def access_secret(self, secret_id, version_id="latest"):

        # TODO: Payloadcheck? as in the docs...

        environment = config("ENV")
        name = (
            f"projects/blogity/secrets/{secret_id}-{environment}/versions/{version_id}"
        )
        response = self.client.access_secret_version(request={"name": name})
        return response.payload.data.decode("utf-8")
