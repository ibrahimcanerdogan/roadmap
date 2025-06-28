#!/usr/bin/env python3
"""
Task Tracker Web Application
A web-based version of the task tracker using Flask
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from task_manager import TaskManager
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'task-tracker-secret-key-2024'

# Initialize task manager
task_manager = TaskManager()

@app.route('/')
def index():
    """Main page showing all tasks."""
    tasks = task_manager.list_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    """Add a new task."""
    if request.method == 'POST':
        description = request.form.get('description', '').strip()
        if description:
            try:
                task_id = task_manager.add_task(description)
                flash(f'Task added successfully! (ID: {task_id})', 'success')
                return redirect(url_for('index'))
            except ValueError as e:
                flash(str(e), 'error')
        else:
            flash('Task description cannot be empty', 'error')
    
    return render_template('add_task.html')

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    """Edit an existing task."""
    task = task_manager.get_task(task_id)
    if not task:
        flash('Task not found', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        description = request.form.get('description', '').strip()
        if description:
            try:
                if task_manager.update_task(task_id, description):
                    flash('Task updated successfully!', 'success')
                    return redirect(url_for('index'))
                else:
                    flash('Failed to update task', 'error')
            except ValueError as e:
                flash(str(e), 'error')
        else:
            flash('Task description cannot be empty', 'error')
    
    return render_template('edit_task.html', task=task)

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    """Delete a task."""
    if task_manager.delete_task(task_id):
        flash('Task deleted successfully!', 'success')
    else:
        flash('Task not found', 'error')
    return redirect(url_for('index'))

@app.route('/status/<int:task_id>/<status>', methods=['POST'])
def change_status(task_id, status):
    """Change task status."""
    valid_statuses = ['todo', 'in-progress', 'done']
    if status not in valid_statuses:
        flash('Invalid status', 'error')
        return redirect(url_for('index'))
    
    status_messages = {
        'todo': 'Task marked as pending!',
        'in-progress': 'Task marked as in progress!',
        'done': 'Task marked as completed!'
    }
    
    if task_manager.mark_task_status(task_id, status):
        flash(status_messages[status], 'success')
    else:
        flash('Task not found', 'error')
    return redirect(url_for('index'))

@app.route('/filter/<status>')
def filter_tasks(status):
    """Filter tasks by status."""
    valid_statuses = ['todo', 'in-progress', 'done']
    if status not in valid_statuses:
        flash('Invalid status filter', 'error')
        return redirect(url_for('index'))
    
    tasks = task_manager.list_tasks(status)
    return render_template('index.html', tasks=tasks, current_filter=status)

@app.route('/api/tasks', methods=['GET'])
def api_get_tasks():
    """API endpoint to get all tasks."""
    tasks = task_manager.list_tasks()
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def api_add_task():
    """API endpoint to add a task."""
    data = request.get_json()
    description = data.get('description', '').strip()
    
    if not description:
        return jsonify({'error': 'Task description cannot be empty'}), 400
    
    try:
        task_id = task_manager.add_task(description)
        return jsonify({'id': task_id, 'message': 'Task added successfully'}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def api_update_task(task_id):
    """API endpoint to update a task."""
    data = request.get_json()
    description = data.get('description', '').strip()
    
    if not description:
        return jsonify({'error': 'Task description cannot be empty'}), 400
    
    try:
        if task_manager.update_task(task_id, description):
            return jsonify({'message': 'Task updated successfully'})
        else:
            return jsonify({'error': 'Task not found'}), 404
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def api_delete_task(task_id):
    """API endpoint to delete a task."""
    if task_manager.delete_task(task_id):
        return jsonify({'message': 'Task deleted successfully'})
    else:
        return jsonify({'error': 'Task not found'}), 404

@app.route('/api/tasks/<int:task_id>/status', methods=['PUT'])
def api_change_status(task_id):
    """API endpoint to change task status."""
    data = request.get_json()
    status = data.get('status')
    
    valid_statuses = ['todo', 'in-progress', 'done']
    if status not in valid_statuses:
        return jsonify({'error': 'Invalid status'}), 400
    
    status_messages = {
        'todo': 'Task marked as pending',
        'in-progress': 'Task marked as in progress',
        'done': 'Task marked as completed'
    }
    
    if task_manager.mark_task_status(task_id, status):
        return jsonify({'message': status_messages[status]})
    else:
        return jsonify({'error': 'Task not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 