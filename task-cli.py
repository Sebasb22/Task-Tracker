import sys
import json
import os
from datetime import datetime

TASKS_FILE = 'tasks.json'

# Asegurar que exista el archivo de tareas

def initialize_tasks_file():
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'w') as f:
            json.dump([], f)


# Cargar tareas desde el archivo
def load_tasks():
    with open(TASKS_FILE, 'r') as f:
        return json.load(f)
    
# Guardar tareas en el archivo
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

# Generar nuevo ID
def generate_id(tasks):
    if not tasks:
        return 1
    return max(task['id'] for task in tasks) + 1

# Comandos

def add_task(description):
    tasks = load_tasks()
    now = datetime.now().isoformat()
    task = {
        "id": generate_id(tasks),
        "description": description,
        "status": "todo",
        "createdAt": now,
        "updatedAt": now
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {task['id']})")

def update_task(task_id, description):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['description'] = description
            task['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
            print("Task updated successfully")
            return
    print("Task not found")

def delete_task(task_id):
    tasks = load_tasks()
    new_tasks = [task for task in tasks if task['id'] != task_id]
    if len(new_tasks) == len(tasks):
        print("Task not found")
    else:
        save_tasks(new_tasks)
        print("Task deleted successfully")

def mark_status(task_id, status):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = status
            task['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task marked as {status}")
            return
    print("Task not found")

def list_tasks(filter_status=None):
    tasks = load_tasks()
    if filter_status:
        tasks = [task for task in tasks if task['status'] == filter_status]
    if not tasks:
        print("No tasks found.")
        return
    for task in tasks:
        print(f"[{task['id']}] {task['description']} - {task['status']} (Created: {task['createdAt']})")

# Función principal
def main():
    initialize_tasks_file()
    args = sys.argv[1:]

    if not args:
        print("No command provided.")
        return

    command = args[0]

    if command == "add" and len(args) >= 2:
        description = " ".join(args[1:])
        add_task(description)
    elif command == "update" and len(args) >= 3:
        task_id = int(args[1])
        description = " ".join(args[2:])
        update_task(task_id, description)
    elif command == "delete" and len(args) == 2:
        task_id = int(args[1])
        delete_task(task_id)
    elif command == "mark-in-progress" and len(args) == 2:
        task_id = int(args[1])
        mark_status(task_id, "in-progress")
    elif command == "mark-done" and len(args) == 2:
        task_id = int(args[1])
        mark_status(task_id, "done")
    elif command == "list":
        if len(args) == 2:
            status = args[1]
            if status not in ["todo", "in-progress", "done"]:
                print("Invalid status. Use 'todo', 'in-progress' or 'done'.")
            else:
                list_tasks(status)
        else:
            list_tasks()
    else:
        print("Unknown command or wrong number of arguments.")

if __name__ == "__main__":
    main()