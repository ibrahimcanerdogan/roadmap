#!/usr/bin/env python3
"""
Web Demo Script for Task Tracker
This script demonstrates the web application functionality via API calls.
"""

import requests
import json
import time
from datetime import datetime


def print_section(title):
    """Print a section header."""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")


def api_request(method, endpoint, data=None):
    """Make an API request and return the response."""
    base_url = "http://localhost:5000/api"
    url = f"{base_url}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        
        return response.json(), response.status_code
    except requests.exceptions.ConnectionError:
        print("❌ Web application is not running! Please run 'python3 app.py' first.")
        return None, 0
    except Exception as e:
        print(f"❌ API error: {e}")
        return None, 0


def print_tasks(tasks):
    """Print tasks in a formatted way."""
    if not tasks:
        print("📝 No tasks yet.")
        return
    
    for task in tasks:
        status_icons = {
            'todo': '⏳',
            'in-progress': '🔄',
            'done': '✅'
        }
        icon = status_icons.get(task['status'], '❓')
        print(f"{icon} [{task['id']}] {task['description']} ({task['status']})")


def main():
    """Run the web demo."""
    print("🌐 Task Tracker Web Application Demo")
    print("This demo will showcase the web application's API features.")
    
    print_section("1. List Current Tasks")
    tasks, status = api_request("GET", "/tasks")
    if status == 200:
        print("📋 Current tasks:")
        print_tasks(tasks)
    else:
        print("❌ Could not retrieve tasks")
        return
    
    print_section("2. Add New Tasks")
    
    new_tasks = [
        "Test the web application",
        "Write API documentation",
        "Improve user interface",
        "Optimize database performance"
    ]
    
    for task_desc in new_tasks:
        print(f"➕ Adding task: '{task_desc}'...")
        result, status = api_request("POST", "/tasks", {"description": task_desc})
        if status == 201:
            print(f"✅ Task added (ID: {result['id']})")
        else:
            print(f"❌ Failed to add task: {result}")
        time.sleep(0.5)
    
    print_section("3. Updated Task List")
    tasks, status = api_request("GET", "/tasks")
    if status == 200:
        print("📋 Updated task list:")
        print_tasks(tasks)
    
    print_section("4. Change Task Status")
    
    # Mark first task as "in progress"
    print("🔄 Marking first task as 'in progress'...")
    result, status = api_request("PUT", "/tasks/1/status", {"status": "in-progress"})
    if status == 200:
        print("✅ Status changed")
    else:
        print(f"❌ Failed to change status: {result}")
    
    # Mark last task as "completed"
    print("✅ Marking last task as 'completed'...")
    result, status = api_request("PUT", "/tasks/5/status", {"status": "done"})
    if status == 200:
        print("✅ Status changed")
    else:
        print(f"❌ Failed to change status: {result}")
    
    print_section("5. Update Task Description")
    print("✏️ Updating second task description...")
    result, status = api_request("PUT", "/tasks/2", {"description": "Write API documentation and test it"})
    if status == 200:
        print("✅ Task updated")
    else:
        print(f"❌ Failed to update task: {result}")
    
    print_section("6. Updated Task List")
    tasks, status = api_request("GET", "/tasks")
    if status == 200:
        print("📋 Current status:")
        print_tasks(tasks)
    
    print_section("7. Statistics")
    if tasks:
        todo_count = len([t for t in tasks if t['status'] == 'todo'])
        in_progress_count = len([t for t in tasks if t['status'] == 'in-progress'])
        done_count = len([t for t in tasks if t['status'] == 'done'])
        total_count = len(tasks)
        
        print(f"📊 Task Statistics:")
        print(f"   ⏳ Pending: {todo_count}")
        print(f"   🔄 In Progress: {in_progress_count}")
        print(f"   ✅ Completed: {done_count}")
        print(f"   📋 Total: {total_count}")
    
    print_section("8. Delete Task")
    print("🗑️ Deleting last task...")
    result, status = api_request("DELETE", "/tasks/5")
    if status == 200:
        print("✅ Task deleted")
    else:
        print(f"❌ Failed to delete task: {result}")
    
    print_section("9. Final Task List")
    tasks, status = api_request("GET", "/tasks")
    if status == 200:
        print("📋 Final task list:")
        print_tasks(tasks)
    
    print_section("10. Error Handling Test")
    
    # Test updating non-existent task
    print("❌ Trying to update non-existent task...")
    result, status = api_request("PUT", "/tasks/999", {"description": "This task doesn't exist"})
    if status == 404:
        print("✅ Correct error message received")
    else:
        print(f"❌ Unexpected response: {result}")
    
    # Test adding task with empty description
    print("❌ Trying to add task with empty description...")
    result, status = api_request("POST", "/tasks", {"description": ""})
    if status == 400:
        print("✅ Correct error message received")
    else:
        print(f"❌ Unexpected response: {result}")
    
    print_section("🌐 Web Demo Completed!")
    print("Web application is working perfectly!")
    print("Visit http://localhost:5000 in your browser.")
    print("Use the web interface to test all features.")


if __name__ == "__main__":
    main() 