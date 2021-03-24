import unittest

from origin_response import lambda_handler


event = {
    "Records": [
        {
            "cf": {
                "config": {"requestId": "thisfakeidisthisfakeidisthisfakeidis"},
                "request": {"uri": ""},
                "response": {"headers": {}, "status": 0},
            }
        }
    ]
}


class TestLambdaHandler(unittest.TestCase):
    def test_success(self):
        """
        This sends a success response
        Should return identical result with injected security headers
        """
        event["Records"][0]["cf"]["request"]["uri"] = "/v2/examplefolder/"
        response = event["Records"][0]["cf"]["response"]
        result = lambda_handler(event, None)
        headers = response["headers"]
        headers["strict-transport-security"] = [
            {"value": "max-age=63072000; includeSubdomains; preload"}
        ]
        headers["content-security-policy"] = [{"value": "default-src 'self' https://*"}]
        headers["x-content-type-options"] = [{"value": "nosniff"}]
        headers["x-frame-options"] = [{"value": "DENY"}]
        headers["x-xss-protection"] = [{"value": "1; mode=block"}]
        headers["referrer-policy"] = [{"value": "strict-origin-when-cross-origin"}]
        self.assertEqual(result, response)

    def test_not_found_with_slash(self):
        """
        This sends a not found response for a URI with trailing slash
        Should return identical result with injected security headers
        """
        event["Records"][0]["cf"]["request"]["uri"] = "/v2/examplefolder/"
        response = event["Records"][0]["cf"]["response"]
        response["status"] = 404
        result = lambda_handler(event, None)
        headers = response["headers"]
        headers["strict-transport-security"] = [
            {"value": "max-age=63072000; includeSubdomains; preload"}
        ]
        headers["content-security-policy"] = [
            {
                "value": "default-src 'self' https://*.everypay.gr:443; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://*.everypay.gr:443 http://www.google-analytics.com https://www.google-analytics.com https://ssl.google-analytics.com http://html5shim.googlecode.com https://html5shim.googlecode.com https://ajax.googleapis.com https://netdna.bootstrapcdn.com https://code.jquery.com https://*.doubleclick.net https://www.googletagmanager.com https://connect.facebook.net; img-src 'self' data: https://*.everypay.gr:443 http://www.google-analytics.com https://www.google-analytics.com https://ssl.google-analytics.com https://*.doubleclick.net; style-src 'self' 'unsafe-inline' 'unsafe-eval' https://*.everypay.gr:443 https://fonts.googleapis.com; font-src 'self' https://*.everypay.gr:443 https://themes.googleusercontent.com https://fonts.gstatic.com; frame-src 'self' https://*; object-src 'self' https://*.everypay.gr:443"  # noqa: E501
            }
        ]
        headers["x-content-type-options"] = [{"value": "nosniff"}]
        headers["x-frame-options"] = [{"value": "DENY"}]
        headers["x-xss-protection"] = [{"value": "1; mode=block"}]
        headers["referrer-policy"] = [{"value": "strict-origin-when-cross-origin"}]
        self.assertEqual(result, response)

    def test_not_found_without_slash(self):
        """
        This sends a not found response for a URI without trailing slash
        Should return 302 redirect result tp the original URI appended
        with "/" and injected security headers
        """
        event["Records"][0]["cf"]["request"]["uri"] = "/v2/examplefolder"
        response = event["Records"][0]["cf"]["response"]
        response["status"] = 404
        result = lambda_handler(event, None)
        headers = response["headers"]
        headers["strict-transport-security"] = [
            {"value": "max-age=63072000; includeSubdomains; preload"}
        ]
        headers["content-security-policy"] = [
            {
                "value": "default-src 'self' https://*.everypay.gr:443; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://*.everypay.gr:443 http://www.google-analytics.com https://www.google-analytics.com https://ssl.google-analytics.com http://html5shim.googlecode.com https://html5shim.googlecode.com https://ajax.googleapis.com https://netdna.bootstrapcdn.com https://code.jquery.com https://*.doubleclick.net https://www.googletagmanager.com https://connect.facebook.net; img-src 'self' data: https://*.everypay.gr:443 http://www.google-analytics.com https://www.google-analytics.com https://ssl.google-analytics.com https://*.doubleclick.net; style-src 'self' 'unsafe-inline' 'unsafe-eval' https://*.everypay.gr:443 https://fonts.googleapis.com; font-src 'self' https://*.everypay.gr:443 https://themes.googleusercontent.com https://fonts.gstatic.com; frame-src 'self' https://*; object-src 'self' https://*.everypay.gr:443"  # noqa: E501
            }
        ]
        headers["x-content-type-options"] = [{"value": "nosniff"}]
        headers["x-frame-options"] = [{"value": "DENY"}]
        headers["x-xss-protection"] = [{"value": "1; mode=block"}]
        headers["referrer-policy"] = [{"value": "strict-origin-when-cross-origin"}]
        headers["location"] = [{"key": "Location", "value": "/v2/examplefolder/"}]
        response["status"] = 302
        self.assertEqual(result, response)


if __name__ == "__main__":
    unittest.main()
