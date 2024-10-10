"""
This module is responsible for authenticating with the Xray API
and constructing the appropriate headers for the API requests.
"""
import requests

from API.utils.get_secret import get_secret


class Authenticator:
    """Class to authenticate the user with the Xray API"""

    def __init__(self, xray_secret_name: str):
        self.auth_url = 'https://xray.cloud.getxray.app/api/v2/authenticate'
        self.pre_auth_headers = {'Content-Type': 'application/json'}
        self.__xray_credentials = self.__get_xray_credentials(xray_secret_name)

        self.auth_token = self.get_auth_token()
        self.auth_headers = self.get_auth_headers()

    def get_auth_token(self):
        """Return the authentication token"""
        decoded_auth_response_content = self.__authenticate()
        decoded_auth_token = f"Bearer {decoded_auth_response_content}"
        return decoded_auth_token.replace('"', '')

    def get_auth_headers(self):
        """Return the authentication headers"""
        return {
            'Content-Type': 'application/json',
            'Authorization': self.auth_token
        }

    def __get_xray_credentials(self, xray_secret_name: str):
        """Return the xray API credentials from AWS Secret Manager"""
        return get_secret(xray_secret_name)

    def __authenticate(self):
        response = requests.post(
            self.auth_url,
            data = self.__xray_credentials,
            headers = self.pre_auth_headers,
            timeout=15
        )

        if response.status_code != 200:
            print("Error: Not Authenticated :(")
            return None

        print("Successfully Authenticated")
        return response.content.decode('UTF-8')
