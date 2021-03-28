# pylint: disable=C0114
import unittest

from origin_request import lambda_handler


event = {"Records": [{"cf": {"request": {"uri": ""}}}]}


class TestLambdaHandler(unittest.TestCase):  # pylint: disable=C0115
    def test_no_slash(self):
        """
        This requests a URI without a trailing slash and no file extension
        Should return identical result
        """
        request = event["Records"][0]["cf"]["request"]
        request["uri"] = "/examplefolder/examplefile"
        result = lambda_handler(event, None)
        self.assertEqual(result, request)

    def test_file_extension(self):
        """
        This requests a URI with a file extension
        Should return identical result
        """
        request = event["Records"][0]["cf"]["request"]
        request["uri"] = "/examplefolder/examplefile.ext"
        result = lambda_handler(event, None)
        self.assertEqual(result, request)

    def test_with_slash(self):
        """
        This requests a URI with a trailing slash
        Should return result with appended "index.html" to the URI
        """
        request = event["Records"][0]["cf"]["request"]
        request["uri"] = "/examplefolder/examplefolder2/"
        result = lambda_handler(event, None)
        self.assertEqual(result["uri"], "/examplefolder/examplefolder2/index.html")


if __name__ == "__main__":
    unittest.main()
