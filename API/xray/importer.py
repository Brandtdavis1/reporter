"""Module for importing processed test results to Xray"""
import requests


class Importer:
    """"Class for importing processed test results to Xray"""
    def __init__(self, auth_headers):
        self.import_url = 'https://xray.cloud.getxray.app/api/v2/import/execution'
        self.auth_headers = auth_headers

    def import_results(self, results):
        """Import the processed test results to Xray"""
        response = requests.post(
            self.import_url,
            headers = self.auth_headers,
            data = results,
            timeout=35
        )

        return response
