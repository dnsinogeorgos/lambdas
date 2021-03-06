"""
This function injects security headers to origin responses.
In case of 404, it conditionally redirects to request URI
appended with /.
"""
import re


def lambda_handler(event, _):  # pylint: disable=C0116
    request = event["Records"][0]["cf"]["request"]
    response = event["Records"][0]["cf"]["response"]
    headers = response["headers"]

    # Inject security headers
    headers["strict-transport-security"] = [
        {"value": "max-age=63072000; includeSubdomains; preload"}
    ]
    headers["content-security-policy"] = [{"value": "default-src 'self' https://*"}]
    headers["x-content-type-options"] = [{"value": "nosniff"}]
    headers["x-frame-options"] = [{"value": "DENY"}]
    headers["x-xss-protection"] = [{"value": "1; mode=block"}]
    headers["referrer-policy"] = [{"value": "strict-origin-when-cross-origin"}]

    # Conditionally modify 404 response
    if int(response["status"]) == 404:
        print(
            "Captured a 404 with requestId: ",
            event["Records"][0]["cf"]["config"]["requestId"],
        )
        capture = re.compile("/[A-Za-z0-9-_~]*$")
        old_uri = request["uri"]

        # if URI has no trailing slash and is not a filename
        # with extension, then redirect to request URI appended with /
        if not old_uri.endswith("/") and capture.search(old_uri):
            new_uri = capture.sub(r"\g<0>/", old_uri)
            print(
                "Redirected a 404 to " + new_uri + " with requestId: ",
                event["Records"][0]["cf"]["config"]["requestId"],
            )
            response["status"] = 302
            response.pop("body", None)
            headers["location"] = [{"key": "Location", "value": new_uri}]

    # Return modified response
    return response
