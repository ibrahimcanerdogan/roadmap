import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class TaskManager:
    def __init__(self, file_path: str = "tasks.json"):
        """Initialize TaskManager with JSON file path."""
        self.file_path = file_path
        self.tasks = self._load_tasks()
        self.next_id = self._get_next_id()

    def _load_tasks(self) -> List[Dict]:
        """Load tasks from JSON file or create empty list if file doesn't exist."""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as file:
                    return json.load(file)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def _save_tasks(self):
        """Save tasks to JSON file."""
        try:
            with open(self.file_path, 'w') as file:
                json.dump(self.tasks, file, indent=2)
        except IOError as e:
            raise Exception(f"Failed to save tasks: {e}")

    def _get_next_id(self) -> int:
        """Get the next available task ID."""
        if not self.tasks:
            return 1
        return max(task['id'] for task in self.tasks) + 1

    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        return datetime.now().isoformat()

    def add_task(self, description: str) -> int:
        """Add a new task and return its ID."""
        if not description.strip():
            raise ValueError("Task description cannot be empty")
        
        task = {
            'id': self.next_id,
            'description': description.strip(),
            'status': 'todo',
            'createdAt': self._get_timestamp(),
            'updatedAt': self._get_timestamp()
        }
        
        self.tasks.append(task)
        self._save_tasks()
        self.next_id += 1
        return task['id']

    def update_task(self, task_id: int, description: str) -> bool:
        """Update task description and return success status."""
        if not description.strip():
            raise ValueError("Task description cannot be empty")
        
        for task in self.tasks:
            if task['id'] == task_id:
                task['description'] = description.strip()
                task['updatedAt'] = self._get_timestamp()
                self._save_tasks()
                return True
        return False

    def delete_task(self, task_id: int) -> bool:
        """Delete a task and return success status."""
        for i, task in enumerate(self.tasks):
            if task['id'] == task_id:
                del self.tasks[i]
                self._save_tasks()
                return True
        return False

    def mark_task_status(self, task_id: int, status: str) -> bool:
        """Mark task as todo, in-progress, or done and return success status."""
        valid_statuses = ['todo', 'in-progress', 'done']
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
        
        for task in self.tasks:
            if task['id'] == task_id:
                task['status'] = status
                task['updatedAt'] = self._get_timestamp()
                self._save_tasks()
                return True
        return False

    def list_tasks(self, status_filter: Optional[str] = None) -> List[Dict]:
        """List all tasks or filter by status."""
        if status_filter:
            valid_statuses = ['todo', 'in-progress', 'done']
            if status_filter not in valid_statuses:
                raise ValueError(f"Invalid status filter. Must be one of: {', '.join(valid_statuses)}")
            return [task for task in self.tasks if task['status'] == status_filter]
        return self.tasks

    def get_task(self, task_id: int) -> Optional[Dict]:
        """Get a specific task by ID."""
        for task in self.tasks:
            if task['id'] == task_id:
                return task
        return None 