from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, session
from app.github_api import GitHubAPI
from app.utils import format_activity_data, get_user_profile_data
from app.cache import ActivityCache
import json

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    """Home page with username input form"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        if not username:
            flash('Please enter a GitHub username', 'error')
            return render_template('index.html')
        
        return redirect(url_for('main.user_activity', username=username))
    
    return render_template('index.html')

@main.route('/activity/<username>')
def user_activity(username):
    """Display GitHub user activity with enhanced features"""
    try:
        github_api = GitHubAPI()
        cache = ActivityCache()
        
        # Check cache first
        cached_data = cache.get_user_data(username)
        if cached_data:
            user_info = cached_data.get('user_info', {})
            events = cached_data.get('events', [])
            flash('Data loaded from cache', 'info')
        else:
            # Fetch fresh data
            user_info = github_api.get_user_info(username)
            events = github_api.get_user_events(username)
            
            # Cache the data
            cache.set_user_data(username, {
                'user_info': user_info,
                'events': events
            })
        
        if not events:
            flash(f'No activity found for user "{username}"', 'info')
            return render_template('activity.html', 
                                 username=username, 
                                 user_info=user_info,
                                 activities=[])
        
        formatted_activities = format_activity_data(events)
        
        # Get activity statistics
        activity_stats = get_activity_statistics(events)
        
        return render_template('activity.html', 
                             username=username, 
                             user_info=user_info,
                             activities=formatted_activities,
                             activity_stats=activity_stats)
    
    except Exception as e:
        flash(f'Error fetching activity for "{username}": {str(e)}', 'error')
        return render_template('activity.html', 
                             username=username, 
                             user_info={},
                             activities=[])

@main.route('/api/user/<username>')
def api_user_activity(username):
    """API endpoint for getting user activity data"""
    try:
        github_api = GitHubAPI()
        cache = ActivityCache()
        
        # Check cache first
        cached_data = cache.get_user_data(username)
        if cached_data:
            return jsonify(cached_data)
        
        # Fetch fresh data
        user_info = github_api.get_user_info(username)
        events = github_api.get_user_events(username)
        
        # Cache the data
        cache.set_user_data(username, {
            'user_info': user_info,
            'events': events
        })
        
        return jsonify({
            'user_info': user_info,
            'events': events
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@main.route('/api/activity/<username>/filter')
def api_filtered_activity(username):
    """API endpoint for filtered activity data"""
    try:
        event_type = request.args.get('type', 'all')
        limit = int(request.args.get('limit', 50))
        
        github_api = GitHubAPI()
        cache = ActivityCache()
        
        # Get cached data or fetch fresh
        cached_data = cache.get_user_data(username)
        if cached_data:
            events = cached_data.get('events', [])
        else:
            events = github_api.get_user_events(username)
            cache.set_user_data(username, {'events': events})
        
        # Filter events
        if event_type != 'all':
            events = [event for event in events if event.get('type') == event_type]
        
        # Limit results
        events = events[:limit]
        
        formatted_activities = format_activity_data(events)
        
        return jsonify({
            'activities': formatted_activities,
            'total': len(formatted_activities),
            'filter': event_type
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@main.route('/compare')
def compare_users():
    """Compare multiple users' activity"""
    return render_template('compare.html')

@main.route('/api/compare', methods=['POST'])
def api_compare_users():
    """API endpoint for comparing users"""
    try:
        data = request.get_json()
        usernames = data.get('usernames', [])
        
        if len(usernames) < 2:
            return jsonify({'error': 'Please provide at least 2 usernames'}), 400
        
        if len(usernames) > 5:
            return jsonify({'error': 'Maximum 5 users can be compared'}), 400
        
        github_api = GitHubAPI()
        cache = ActivityCache()
        
        comparison_data = {}
        
        for username in usernames:
            # Get cached data or fetch fresh
            cached_data = cache.get_user_data(username)
            if cached_data:
                user_info = cached_data.get('user_info', {})
                events = cached_data.get('events', [])
            else:
                user_info = github_api.get_user_info(username)
                events = github_api.get_user_events(username)
                cache.set_user_data(username, {
                    'user_info': user_info,
                    'events': events
                })
            
            activity_stats = get_activity_statistics(events)
            
            comparison_data[username] = {
                'user_info': user_info,
                'activity_stats': activity_stats,
                'events': events,  # Include events data for timeline
                'total_events': len(events)
            }
        
        return jsonify(comparison_data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@main.route('/trending')
def trending_users():
    """Show trending GitHub users"""
    try:
        # This would typically fetch from a trending API or cache
        trending_users = [
            'torvalds', 'gvanrossum', 'antirez', 'kamranahmedse',
            'tj', 'sindresorhus', 'addy-dclxvi', 'jashkenas'
        ]
        
        return render_template('trending.html', trending_users=trending_users)
    
    except Exception as e:
        flash(f'Error loading trending users: {str(e)}', 'error')
        return render_template('trending.html', trending_users=[])

@main.route('/clear-cache')
def clear_cache():
    """Clear the activity cache"""
    try:
        cache = ActivityCache()
        cache.clear_all()
        flash('Cache cleared successfully', 'success')
    except Exception as e:
        flash(f'Error clearing cache: {str(e)}', 'error')
    
    return redirect(url_for('main.index'))

def get_activity_statistics(events):
    """Generate detailed activity statistics"""
    stats = {
        'total_events': len(events),
        'event_types': {},
        'repositories': {},
        'activity_by_hour': {},
        'activity_by_day': {}
    }
    
    for event in events:
        event_type = event.get('type', 'Unknown')
        repo_name = event.get('repo', {}).get('name', 'Unknown')
        created_at = event.get('created_at')
        
        # Count event types
        stats['event_types'][event_type] = stats['event_types'].get(event_type, 0) + 1
        
        # Count repositories
        stats['repositories'][repo_name] = stats['repositories'].get(repo_name, 0) + 1
        
        # Activity by time (if we have timestamps)
        if created_at:
            try:
                from datetime import datetime
                dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                
                # Activity by hour
                hour = dt.hour
                stats['activity_by_hour'][hour] = stats['activity_by_hour'].get(hour, 0) + 1
                
                # Activity by day of week
                day = dt.strftime('%A')
                stats['activity_by_day'][day] = stats['activity_by_day'].get(day, 0) + 1
            except:
                pass
    
    return stats 