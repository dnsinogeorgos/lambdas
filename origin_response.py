'''
This function injects security headers to origin responses.
In case of 404, it conditionally redirects to request URI
appended with /.
'''
import re


def lambda_handler(event, _):
    request = event["Records"][0]["cf"]["request"]
    response = event["Records"][0]["cf"]["response"]
    headers = response["headers"]

    # Inject security headers
    headers["strict-transport-security"] = [{
        "value": "max-age=63072000; includeSubdomains; preload"
    }]
    headers["content-security-policy"] = [{
        "value": "default-src 'self' https://*.everypay.gr:443; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://*.everypay.gr:443 http://www.google-analytics.com https://www.google-analytics.com https://ssl.google-analytics.com http://html5shim.googlecode.com https://html5shim.googlecode.com https://ajax.googleapis.com https://netdna.bootstrapcdn.com https://code.jquery.com https://*.doubleclick.net https://www.googletagmanager.com https://connect.facebook.net; img-src 'self' data: https://*.everypay.gr:443 http://www.google-analytics.com https://www.google-analytics.com https://ssl.google-analytics.com https://*.doubleclick.net; style-src 'self' 'unsafe-inline' 'unsafe-eval' https://*.everypay.gr:443 https://fonts.googleapis.com; font-src 'self' https://*.everypay.gr:443 https://themes.googleusercontent.com https://fonts.gstatic.com; frame-src 'self' https://*; object-src 'self' https://*.everypay.gr:443"
    }]
    headers["x-content-type-options"] = [{
        "value": "nosniff"
    }]
    headers["x-frame-options"] = [{
        "value": "DENY"
    }]
    headers["x-xss-protection"] = [{
        "value": "1; mode=block"
    }]
    headers["referrer-policy"] = [{
        "value": "strict-origin-when-cross-origin"
    }]

    # Conditionally modify 404 response
    if int(response["status"]) == 404:
        print("Captured a 404 with requestId: ",
              event["Records"][0]["cf"]["config"]["requestId"])
        capture = re.compile("/[A-Za-z0-9-_~]*$")
        old_uri = request["uri"]

        # if URI has no trailing slash and is not a filename
        # with extension, then redirect to request URI appended with /
        if not old_uri.endswith("/") and capture.search(old_uri):
            new_uri = capture.sub(r"\g<0>/", old_uri)
            print("Redirected a 404 to " + new_uri + " with requestId: ",
                  event["Records"][0]["cf"]["config"]["requestId"])
            response["status"] = 302
            response.pop("body", None)
            headers["location"] = [{
                "key": "Location",
                "value": new_uri
            }]

    # Return modified response
    return response
