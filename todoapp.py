import flet as ft
import sqlite3

# ---------- DATABASE SETUP ----------
conn = sqlite3.connect("todolist.sqlite3", check_same_thread=False)
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS tasklist (
          ID INTEGER PRIMARY KEY AUTOINCREMENT,
          title TEXT,
          status TEXT,
          note TEXT )""")


def insert_tasklist(title, status, note):
    with conn:
        command = "INSERT INTO tasklist VALUES (?,?,?,?)"
        c.execute(command, (None, title, status, note))
        conn.commit()


def view_tasklist():
    with conn:
        c.execute("SELECT * FROM tasklist")
        return c.fetchall()


def update_tasklist(ID, field, newvalue):
    with conn:
        c.execute(f"UPDATE tasklist SET {field} = (?) WHERE ID = (?)", (newvalue, ID))
        conn.commit()


def delete_tasklist(ID):
    with conn:
        c.execute("DELETE FROM tasklist WHERE ID = (?)", ([ID]))
        conn.commit()

# ---------- FLET UI ----------
def main(page: ft.Page):
    page.title = "Todolist App"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO

    # Center the content and apply SafeArea
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    task_column = ft.Column(expand=True, spacing=10, scroll=ft.ScrollMode.AUTO)

    title_input = ft.TextField(label="ชื่อรายการ", width=300)
    note_input = ft.TextField(label="หมายเหตุ", width=300)

    def load_tasks():
        task_column.controls.clear()
        for task in view_tasklist():
            task_id, title, status, note = task
            is_done = status == "done"

            checkbox = ft.Checkbox(label=title, value=is_done, expand=True)
            note_display = ft.Text(note, italic=True, size=12)

            def toggle_status(e, id=task_id):
                new_status = "done" if e.control.value else "pending"
                update_tasklist(id, "status", new_status)
                load_tasks()
                page.update()

            checkbox.on_change = toggle_status

            def delete_task(e, id=task_id):
                delete_tasklist(id)
                load_tasks()
                page.update()

            def edit_task(e, id=task_id, current_title=title, current_note=note):
                title_input.value = current_title
                note_input.value = current_note

                def save_edit(e):
                    update_tasklist(id, "title", title_input.value)
                    update_tasklist(id, "note", note_input.value)
                    title_input.value = ""
                    note_input.value = ""
                    save_button.text = "เพิ่มรายการ"
                    save_button.on_click = add_task
                    load_tasks()
                    page.update()

                save_button.text = "บันทึกการแก้ไข"
                save_button.on_click = save_edit
                page.update()

            row = ft.Row(
                [
                    checkbox,
                    ft.IconButton(icon=ft.Icons.EDIT, on_click=edit_task),
                    ft.IconButton(icon=ft.Icons.DELETE, on_click=delete_task),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )
            task_column.controls.append(row)

        page.update()

    def add_task(e):
        if title_input.value.strip() == "":
            return
        insert_tasklist(title_input.value, "pending", note_input.value)
        title_input.value = ""
        note_input.value = ""
        load_tasks()
        page.update()

    save_button = ft.ElevatedButton(text="เพิ่มรายการ", on_click=add_task)

    page.add(
        ft.SafeArea(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text("📋 To-Do List", size=30, weight=ft.FontWeight.BOLD),
                        title_input,
                        note_input,
                        save_button,
                        ft.Divider(),
                        ft.Container(task_column, height=400, expand=True, padding=10),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.center,
                padding=20,
                width=400,
            )
        )
    )

    load_tasks()

ft.app(target=main)
