"""General purpose authentication functions for API requests"""

def get_auth_header(auth_string):
    """Return formatted headers for API authentication"""

    return {
        'Content-Type': 'application/json',
        'Authorization': auth_string
    }

def get_credentials(secret_name):
    """Return the specified API credentials from AWS Secret Manager"""

def authenticate(api_url):
    """Authenticate with the specified API"""
    pass
