from datetime import datetime
import re

def format_activity_data(events):
    """
    Format GitHub events for display
    
    Args:
        events (list): Raw GitHub events from API
        
    Returns:
        list: Formatted activity data
    """
    formatted_activities = []
    
    for event in events:
        activity = {
            'type': event.get('type', 'Unknown'),
            'created_at': format_date(event.get('created_at')),
            'repo_name': extract_repo_name(event.get('repo', {}).get('name', '')),
            'description': generate_description(event),
            'icon': get_event_icon(event.get('type', '')),
            'url': extract_event_url(event),
            'raw_event': event  # Keep raw event for additional processing
        }
        formatted_activities.append(activity)
    
    return formatted_activities

def get_user_profile_data(user_info):
    """
    Extract and format user profile information
    
    Args:
        user_info (dict): Raw user info from GitHub API
        
    Returns:
        dict: Formatted user profile data
    """
    if not user_info:
        return {}
    
    return {
        'name': user_info.get('name', ''),
        'login': user_info.get('login', ''),
        'avatar_url': user_info.get('avatar_url', ''),
        'bio': user_info.get('bio', ''),
        'location': user_info.get('location', ''),
        'company': user_info.get('company', ''),
        'blog': user_info.get('blog', ''),
        'twitter_username': user_info.get('twitter_username', ''),
        'public_repos': user_info.get('public_repos', 0),
        'public_gists': user_info.get('public_gists', 0),
        'followers': user_info.get('followers', 0),
        'following': user_info.get('following', 0),
        'created_at': format_date(user_info.get('created_at')),
        'updated_at': format_date(user_info.get('updated_at')),
        'hireable': user_info.get('hireable', False),
        'type': user_info.get('type', 'User')
    }

def format_date(date_string):
    """
    Format date string to readable format
    
    Args:
        date_string (str): ISO date string from GitHub API
        
    Returns:
        str: Formatted date string
    """
    if not date_string:
        return 'Unknown date'
    
    try:
        dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        return dt.strftime('%B %d, %Y at %I:%M %p')
    except ValueError:
        return date_string

def format_relative_date(date_string):
    """
    Format date as relative time (e.g., "2 hours ago")
    
    Args:
        date_string (str): ISO date string from GitHub API
        
    Returns:
        str: Relative time string
    """
    if not date_string:
        return 'Unknown time'
    
    try:
        dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        now = datetime.now(dt.tzinfo)
        diff = now - dt
        
        if diff.days > 0:
            if diff.days == 1:
                return '1 day ago'
            elif diff.days < 7:
                return f'{diff.days} days ago'
            elif diff.days < 30:
                weeks = diff.days // 7
                return f'{weeks} week{"s" if weeks > 1 else ""} ago'
            else:
                months = diff.days // 30
                return f'{months} month{"s" if months > 1 else ""} ago'
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f'{hours} hour{"s" if hours > 1 else ""} ago'
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f'{minutes} minute{"s" if minutes > 1 else ""} ago'
        else:
            return 'Just now'
    except ValueError:
        return date_string

def extract_repo_name(repo_name):
    """
    Extract repository name from full repo name
    
    Args:
        repo_name (str): Full repository name (owner/repo)
        
    Returns:
        str: Repository name
    """
    if not repo_name:
        return 'Unknown repository'
    
    parts = repo_name.split('/')
    return parts[-1] if len(parts) > 1 else repo_name

def extract_repo_owner(repo_name):
    """
    Extract repository owner from full repo name
    
    Args:
        repo_name (str): Full repository name (owner/repo)
        
    Returns:
        str: Repository owner
    """
    if not repo_name:
        return 'Unknown'
    
    parts = repo_name.split('/')
    return parts[0] if len(parts) > 1 else 'Unknown'

def generate_description(event):
    """
    Generate human-readable description for GitHub event
    
    Args:
        event (dict): GitHub event data
        
    Returns:
        str: Human-readable description
    """
    event_type = event.get('type', '')
    actor = event.get('actor', {}).get('login', 'User')
    repo_name = extract_repo_name(event.get('repo', {}).get('name', ''))
    
    descriptions = {
        'PushEvent': f'Pushed commits to {repo_name}',
        'CreateEvent': f'Created {event.get("payload", {}).get("ref_type", "repository")} in {repo_name}',
        'DeleteEvent': f'Deleted {event.get("payload", {}).get("ref_type", "repository")} in {repo_name}',
        'ForkEvent': f'Forked {repo_name}',
        'WatchEvent': f'Starred {repo_name}',
        'IssuesEvent': f'{event.get("payload", {}).get("action", "Updated")} an issue in {repo_name}',
        'IssueCommentEvent': f'Commented on an issue in {repo_name}',
        'PullRequestEvent': f'{event.get("payload", {}).get("action", "Updated")} a pull request in {repo_name}',
        'PullRequestReviewEvent': f'Reviewed a pull request in {repo_name}',
        'CommitCommentEvent': f'Commented on a commit in {repo_name}',
        'ReleaseEvent': f'Released {event.get("payload", {}).get("release", {}).get("tag_name", "version")} in {repo_name}',
        'GollumEvent': f'Updated wiki pages in {repo_name}',
        'MemberEvent': f'{event.get("payload", {}).get("action", "Updated")} member access in {repo_name}',
        'PublicEvent': f'Made {repo_name} public',
        'GistEvent': f'{event.get("payload", {}).get("action", "Updated")} a gist'
    }
    
    return descriptions.get(event_type, f'Performed {event_type.lower().replace("event", "")} in {repo_name}')

