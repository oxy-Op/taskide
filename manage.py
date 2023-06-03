import sqlite3

conn = sqlite3.connect('database.db')
conn.execute('''CREATE TABLE IF NOT EXISTS lists (
                id INTEGER PRIMARY KEY,
                list_name TEXT
            )''')

conn.execute('''CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER,
                list_id INTEGER,
                task_name TEXT,
                FOREIGN KEY (list_id) REFERENCES lists (id)
            )''')
conn.commit()


def add_list(id, name):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute(
        '''INSERT into lists (id, list_name) VALUES (?,?)''', (str(id), str(name)))
    conn.commit()
    conn.close()


def add_task(list_id, task_id, task_name):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO tasks (id, list_id, task_name) VALUES (?, ?, ?)',
                 (str(task_id), str(list_id), str(task_name)))
    conn.commit()
    conn.close()
    

def update_list(id, name):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    try:
        c.execute('UPDATE lists SET list_name = ? WHERE id = ?', (name, id))
        conn.commit()
        conn.close()
    except Exception as e:
        return e
    finally:
        conn.close()


def update_task(list_id, task_id, task_name):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    try:
        c.execute('''UPDATE tasks SET task_name = ? WHERE id = ? AND list_id = ?''',
                    (task_name, task_id, list_id))
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
    finally:
        conn.close()

def delete_task(list_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    try:
        c.execute("DELETE FROM tasks WHERE list_id = ?", (str(list_id)))
        conn.commit()
        conn.close()
    except Exception as e:
        return e
    finally:
        conn.close()


def get_list(id=None):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    if id is None:
        lists_ = c.execute('''SELECT id, list_name FROM lists''')
        lists = {}
        for i in lists_:
            lists[i[0]] = {'list': i[1], 'tasks': {}}
        conn.close()
        return lists
    else:
        lists_ = c.execute(
            '''SELECT list_name FROM lists WHERE id = ?''', (str(id)))
        lists = {}
        for i in lists_:
            lists[id] = {'list': i[0], 'tasks': {}}
        conn.close()
        return lists[id]
        


def get_task(list_id, task_id=None):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    if list_id and task_id is None:
        tasks = c.execute(
            '''SELECT task_name, id FROM tasks WHERE list_id = ?''', (str(list_id)))
        for i in tasks.fetchall():
            return {'tasks': {
                i[1]: i[0]
            }}
    elif list_id and task_id is not None:
        tasks = c.execute(
            '''SELECT task_name FROM tasks WHERE list_id = ? AND id = ?''', (str(list_id), str(task_id)))
        for i in tasks:
            return {'task': i[0]}
        conn.close()



def update_value():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''SELECT lists.id, lists.list_name, tasks.id, tasks.task_name, tasks.list_id
             FROM lists
             LEFT JOIN tasks ON lists.id = tasks.list_id''')

    data = c.fetchall()
    lists = {}
    for row in data:
        list_id = row[0]
        list_name = row[1]
        task_id = row[2]
        task_name = row[3]
        task_list_id = row[4]

        if list_id not in lists:
            if list_name is not None:
                lists[list_id] = {"list": list_name, "tasks": {}}
            else:
                lists[list_id] = {}

        if list_name and task_id is not None and task_name is not None:
            lists[list_id].setdefault("tasks", {}).setdefault(task_id, {"task": task_name})
        elif list_name and task_id is not None:
            lists[list_id].setdefault("tasks", {}).setdefault(task_id, {})

    conn.close()
    return lists



def get_lists_table_length():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''SELECT COUNT(*) FROM lists''')
    result = c.fetchone()
    length = result[0] if result else 0

    conn.close()
    return length

