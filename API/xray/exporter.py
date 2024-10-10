"""Module for exporting, and processing tests from Xray"""
import zipfile
import requests


class Exporter:
    """Class to handle exporting, and processing tests from Xray to a directory"""
    def __init__(self, auth_headers, issue_keys, extraction_location):
        self.export_url = 'https://xray.cloud.getxray.app/api/v2/export/cucumber'
        self.auth_headers = auth_headers
        self.issue_keys = issue_keys
        self.extraction_location = extraction_location

    def __extract_tests(self, zip_contents, extraction_location):
        """Extract the tests from the zip file and write them to a directory"""
        with open('test.zip', 'wb') as f:
            f.write(zip_contents)

        with zipfile.ZipFile('test.zip', 'r') as zip_obj:
            zip_obj.extractall(extraction_location)

    def get_export_tests_response(self):
        """Export the tests from Xray and return the response object"""
        response = requests.get(
            self.export_url,
            params = {"keys": self.issue_keys},
            headers = self.auth_headers,
            timeout=15
        )

        if response.status_code != 200:
            print("Error: Files not exported")
            return None

        print("Successfully exported tests")
        return response

    def export_tests_to_directory(self):
        """Export the tests from Xray and write them to a directory"""
        response = self.get_export_tests_response()
        if response is None:
            return

        self.__extract_tests(response.content, self.extraction_location)
