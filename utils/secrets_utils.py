import google_crc32c
from decouple import config
from google.cloud import secretmanager

# See here:
# https://cloud.google.com/secret-manager/docs/
# access-secret-version#secretmanager-access-secret-version-python

# Create the Secret Manager client.
client = secretmanager.SecretManagerServiceClient()


def access_secret(project_id: str, secret_id: str, version_id: str = "latest") -> str:
    """Access the payload for the given secret version if one exists.

    The version can be a version number as a string (e.g. "5") or an
    alias (e.g. "latest").
    """

    # TODO: Make unit tests for me, mock out the API and simulate.

    # dev, staging or prod
    environment = config("ENVIRONMENT")

    # Build the resource name of the secret version.
    name = (
        f"projects/{project_id}/secrets/{secret_id}-{environment}/versions/{version_id}"
    )

    # Access the secret version.
    response = client.access_secret_version(request={"name": name})

    # Verify payload checksum.
    crc32c = google_crc32c.Checksum()
    crc32c.update(response.payload.data)
    if response.payload.data_crc32c != int(crc32c.hexdigest(), 16):
        print("Data corruption detected.")
        # TODO: Log the response intead of printing it
        print(response)
    payload = response.payload.data.decode("UTF-8")
    return payload
