# lambdas

python functions for aws lambda  

### edge functions:
a set of functions, intended for cloudfront distributions  

##### origin_requests
```
This function appends index.html to all request URIs with a trailing
slash. Intended to work around the S3 Origins for Cloudfront, that use
Origin Access Identity.
```

##### origin_response
```python
This function injects security headers to origin responses.
In case of 404, it conditionally redirects to request URI
appended with /.
```

##### viewer_request
```python
This function implements Basic HTTP authentication.
https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/401
https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/WWW-Authenticate
```

![Python repo workflow](https://github.com/dnsinogeorgos/lambdas/workflows/Python%20repo%20workflow/badge.svg?branch=main)
