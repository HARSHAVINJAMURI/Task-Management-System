import json
from datetime import datetime, timedelta
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)
class TodoList:
    def __init__(self, filename='tasks.json'):
        self.filename = filename
        self.tasks = self.load_tasks()
    def load_tasks(self):
        try:
            with open(self.filename, 'r') as file:
                tasks = json.load(file)
            return tasks
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    def save_tasks(self):
        with open(self.filename, 'w') as file:
            json.dump(self.tasks, file, indent=2, cls=DateTimeEncoder)
    def add_task(self, title, priority='medium', due_date=None):
        task = {'title': title, 'priority': priority, 'due_date': due_date, 'completed': False}
        self.tasks.append(task)
        self.save_tasks()
        print(f'Task "{title}" added successfully.')
    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            removed_task = self.tasks.pop(index)
            self.save_tasks()
            print(f'Task "{removed_task["title"]}" removed successfully.')
        else:
            print('Invalid task index.')
    def mark_completed(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index]['completed'] = True
            self.save_tasks()
            print(f'Task "{self.tasks[index]["title"]}" marked as completed.')
        else:
            print('Invalid task index.')
    def display_tasks(self):
        if not self.tasks:
            print('No tasks found.')
        else:
            print('Task List:')
            for i, task in enumerate(self.tasks):
                status = 'Completed' if task['completed'] else 'Pending'
                due_date = f"Due on {task['due_date']}" if task['due_date'] else "No due date"
                print(f'{i + 1}. {task["title"]} - Priority: {task["priority"]}, Status: {status}, {due_date}')
def main():
    todo_list = TodoList()
    while True:
        print('\nCommand Menu:')
        print('1. Add Task')
        print('2. Remove Task')
        print('3. Mark Task as Completed')
        print('4. Display Tasks')
        print('5. Exit')
        choice = input('Enter your choice (1-5): ')
        if choice == '1':
            title = input('Enter task title: ')
            priority = input('Enter task priority (high/medium/low): ')
            due_date_str = input('Enter due date (YYYY-MM-DD, leave blank if none): ')
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d') if due_date_str else None
            todo_list.add_task(title, priority, due_date)
        elif choice == '2':
            index = int(input('Enter the index of the task to remove: ')) - 1
            todo_list.remove_task(index)
        elif choice == '3':
            index = int(input('Enter the index of the task to mark as completed: ')) - 1
            todo_list.mark_completed(index)
        elif choice == '4':
            todo_list.display_tasks()
        elif choice == '5':
            print('Exiting the application. Goodbye!')
            break
        else:
            print('Invalid choice. Please enter a number between 1 and 5.')
if __name__ == '__main__':
    main()