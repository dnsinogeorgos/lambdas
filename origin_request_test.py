import unittest

from origin_request import lambda_handler


event = {
    "Records": [
        {
            "cf": {
                "request": {
                    "uri": ""
                }
            }
        }
    ]
}

class TestLambdaHandler(unittest.TestCase):
    def test_no_slash(self):
        '''
        This requests a URI without a trailing slash and no file extension
        Should return identical result
        '''
        request = event["Records"][0]["cf"]["request"]
        request["uri"] = "/v2/examplefolder"
        result = lambda_handler(event, None)
        self.assertEqual(result, request)

    def test_file_extension(self):
        '''
        This requests a URI with a file extension
        Should return identical result
        '''
        request = event["Records"][0]["cf"]["request"]
        request["uri"] = "/v2/examplefolder.doc"
        result = lambda_handler(event, None)
        self.assertEqual(result, request)

    def test_with_slash(self):
        '''
        This requests a URI with a trailing slash
        Should return result with appended "index.html" to the URI
        '''
        request = event["Records"][0]["cf"]["request"]
        request["uri"] = "/v2/examplefolder/"
        result = lambda_handler(event, None)
        self.assertEqual(result["uri"], "/v2/examplefolder/index.html")

if __name__ == "__main__":
    unittest.main()
