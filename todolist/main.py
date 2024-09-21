import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import *
import sqlite3

def init_db():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL,
            date_from TEXT,
            date_to TEXT
        )
    ''')
    conn.commit()
    conn.close()


def get_tasks(status_filter=None):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    if status_filter:
        cursor.execute('SELECT * FROM tasks WHERE status = ?', (status_filter,))
    else:
        cursor.execute('SELECT * FROM tasks')

    tasks = cursor.fetchall()
    conn.close()
    return tasks

def add_task(title, description, status, date_from=None, date_to=None):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (title, description, status, date_from, date_to) VALUES (?, ?, ?, ?, ?)',
                   (title, description, status, date_from, date_to))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
def update_task(task_id, title, description, status):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE tasks
    SET title = ?, description = ?, status = ?
    WHERE id = ?
    ''', (title, description, status, task_id))
    conn.commit()
    conn.close()



def on_edit_task():
    selected_item = tree.selection()
    if selected_item:
        task_id = tree.item(selected_item)['values'][0]
        title = tree.item(selected_item)['values'][1]
        description = tree.item(selected_item)['values'][2]
        status = tree.item(selected_item)['values'][3]
        date_from = tree.item(selected_item)['values'][4]
        date_to = tree.item(selected_item)['values'][5]

        edit_window = tk.Toplevel(root)
        edit_window.title("Редактировать задачу")

        tk.Label(edit_window, text="Название:").grid(row=0, column=0, padx=5, pady=5)
        entry_edit_title = tk.Entry(edit_window)
        entry_edit_title.grid(row=0, column=1, padx=5, pady=5)
        entry_edit_title.insert(0, title)

        tk.Label(edit_window, text="Описание:").grid(row=1, column=0, padx=5, pady=5)
        entry_edit_description = tk.Entry(edit_window)
        entry_edit_description.grid(row=1, column=1, padx=5, pady=5)
        entry_edit_description.insert(0, description)

        tk.Label(edit_window, text="Статус:").grid(row=2, column=0, padx=5, pady=5)
        combo_edit_status = ttk.Combobox(edit_window, values=["Запланирована", "В процессе", "Завершена"])
        combo_edit_status.grid(row=2, column=1, padx=5, pady=5)
        combo_edit_status.set(status)

        def save_changes():
            new_title = entry_edit_title.get()
            new_description = entry_edit_description.get()
            new_status = combo_edit_status.get()

            if new_title and new_status:

                update_task(task_id, new_title, new_description, new_status)

                update_task_list()
                edit_window.destroy()
            else:
                messagebox.showwarning("Ошибка", "Название и статус задачи обязательны для заполнения")

        tk.Button(edit_window, text="Сохранить изменения", command=save_changes).grid(row=7, column=0, columnspan=2, pady=10)

    else:
        messagebox.showwarning("Ошибка", "Выберите задачу для редактирования")
def update_task_list(filter_status=None):
    for row in tree.get_children():
        tree.delete(row)

    tasks = get_tasks(filter_status)
    for task in tasks:
        tree.insert('', 'end', values=task)

def on_add_task():
    title = entry_title.get()
    description = entry_description.get()
    status = combo_status.get()
    from_date = date_from.get() if date_from.get() else None
    to_date = date_to.get() if date_to.get() else None

    if title and status:
        add_task(title, description, status, from_date, to_date)
        update_task_list()

        entry_title.delete(0, tk.END)
        entry_description.delete(0, tk.END)
        combo_status.set("")
        date_from.set_date(datetime.date.today())
        date_to.set_date(datetime.date.today())
    else:
        messagebox.showwarning("Ошибка", "Название и статус задачи обязательны для заполнения")

def on_delete_task():
    selected_item = tree.selection()

    if selected_item:
        task_id = tree.item(selected_item)['values'][0]
        delete_task(task_id)
        update_task_list()
    else:
        messagebox.showwarning("Ошибка", "Выберите задачу для удаления")

def on_filter_tasks():
    filter_status = combo_filter.get()
    if filter_status == "Все":
        update_task_list()
    else:
        update_task_list(filter_status)

root = tk.Tk()
root.title("ToDo List с фильтрами")
root.geometry('1280x720')

frame_top = tk.Frame(root)
frame_top.pack(pady=10)

tk.Label(frame_top, text="Название:").grid(row=0, column=0, padx=5, pady=5)
entry_title = tk.Entry(frame_top)
entry_title.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_top, text="Описание:").grid(row=1, column=0, padx=5, pady=5)
entry_description = tk.Entry(frame_top)
entry_description.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_top, text="Дата от:").grid(row=3, column=0, padx=5, pady=5)
date_from = DateEntry(frame_top, width=12, background='darkblue', foreground='white', borderwidth=2)
date_from.grid(row=3, column=1, padx=5, pady=5)

tk.Label(frame_top, text="Дата до:").grid(row=4, column=0, padx=5, pady=5)
date_to = DateEntry(frame_top, width=12, background='darkblue', foreground='white', borderwidth=2)
date_to.grid(row=4, column=1, padx=5, pady=5)

tk.Label(frame_top, text="Статус:").grid(row=2, column=0, padx=5, pady=5)
combo_status = ttk.Combobox(frame_top, values=["Запланирована", "В процессе", "Завершена"], state="readonly")
combo_status.grid(row=2, column=1, padx=5, pady=5)

columns = ('ID', 'Название', 'Описание', 'Статус', 'Дата от', 'Дата до')
tree = ttk.Treeview(root, columns=columns, show='headings')
tree.heading('ID', text='Номер задачи')
tree.heading('Название', text='Название')
tree.heading('Описание', text='Описание')
tree.heading('Статус', text='Статус')
tree.heading('Дата от', text='Дата от')
tree.heading('Дата до', text='Дата до')
tree.pack(pady=10)

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

tk.Button(frame_buttons, text="Добавить задачу", command=on_add_task).grid(row=0, column=0, padx=5)

tk.Button(frame_buttons, text="Редактировать задачу", command=on_edit_task).grid(row=0, column=1, padx=5)

tk.Button(frame_buttons, text="Удалить задачу", command=on_delete_task).grid(row=0, column=2, padx=5)

frame_filter = tk.Frame(root)
frame_filter.pack(pady=10)

tk.Label(frame_filter, text="Фильтр по статусу:").grid(row=0, column=0, padx=5, pady=5)
combo_filter = ttk.Combobox(frame_filter, values=["Все", "Запланирована", "В процессе", "Завершена"], state="readonly")
combo_filter.grid(row=0, column=1, padx=5, pady=5)
combo_filter.set("Все")

tk.Button(frame_filter, text="Применить фильтр", command=on_filter_tasks).grid(row=0, column=2, padx=5, pady=5)

init_db()
update_task_list()

root.mainloop()