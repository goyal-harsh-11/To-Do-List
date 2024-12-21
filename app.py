from flask import Flask, render_template, request, redirect
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app=Flask(__name__)

db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'port': os.getenv('DB_PORT'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
}

@app.route('/')
def index():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM todo_list")
    todo_list = cursor.fetchall()
    conn.close()
    return render_template('index.html', todo_list=todo_list)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form['task']
    if task:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO todo_list (task) VALUES (%s)", (task,))
        conn.commit()
        conn.close()
    return redirect('/')

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("UPDATE todo_list SET completed = TRUE WHERE ID = %s", (task_id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todo_list WHERE ID = %s", (task_id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True,port=8080)