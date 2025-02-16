import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
import time

# Initialize Firebase Admin SDK
cred = credentials.Certificate("to-do-list-46c39-firebase-adminsdk-fbsvc-b9c4cee96c.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Collection reference
tasks_ref = db.collection("tasks")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_tasks():
    tasks = tasks_ref.stream()
    for idx, task in enumerate(tasks):
        task_data = task.to_dict()
        status = "✓" if task_data.get("done", False) else "✗"
        print(f"{idx + 1}. [{status}] {task_data['title']} - {task_data.get('description', 'No description')}")
    print()

def add_task():
    clear_screen()
    print("=== Agregar Tarea ===")
    title = input("Título: ")
    description = input("Descripción: ")
    tasks_ref.add({
        "title": title,
        "description": description,
        "done": False
    })
    print("Tarea agregada con éxito!")
    time.sleep(2)

def edit_task():
    clear_screen()
    print("=== Editar Tarea ===")
    display_tasks()
    try:
        task_number = int(input("Selecciona el número de la tarea a editar (0 para cancelar): "))
        if task_number == 0:
            return
        tasks = list(tasks_ref.stream())
        if 1 <= task_number <= len(tasks):
            task = tasks[task_number - 1]
            new_title = input(f"Nuevo título ({task.to_dict()['title']}): ") or task.to_dict()['title']
            new_description = input(f"Nueva descripción ({task.to_dict().get('description', 'No description')}): ") or task.to_dict().get('description', 'No description')
            tasks_ref.document(task.id).update({
                "title": new_title,
                "description": new_description
            })
            print("Tarea editada con éxito!")
        else:
            print("Número de tarea inválido.")
    except ValueError:
        print("Entrada inválida.")
    time.sleep(2)

def delete_task():
    clear_screen()
    print("=== Borrar Tarea ===")
    display_tasks()
    try:
        task_number = int(input("Selecciona el número de la tarea a borrar (0 para cancelar): "))
        if task_number == 0:
            return
        tasks = list(tasks_ref.stream())
        if 1 <= task_number <= len(tasks):
            task = tasks[task_number - 1]
            tasks_ref.document(task.id).delete()
            print("Tarea borrada con éxito!")
        else:
            print("Número de tarea inválido.")
    except ValueError:
        print("Entrada inválida.")
    time.sleep(2)

def mark_task_done():
    clear_screen()
    print("=== Marcar Tarea como Hecha ===")
    display_tasks()
    try:
        task_number = int(input("Selecciona el número de la tarea a marcar como hecha (0 para cancelar): "))
        if task_number == 0:
            return
        tasks = list(tasks_ref.stream())
        if 1 <= task_number <= len(tasks):
            task = tasks[task_number - 1]
            tasks_ref.document(task.id).update({
                "done": True
            })
            print("Tarea marcada como hecha!")
        else:
            print("Número de tarea inválido.")
    except ValueError:
        print("Entrada inválida.")
    time.sleep(2)

def main_menu():
    while True:
        clear_screen()
        print("=== To-Do List ===")
        print("1. Ver Tareas")
        print("2. Agregar Tarea")
        print("3. Editar Tarea")
        print("4. Borrar Tarea")
        print("5. Marcar Tarea como Hecha")
        print("6. Salir")
        choice = input("Selecciona una opción: ")
        
        if choice == "1":
            clear_screen()
            print("=== Tareas ===")
            display_tasks()
            input("Presiona Enter para continuar...")
        elif choice == "2":
            add_task()
        elif choice == "3":
            edit_task()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            mark_task_done()
        elif choice == "6":
            print("Saliendo...")
            break
        else:
            print("Opción inválida. Intenta de nuevo.")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()