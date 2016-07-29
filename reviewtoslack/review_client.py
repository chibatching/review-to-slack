import os

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client.service_account import ServiceAccountCredentials

from review import Review


_SCOPES = ['https://www.googleapis.com/auth/androidpublisher']

_CREDENTIAL_DICT = {
    "type": os.environ.get("GCP_TYPE"),
    "project_id": os.environ.get("GCP_PROJECT_ID"),
    "private_key_id": os.environ.get("GCP_PRIVATE_KEY_ID"),
    "private_key": os.environ.get("GCP_PRIVATE_KEY"),
    "client_email": os.environ.get("GCP_CLIENT_EMAIL"),
    "client_id": os.environ.get("GCP_CLIENT_ID"),
    "auth_uri": os.environ.get("GCP_AUTH_URI"),
    "token_uri": os.environ.get("GCP_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.environ.get("GCP_AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.environ.get("GCP_CLIENT_X509_CERT_URL")
}


def load_review_list(package_name, last_post=0):
    credential = ServiceAccountCredentials.from_json_keyfile_dict(_CREDENTIAL_DICT, scopes=_SCOPES)
    http_auth = credential.authorize(Http())
    service = build('androidpublisher', 'v2', http=http_auth)

    token = None
    result = list()
    latest_modified = last_post
    while True:
        reviews = service.reviews().list(packageName=package_name, token=token).execute()

        for r in reviews["reviews"]:
            if "text" in r["comments"][0]["userComment"]:

                modified = int(r["comments"][0]["userComment"]["lastModified"]["seconds"])
                if last_post < modified:
                    result.append(Review(r))
                    if latest_modified < modified:
                        latest_modified = modified
                else:
                    return _create_result_dict(latest_modified, result)

        if "tokenPagination" in reviews:
            token = reviews["tokenPagination"]["nextPageToken"]
        else:
            break

    return _create_result_dict(latest_modified, result)


def _create_result_dict(latest_modified, result):
    return {"latestModified": latest_modified, "list": result}


def main():
    result = load_review_list("com.chibatching.worldclockwidget", last_post=1463689045)
    print result["latestModified"]
    for r in result["list"]:
        print vars(r)


if __name__ == '__main__':
    main()
