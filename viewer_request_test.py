import unittest

from viewer_request import lambda_handler


event = {
    "Records": [
        {
            "cf": {
                "request": {
                    "headers": {}
                }
            }
        }
    ]
}

response = {
    "status": 401,
    "statusDescription": "Unauthorized",
    "body": "Unauthorized",
    "headers": {
        "www-authenticate": [{
            "value": "Basic"
        }]
    }
}

class TestLambdaHandler(unittest.TestCase):
    def test_no_auth(self):
        '''
        This sends a request event without an authentication header
        Should return a 401 Unauthorized for Basic authentication
        '''
        result = lambda_handler(event, None)
        self.assertEqual(result, response)

    def test_invalid_auth(self):
        '''
        This sends a request event with an invalid authentication header
        Should return a 401 Unauthorized for Basic authentication
        '''
        request = event["Records"][0]["cf"]["request"]
        request["headers"]["authorization"] = [{
            "value": "Basic badauthbadauth="
        }]
        result = lambda_handler(event, None)
        self.assertEqual(result, response)

    def test_valid_auth(self):
        '''
        This sends a request event with a valid authentication header
        Should return a request object to be forwarded to origin
        '''
        request = event["Records"][0]["cf"]["request"]
        request["headers"]["authorization"] = [{
            "value": "Basic aGVsbG86d29ybGQ="
        }]
        result = lambda_handler(event, None)
        self.assertEqual(result, request)

if __name__ == "__main__":
    unittest.main()