def get_event_icon(event_type):
    """
    Get appropriate icon for event type
    
    Args:
        event_type (str): GitHub event type
        
    Returns:
        str: Icon class or emoji
    """
    icons = {
        'PushEvent': '🚀',
        'CreateEvent': '✨',
        'DeleteEvent': '🗑️',
        'ForkEvent': '🍴',
        'WatchEvent': '⭐',
        'IssuesEvent': '🐛',
        'IssueCommentEvent': '💬',
        'PullRequestEvent': '🔀',
        'PullRequestReviewEvent': '👀',
        'CommitCommentEvent': '💬',
        'ReleaseEvent': '🏷️',
        'GollumEvent': '📝',
        'MemberEvent': '👥',
        'PublicEvent': '🌍',
        'GistEvent': '📄'
    }
    
    return icons.get(event_type, '📋')

def extract_event_url(event):
    """
    Extract relevant URL for the event
    
    Args:
        event (dict): GitHub event data
        
    Returns:
        str: Event URL or None
    """
    event_type = event.get('type', '')
    
    if event_type == 'PushEvent':
        return event.get('payload', {}).get('commits', [{}])[0].get('url')
    elif event_type in ['IssuesEvent', 'IssueCommentEvent']:
        return event.get('payload', {}).get('issue', {}).get('html_url')
    elif event_type in ['PullRequestEvent', 'PullRequestReviewEvent']:
        return event.get('payload', {}).get('pull_request', {}).get('html_url')
    elif event_type == 'ForkEvent':
        return event.get('payload', {}).get('forkee', {}).get('html_url')
    elif event_type == 'ReleaseEvent':
        return event.get('payload', {}).get('release', {}).get('html_url')
    else:
        return event.get('repo', {}).get('url')

def get_commit_message(event):
    """
    Extract commit message from push event
    
    Args:
        event (dict): GitHub event data
        
    Returns:
        str: Commit message or None
    """
    if event.get('type') == 'PushEvent':
        commits = event.get('payload', {}).get('commits', [])
        if commits:
            return commits[0].get('message', '')
    return None

def get_issue_title(event):
    """
    Extract issue title from issue event
    
    Args:
        event (dict): GitHub event data
        
    Returns:
        str: Issue title or None
    """
    if event.get('type') in ['IssuesEvent', 'IssueCommentEvent']:
        return event.get('payload', {}).get('issue', {}).get('title', '')
    return None

def get_pull_request_title(event):
    """
    Extract pull request title from PR event
    
    Args:
        event (dict): GitHub event data
        
    Returns:
        str: Pull request title or None
    """
    if event.get('type') in ['PullRequestEvent', 'PullRequestReviewEvent']:
        return event.get('payload', {}).get('pull_request', {}).get('title', '')
    return None

def format_number(num):
    """
    Format number with K, M suffixes
    
    Args:
        num (int): Number to format
        
    Returns:
        str: Formatted number
    """
    if num >= 1000000:
        return f'{num/1000000:.1f}M'
    elif num >= 1000:
        return f'{num/1000:.1f}K'
    else:
        return str(num)

def sanitize_username(username):
    """
    Sanitize username for safe use in URLs and filenames
    
    Args:
        username (str): Raw username
        
    Returns:
        str: Sanitized username
    """
    if not username:
        return ''
    
    # Remove any non-alphanumeric characters except hyphens and underscores
    sanitized = re.sub(r'[^a-zA-Z0-9\-_]', '', username)
    return sanitized.lower()

def get_activity_summary(events):
    """
    Generate a summary of user activity
    
    Args:
        events (list): List of GitHub events
        
    Returns:
        dict: Activity summary
    """
    summary = {
        'total_events': len(events),
        'event_types': {},
        'repositories': {},
        'most_active_hour': None,
        'most_active_day': None,
        'activity_period': None
    }
    
    hour_counts = {}
    day_counts = {}
    timestamps = []
    
    for event in events:
        event_type = event.get('type', 'Unknown')
        repo_name = event.get('repo', {}).get('name', 'Unknown')
        created_at = event.get('created_at')
        
        # Count event types
        summary['event_types'][event_type] = summary['event_types'].get(event_type, 0) + 1
        
        # Count repositories
        summary['repositories'][repo_name] = summary['repositories'].get(repo_name, 0) + 1
        
        # Process timestamp
        if created_at:
            try:
                dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                timestamps.append(dt)
                
                # Count by hour
                hour = dt.hour
                hour_counts[hour] = hour_counts.get(hour, 0) + 1
                
                # Count by day
                day = dt.strftime('%A')
                day_counts[day] = day_counts.get(day, 0) + 1
            except:
                pass
    
    # Find most active hour and day
    if hour_counts:
        summary['most_active_hour'] = max(hour_counts, key=hour_counts.get)
    if day_counts:
        summary['most_active_day'] = max(day_counts, key=day_counts.get)
    
    # Calculate activity period
    if timestamps:
        timestamps.sort()
        summary['activity_period'] = {
            'start': timestamps[0].isoformat(),
            'end': timestamps[-1].isoformat(),
            'duration_days': (timestamps[-1] - timestamps[0]).days
        }
    
    return summary 