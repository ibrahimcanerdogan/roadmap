import requests
from flask import current_app
import json

class GitHubAPI:
    def __init__(self):
        self.base_url = current_app.config['GITHUB_API_BASE_URL']
        self.timeout = current_app.config['GITHUB_API_TIMEOUT']
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'GitHub-User-Activity-App'
        }
    
    def get_user_events(self, username):
        """
        Fetch recent events for a GitHub user
        
        Args:
            username (str): GitHub username
            
        Returns:
            list: List of user events
            
        Raises:
            requests.RequestException: If API request fails
            ValueError: If username is invalid
        """
        if not username or not username.strip():
            raise ValueError("Username cannot be empty")
        
        url = f"{self.base_url}/users/{username}/events"
        
        try:
            response = requests.get(
                url, 
                headers=self.headers, 
                timeout=self.timeout
            )
            
            # Handle different HTTP status codes
            if response.status_code == 404:
                raise ValueError(f"User '{username}' not found on GitHub")
            elif response.status_code == 403:
                raise ValueError("GitHub API rate limit exceeded. Please try again later.")
            elif response.status_code != 200:
                raise ValueError(f"GitHub API error: {response.status_code}")
            
            events = response.json()
            
            # Limit the number of events to display
            max_events = current_app.config['MAX_EVENTS_DISPLAY']
            return events[:max_events]
            
        except requests.Timeout:
            raise ValueError("Request timeout. Please try again.")
        except requests.ConnectionError:
            raise ValueError("Connection error. Please check your internet connection.")
        except json.JSONDecodeError:
            raise ValueError("Invalid response from GitHub API.")
        except requests.RequestException as e:
            raise ValueError(f"API request failed: {str(e)}")
    
    def get_user_info(self, username):
        """
        Fetch basic user information
        
        Args:
            username (str): GitHub username
            
        Returns:
            dict: User information
        """
        if not username or not username.strip():
            raise ValueError("Username cannot be empty")
        
        url = f"{self.base_url}/users/{username}"
        
        try:
            response = requests.get(
                url, 
                headers=self.headers, 
                timeout=self.timeout
            )
            
            if response.status_code == 404:
                raise ValueError(f"User '{username}' not found on GitHub")
            elif response.status_code != 200:
                raise ValueError(f"GitHub API error: {response.status_code}")
            
            return response.json()
            
        except requests.RequestException as e:
            raise ValueError(f"API request failed: {str(e)}") 