"""
This function implements Basic HTTP authentication.
https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/401
https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/WWW-Authenticate
"""
import base64


def lambda_handler(event, _):
    request = event["Records"][0]["cf"]["request"]

    # Prepare a Basic HTTP auth response
    response = {
        "status": 401,
        "statusDescription": "Unauthorized",
        "body": "Unauthorized",
        "headers": {"www-authenticate": [{"value": "Basic"}]},
    }

    # Check for authorization header
    if "authorization" in request["headers"]:
        value = request["headers"].get("authorization")[0]["value"]

        auth_user = b"this"
        auth_pass = b"password"
        auth_string = "Basic " + base64.b64encode(auth_user + b":" + auth_pass).decode(
            "utf8"
        )

        # If the authorization header is valid, forward the
        # request to origin
        if value == auth_string:
            return request

    # Otherwise, return the Basic HTTP auth response
    return response
