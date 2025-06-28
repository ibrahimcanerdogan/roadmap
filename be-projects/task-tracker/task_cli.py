#!/usr/bin/env python3
"""
Task Tracker CLI - A simple command-line task management tool
"""

import sys
import argparse
from task_manager import TaskManager


def print_task(task):
    """Print a single task in a formatted way."""
    status_icons = {
        'todo': '⏳',
        'in-progress': '🔄', 
        'done': '✅'
    }
    icon = status_icons.get(task['status'], '❓')
    print(f"{icon} [{task['id']}] {task['description']} ({task['status']})")


def print_tasks(tasks):
    """Print a list of tasks."""
    if not tasks:
        print("No tasks found.")
        return
    
    for task in tasks:
        print_task(task)


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Task Tracker CLI - Manage your tasks from the command line",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  task-cli add "Buy groceries"
  task-cli update 1 "Buy groceries and cook dinner"
  task-cli delete 1
  task-cli mark-in-progress 1
  task-cli mark-done 1
  task-cli list
  task-cli list done
  task-cli list todo
  task-cli list in-progress
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add task command
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('description', help='Task description')
    
    # Update task command
    update_parser = subparsers.add_parser('update', help='Update an existing task')
    update_parser.add_argument('task_id', type=int, help='Task ID to update')
    update_parser.add_argument('description', help='New task description')
    
    # Delete task command
    delete_parser = subparsers.add_parser('delete', help='Delete a task')
    delete_parser.add_argument('task_id', type=int, help='Task ID to delete')
    
    # Mark task status commands
    mark_in_progress_parser = subparsers.add_parser('mark-in-progress', help='Mark task as in progress')
    mark_in_progress_parser.add_argument('task_id', type=int, help='Task ID to mark as in progress')
    
    mark_done_parser = subparsers.add_parser('mark-done', help='Mark task as done')
    mark_done_parser.add_argument('task_id', type=int, help='Task ID to mark as done')
    
    # List tasks command
    list_parser = subparsers.add_parser('list', help='List tasks')
    list_parser.add_argument('status', nargs='?', choices=['todo', 'in-progress', 'done'], 
                           help='Filter tasks by status')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        task_manager = TaskManager()
        
        if args.command == 'add':
            task_id = task_manager.add_task(args.description)
            print(f"Task added successfully (ID: {task_id})")
            
        elif args.command == 'update':
            if task_manager.update_task(args.task_id, args.description):
                print(f"Task {args.task_id} updated successfully")
            else:
                print(f"Task {args.task_id} not found")
                sys.exit(1)
                
        elif args.command == 'delete':
            if task_manager.delete_task(args.task_id):
                print(f"Task {args.task_id} deleted successfully")
            else:
                print(f"Task {args.task_id} not found")
                sys.exit(1)
                
        elif args.command == 'mark-in-progress':
            if task_manager.mark_task_status(args.task_id, 'in-progress'):
                print(f"Task {args.task_id} marked as in progress")
            else:
                print(f"Task {args.task_id} not found")
                sys.exit(1)
                
        elif args.command == 'mark-done':
            if task_manager.mark_task_status(args.task_id, 'done'):
                print(f"Task {args.task_id} marked as done")
            else:
                print(f"Task {args.task_id} not found")
                sys.exit(1)
                
        elif args.command == 'list':
            tasks = task_manager.list_tasks(args.status)
            if args.status:
                print(f"Tasks with status '{args.status}':")
            else:
                print("All tasks:")
            print_tasks(tasks)
            
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 