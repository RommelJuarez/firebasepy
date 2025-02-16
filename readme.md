# Overview

This project is a console-based To-Do List application that integrates with Firebase Firestore, a cloud-based NoSQL database. The application allows users to manage tasks by adding, editing, deleting, and marking them as done or not done. The goal of this project is to gain experience in cloud database integration and improve backend development skills.

Users interact with the program via a simple text-based menu. The tasks are stored in Firestore, ensuring data persistence even if the application is closed.

[Software Demo Video](https://youtu.be/LQmeO9jPiHE)

# Cloud Database

The project uses **Firebase Firestore**, a NoSQL cloud database that allows real-time synchronization. The database structure consists of a single collection named **"tasks"**, where each document represents a task with the following fields:

- `name` (string): The name of the task
- `description` (string): A brief description of the task
- `done` (boolean): Indicates if the task is completed or not

# Development Environment

The software was developed using:

- **Programming Language**: Python
- **Libraries Used**:
  - `firebase-admin`: To interact with Firestore
  - `os`: For clearing the console screen
  - `time`: To introduce delays for better user experience

# Useful Websites

- [Firebase Firestore Documentation](https://firebase.google.com/docs/firestore)
- [Python Firebase Admin SDK](https://firebase.google.com/docs/admin/setup)
- [Markdown Guide](https://www.markdownguide.org/)

# Future Work

- Implement a graphical user interface (GUI) for better usability.
- Add authentication to allow multiple users to manage their own tasks.
- Enhance error handling and logging mechanisms.
- Allow task categorization and prioritization.
- Implement notifications or reminders for pending tasks.
