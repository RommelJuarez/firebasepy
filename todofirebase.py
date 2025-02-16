import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
import time

# Initialize the Firebase Admin SDK with the provided credentials
cred = credentials.Certificate("to-do-list-46c39-firebase-adminsdk-fbsvc-b9c4cee96c.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Reference to the tasks collection in Firestore
tasks_ref = db.collection("tasks")

def clear_screen():
    """Clears the console screen for better display."""
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to add a new task to the database
def add_task():
    try:
        task_name = input("Enter task name: ")
        task_description = input("Enter task description: ")
        task = {
            "name": task_name,
            "description": task_description,
            "done": False  # Initially marks the task as not done
        }
        # Adds the task to the Firestore collection
        tasks_ref.add(task)
        clear_screen()
        print("Task added successfully!")
        time.sleep(3)
    except Exception as e:
        print(f"An error occurred: {e}. Please try again.")
        time.sleep(2)

# Function to mark a task as completed or not completed
def mark_task_as_done():
    try:
        show_pending_tasks()  # Shows pending tasks
        task_choice = input("Choose task number to mark (1 for Done, 2 for Not Done): ")
        if task_choice.isdigit():
            task_choice = int(task_choice)
            tasks = tasks_ref.where("done", "==", False).stream()  # Filters for incomplete tasks
            tasks_list = list(tasks)
            
            if task_choice <= len(tasks_list) and task_choice > 0:
                task_ref = tasks_list[task_choice - 1].reference
                done_choice = input("Enter 1 to mark as done or 2 to mark as not done: ")
                
                if done_choice == '1':
                    task_ref.update({"done": True})  # Updates the task's status in Firestore
                    clear_screen()
                    print(f"Task {task_choice} marked as done!")
                    time.sleep(3)
                elif done_choice == '2':
                    task_ref.update({"done": False})  # Updates the task's status in Firestore
                    clear_screen()
                    print(f"Task {task_choice} marked as not done!")
                    time.sleep(3)
                else:
                    print("Invalid option. Please try again.")
                    time.sleep(2)
            else:
                print("Invalid task number. Please try again.")
                time.sleep(2)
        else:
            print("Invalid input. Please enter a number.")
            time.sleep(2)
    except Exception as e:
        print(f"An error occurred: {e}. Please try again.")
        time.sleep(2)

# Function to delete a task from the database
def delete_task():
    try:
        show_tasks()  # Shows all tasks
        task_choice = input("Choose task number to delete: ")
        if task_choice.isdigit():
            task_choice = int(task_choice)
            tasks = tasks_ref.stream()  # Fetches all tasks from the collection
            tasks_list = list(tasks)
            
            if task_choice <= len(tasks_list) and task_choice > 0:
                task_ref = tasks_list[task_choice - 1].reference
                task_ref.delete()  # Deletes the task from Firestore
                clear_screen()
                print(f"Task {task_choice} deleted successfully.")
                time.sleep(3)
            else:
                print("Invalid task number. Please try again.")
                time.sleep(2)
        else:
            print("Invalid input. Please enter a number.")
            time.sleep(2)
    except Exception as e:
        print(f"An error occurred: {e}. Please try again.")
        time.sleep(2)

# Function to edit an existing task
def edit_task():
    try:
        show_tasks()  # Shows all tasks
        task_choice = input("Choose task number to edit: ")
        if task_choice.isdigit():
            task_choice = int(task_choice)
            tasks = tasks_ref.stream()  # Fetches all tasks from Firestore
            tasks_list = list(tasks)

            if task_choice <= len(tasks_list) and task_choice > 0:
                task_ref = tasks_list[task_choice - 1].reference
                task = task_ref.get()  # Retrieves the task's data
                task_data = task.to_dict()
                
                # Prompts the user for new task details
                new_name = input(f"Enter new name (current: {task_data['name']}): ")
                new_description = input(f"Enter new description (current: {task_data['description']}): ")
                
                # Updates the task with new values
                task_ref.update({
                    "name": new_name,
                    "description": new_description
                })
                clear_screen()
                print(f"Task {task_choice} updated successfully.")
                time.sleep(3)
            else:
                print("Invalid task number. Please try again.")
                time.sleep(2)
        else:
            print("Invalid input. Please enter a number.")
            time.sleep(2)
    except Exception as e:
        print(f"An error occurred: {e}. Please try again.")
        time.sleep(2)

# Function to display all tasks
def show_tasks():
    try:
        tasks = tasks_ref.stream()  # Fetches all tasks from Firestore
        clear_screen()
        if not tasks:
            print("No tasks available.")
            time.sleep(2)
        else:
            print("\nTasks List:")
            for index, task in enumerate(tasks, 1):
                task_data = task.to_dict()
                status = "Done" if task_data["done"] else "Pending"
                print(f"{index}. {task_data['name']} - {task_data['description']} - {status}")
    except Exception as e:
        print(f"An error occurred: {e}. Please try again.")
        time.sleep(2)

# Function to show tasks with an option to go back to the main menu
def show_tasks_option():
    try:
        tasks = tasks_ref.stream()  # Fetches all tasks from Firestore
        if not tasks:
            print("No tasks available.")
            time.sleep(2)
        else:
            print("\nTasks List:")
            for index, task in enumerate(tasks, 1):
                task_data = task.to_dict()
                status = "Done" if task_data["done"] else "Pending"
                print(f"{index}. {task_data['name']} - {task_data['description']} - {status}")
            print("\n Press Enter to go back")
            return_to_menu = input("")  # Waits for the user to press Enter to return to menu
            
            clear_screen()
            return
           
    except Exception as e:
        print(f"An error occurred: {e}. Please try again.")
        time.sleep(2)

# Function to show only pending tasks
def show_pending_tasks():
    try:
        tasks = tasks_ref.where("done", "==", False).stream()  # Filters for pending tasks
        tasks_list = list(tasks)
        if not tasks_list:
            print("No pending tasks available.")
            time.sleep(2)
        else:
            print("\nPending Tasks:")
            for index, task in enumerate(tasks_list, 1):
                task_data = task.to_dict()
                print(f"{index}. {task_data['name']} - {task_data['description']}")
            
    except Exception as e:
        print(f"An error occurred: {e}. Please try again.")
        time.sleep(2)

# Main menu function
def menu():
    while True:
        clear_screen()
        print("\nTo-Do List Menu")
        print("1. Add Task")
        print("2. Mark Task as Done or Not Done")
        print("3. Delete Task")
        print("4. Edit Task")
        print("5. Show All Tasks")
        print("6. Exit")

        try:
            choice = input("Choose an option: ")

            if choice == "1":
                add_task()
            elif choice == "2":
                mark_task_as_done()
            elif choice == "3":
                delete_task()
            elif choice == "4":
                edit_task()
            elif choice == "5":
                show_tasks_option()
            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
                time.sleep(2)
        except Exception as e:
            print(f"An error occurred: {e}. Please try again.")
            time.sleep(2)

# Run the menu if this is the main script
if __name__ == "__main__":
    menu()
