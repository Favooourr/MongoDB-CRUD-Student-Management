# MongoDB CRUD Student Management System

A student management web application developed using Python, Flask and MongoDB Atlas.

## Project Overview

This project demonstrates how a Flask application can interact with a MongoDB database to manage student records using CRUD operations.

## Features

- **Create:** Add new students with their name, course and age.
- **Read:** Display all student records stored in MongoDB.
- **Update:** Edit existing student information.
- **Delete:** Remove student records from the database.

## Technologies Used

- Python
- Flask
- MongoDB Atlas
- PyMongo
- HTML
- Git and GitHub

## How It Works

The Flask application connects to MongoDB Atlas using a connection string stored in a local `.env` file.

Users can add, view, edit and delete student records through web forms.

## Running the Application

1. Clone the repository.
2. Install the required packages:

   `pip install flask pymongo python-dotenv`

3. Create a `.env` file containing your own `MONGO_URI`.
4. Run the application:

   `python app.py`

5. Open `http://127.0.0.1:5000/students` in your browser.

## Author

**Favour Oka**

2610336

MSc Data Science and Artificial Intelligence

Leeds Trinity University
