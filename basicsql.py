import sqlite3

conn = sqlite3.connect('todolist.sqlite3')
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS tasklist (
          ID INTEGER PRIMARY KEY AUTOINCREMENT,
          title TEXT,
          status TEXT,
          note TEXT )""")

def insert_tasklist(title,status,note):
    with conn:
        command = 'INSERT INTO tasklist VALUES (?,?,?,?)'
        c.execute(command,(None,title,status,note))
        conn.commit()
        print('saved')

def view_tasklist():
    with conn:
        command = 'SELECT * FROM tasklist'
        c.execute(command)
        result = c.fetchall()
        print(result)
    return result

def update_tasklist(ID,field,newvalue):
    with conn:
        command = 'UPDATE tasklist SET {} = (?) WHERE ID = (?)'.format(field)
        c.execute(command,(newvalue,ID))
        conn.commit()
        print('updated')


def delete_tasklist(ID):
    with conn:
        command = 'DELETE FROM tasklist WHERE ID = (?)'
        c.execute(command,([ID]))
        conn.commit()


# delete_tasklist(7)
# update_tasklist(2,'status','pending')
# insert_tasklist('ทานข้าวกับครอบครัว','waiting','KFC')
# view_tasklist()