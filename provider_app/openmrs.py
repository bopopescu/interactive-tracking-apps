from kivy.network.urlrequest import UrlRequest

import base64
import json
try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote


class RESTConnection(object):
    @staticmethod
    def _construct_url(authority, port, resource, get_parameters=''):
        return 'http://{authority}:{port}/openmrs/ws/rest/v1/{resource}?{get_parameter}' \
            .format(authority=authority, port=port, resource=resource, get_parameter = get_parameters)

    def __init__(self, authority, port, username, password):
        self.authority = authority
        self.port = port
        credentials = '{username}:{password}'.format(username=username, password=password)
        credentials = base64.standard_b64encode(credentials.encode('UTF8')).decode('UTF8')
        self.headers = {
            'Authorization': 'Basic {credentials}'.format(credentials=credentials),
            'Content-type': 'application/json',
        }

    def send_request(self, resource, post_parameters, on_success, on_failure, on_error, get_parameters):
        url = RESTConnection._construct_url(self.authority, self.port, resource, get_parameters)
        post_parameters = json.dumps(post_parameters) if post_parameters is not None else None
        UrlRequest(url, req_headers=self.headers, req_body=post_parameters,
                   on_success=on_success, on_failure=on_failure, on_error=on_error)
