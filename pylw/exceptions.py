class LeekWarsApiException(Exception):
    def __init__(self, response):
        request = response.request
        message = u'{method} {url} {status}'.format(method=request.method, url=request.url, status=response.status_code)
        if response.ok:
            message += ' ' + response.text
        super(LeekWarsApiException, self).__init__(message)
        self.response = response

