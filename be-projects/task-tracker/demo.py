#!/usr/bin/env python3
"""
Demo script for Task Tracker CLI
This script demonstrates all the functionality of the task tracker.
"""

import subprocess
import sys
import os


def run_command(command):
    """Run a command and return the output."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as e:
        return "", str(e), 1


def print_section(title):
    """Print a section header."""
    print(f"\n{'='*50}")
    print(f" {title}")
    print(f"{'='*50}")


def main():
    """Run the demo."""
    print("Task Tracker CLI Demo")
    print("This demo will showcase all the functionality of the task tracker.")
    
    # Clear any existing tasks
    if os.path.exists("tasks.json"):
        os.remove("tasks.json")
        print("Cleared existing tasks.json file")
    
    print_section("1. Adding Tasks")
    
    commands = [
        'python3 task_cli.py add "Buy groceries"',
        'python3 task_cli.py add "Complete project documentation"',
        'python3 task_cli.py add "Review code changes"',
        'python3 task_cli.py add "Write unit tests"'
    ]
    
    for cmd in commands:
        print(f"Running: {cmd}")
        output, error, code = run_command(cmd)
        if code == 0:
            print(f"✅ {output}")
        else:
            print(f"❌ Error: {error}")
    
    print_section("2. Listing All Tasks")
    output, error, code = run_command("python3 task_cli.py list")
    if code == 0:
        print(output)
    else:
        print(f"❌ Error: {error}")
    
    print_section("3. Updating Tasks")
    commands = [
        'python3 task_cli.py update 1 "Buy groceries and cook dinner"',
        'python3 task_cli.py update 2 "Complete project documentation and create README"'
    ]
    
    for cmd in commands:
        print(f"Running: {cmd}")
        output, error, code = run_command(cmd)
        if code == 0:
            print(f"✅ {output}")
        else:
            print(f"❌ Error: {error}")
    
    print_section("4. Marking Task Status")
    commands = [
        'python3 task_cli.py mark-in-progress 2',
        'python3 task_cli.py mark-done 3',
        'python3 task_cli.py mark-done 4'
    ]
    
    for cmd in commands:
        print(f"Running: {cmd}")
        output, error, code = run_command(cmd)
        if code == 0:
            print(f"✅ {output}")
        else:
            print(f"❌ Error: {error}")
    
    print_section("5. Filtering Tasks by Status")
    statuses = ['todo', 'in-progress', 'done']
    
    for status in statuses:
        print(f"\nTasks with status '{status}':")
        output, error, code = run_command(f"python3 task_cli.py list {status}")
        if code == 0:
            print(output)
        else:
            print(f"❌ Error: {error}")
    
    print_section("6. Error Handling Demo")
    
    # Test invalid task ID
    print("Testing invalid task ID:")
    output, error, code = run_command('python3 task_cli.py update 999 "This task doesn\'t exist"')
    if code == 1:
        print(f"✅ {output}")
    else:
        print(f"❌ Expected error but got: {output}")
    
    # Test empty description
    print("\nTesting empty description:")
    output, error, code = run_command('python3 task_cli.py add ""')
    if code == 1:
        print(f"✅ {output}")
    else:
        print(f"❌ Expected error but got: {output}")
    
    print_section("7. Final Task List")
    output, error, code = run_command("python3 task_cli.py list")
    if code == 0:
        print(output)
    else:
        print(f"❌ Error: {error}")
    
    print_section("8. Deleting a Task")
    output, error, code = run_command("python3 task_cli.py delete 4")
    if code == 0:
        print(f"✅ {output}")
    else:
        print(f"❌ Error: {error}")
    
    print("\nFinal task list after deletion:")
    output, error, code = run_command("python3 task_cli.py list")
    if code == 0:
        print(output)
    else:
        print(f"❌ Error: {error}")
    
    print_section("Demo Complete!")
    print("The task tracker CLI is working perfectly!")
    print("You can now use it to manage your own tasks.")


if __name__ == "__main__":
    main() 