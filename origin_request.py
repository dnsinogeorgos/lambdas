"""
This function appends index.html to all request URIs with a trailing
slash. Intended to work around the S3 Origins for Cloudfront, that use
Origin Access Identity.
"""


def lambda_handler(event, _):
    request = event["Records"][0]["cf"]["request"]
    old_uri = request["uri"]

    # If URI has a trailing slash, append index.html
    if old_uri.endswith("/"):
        new_uri = old_uri + "index.html"
        print("Modified URI from: " + old_uri + " to: " + new_uri)

        request["uri"] = new_uri

    return request
