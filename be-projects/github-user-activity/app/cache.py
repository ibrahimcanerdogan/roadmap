import json
import os
import time
from datetime import datetime, timedelta
from flask import current_app

class ActivityCache:
    def __init__(self, cache_dir='cache', ttl_hours=24):
        """
        Initialize the activity cache
        
        Args:
            cache_dir (str): Directory to store cache files
            ttl_hours (int): Time to live for cached data in hours
        """
        self.cache_dir = cache_dir
        self.ttl_hours = ttl_hours
        
        # Create cache directory if it doesn't exist
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
    
    def _get_cache_file_path(self, username):
        """Get the cache file path for a username"""
        return os.path.join(self.cache_dir, f"{username}.json")
    
    def _is_cache_valid(self, cache_data):
        """Check if cached data is still valid"""
        if not cache_data or 'timestamp' not in cache_data:
            return False
        
        cache_time = datetime.fromisoformat(cache_data['timestamp'])
        expiry_time = cache_time + timedelta(hours=self.ttl_hours)
        
        return datetime.now() < expiry_time
    
    def get_user_data(self, username):
        """
        Get cached user data
        
        Args:
            username (str): GitHub username
            
        Returns:
            dict: Cached user data or None if not found/invalid
        """
        try:
            cache_file = self._get_cache_file_path(username)
            
            if not os.path.exists(cache_file):
                return None
            
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            if not self._is_cache_valid(cache_data):
                # Remove expired cache
                os.remove(cache_file)
                return None
            
            return cache_data.get('data')
        
        except Exception as e:
            current_app.logger.error(f"Error reading cache for {username}: {str(e)}")
            return None
    
    def set_user_data(self, username, data):
        """
        Cache user data
        
        Args:
            username (str): GitHub username
            data (dict): User data to cache
        """
        try:
            cache_file = self._get_cache_file_path(username)
            
            cache_data = {
                'timestamp': datetime.now().isoformat(),
                'data': data
            }
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)
        
        except Exception as e:
            current_app.logger.error(f"Error writing cache for {username}: {str(e)}")
    
    def clear_user_cache(self, username):
        """
        Clear cache for a specific user
        
        Args:
            username (str): GitHub username
        """
        try:
            cache_file = self._get_cache_file_path(username)
            if os.path.exists(cache_file):
                os.remove(cache_file)
                return True
            return False
        except Exception as e:
            current_app.logger.error(f"Error clearing cache for {username}: {str(e)}")
            return False
    
    def clear_all(self):
        """Clear all cached data"""
        try:
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.json'):
                    file_path = os.path.join(self.cache_dir, filename)
                    os.remove(file_path)
            return True
        except Exception as e:
            current_app.logger.error(f"Error clearing all cache: {str(e)}")
            return False
    
    def get_cache_stats(self):
        """
        Get cache statistics
        
        Returns:
            dict: Cache statistics
        """
        try:
            stats = {
                'total_files': 0,
                'valid_files': 0,
                'expired_files': 0,
                'total_size': 0,
                'oldest_cache': None,
                'newest_cache': None
            }
            
            oldest_time = None
            newest_time = None
            
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.json'):
                    file_path = os.path.join(self.cache_dir, filename)
                    stats['total_files'] += 1
                    stats['total_size'] += os.path.getsize(file_path)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            cache_data = json.load(f)
                        
                        if self._is_cache_valid(cache_data):
                            stats['valid_files'] += 1
                            cache_time = datetime.fromisoformat(cache_data['timestamp'])
                            
                            if oldest_time is None or cache_time < oldest_time:
                                oldest_time = cache_time
                            
                            if newest_time is None or cache_time > newest_time:
                                newest_time = cache_time
                        else:
                            stats['expired_files'] += 1
                    
                    except Exception:
                        stats['expired_files'] += 1
            
            if oldest_time:
                stats['oldest_cache'] = oldest_time.isoformat()
            if newest_time:
                stats['newest_cache'] = newest_time.isoformat()
            
            return stats
        
        except Exception as e:
            current_app.logger.error(f"Error getting cache stats: {str(e)}")
            return {}
    
    def cleanup_expired(self):
        """Remove all expired cache files"""
        try:
            removed_count = 0
            
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.json'):
                    file_path = os.path.join(self.cache_dir, filename)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            cache_data = json.load(f)
                        
                        if not self._is_cache_valid(cache_data):
                            os.remove(file_path)
                            removed_count += 1
                    
                    except Exception:
                        # Remove corrupted cache files
                        os.remove(file_path)
                        removed_count += 1
            
            return removed_count
        
        except Exception as e:
            current_app.logger.error(f"Error cleaning up expired cache: {str(e)}")
            return 0 