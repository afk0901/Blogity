import google_crc32c
from decouple import config
from google.cloud import secretmanager

# See here:
# https://cloud.google.com/secret-manager/docs/
# access-secret-version#secretmanager-access-secret-version-python


class GoogleCloudsSecretManager:
    def __init__(self):
        self.client = secretmanager.SecretManagerServiceClient()

    def access_secret(self, secret_id: str, version_id="latest") -> str:
        environment = config("ENV")
        google_cloud_project_name = config("GC_PROJECT_NAME")
        name = (
            f"projects/{google_cloud_project_name}/secrets/{secret_id}-"
            f"{environment}/versions/{version_id}"
        )
        response = self.client.access_secret_version(request={"name": name})

        crc32c = google_crc32c.Checksum()
        crc32c.update(response.payload.data)
        if response.payload.data_crc32c != int(crc32c.hexdigest(), 16):
            # TODO: Log the incident
            return "Data corruption detected."

        return response.payload.data.decode("utf-8")
