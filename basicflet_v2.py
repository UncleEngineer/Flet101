import flet as ft
import csv
import os

# รายชื่อนักเรียน 10 คน
students = [
    "อนันต์", "เบญจา", "ชลิต", "ดารา", "ธนา",
    "นภา", "ปกรณ์", "พิมพ์", "มนัส", "รัตน์"
]

# ชื่อไฟล์ CSV
csv_filename = "attendance.csv"

def main(page: ft.Page):
    page.title = "ระบบเช็คชื่อ"
    page.theme_mode = ft.ThemeMode.LIGHT

    # Dropdown สำหรับเลือกชื่อนักเรียน
    selected_student = ft.Dropdown(
        label="เลือกชื่อนักเรียน",
        options=[ft.dropdown.Option(name) for name in students],
        width=300
    )

    # Radio buttons สำหรับเลือกสถานะ
    status_group = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="มา", label="มา"),
            ft.Radio(value="ไม่มา", label="ไม่มา")
        ])
    )

    # แสดงข้อความผลลัพธ์
    result_text = ft.Text("")

    # ฟังก์ชันปิดกล่อง dialog
    def close_dialog(e):
        page.dialog.open = False
        page.update()

    # ปุ่ม: แสดงข้อมูลที่บันทึกไว้
    def show_data(e):
        if not os.path.exists(csv_filename):
            result_text.value = "ยังไม่มีข้อมูลที่บันทึกไว้"
            page.update()
            return

        with open(csv_filename, mode="r", encoding="utf-8") as file:
            rows = list(csv.reader(file))
            data_view = "\n".join([f"{r[0]}: {r[1]}" for r in rows])

        page.dialog = ft.AlertDialog(
            title=ft.Text("ข้อมูลที่บันทึกไว้"),
            content=ft.Text(data_view or "ไม่มีข้อมูล"),
            actions=[ft.TextButton("ปิด", on_click=close_dialog)],
            open=True
        )
        page.update()

    # ปุ่ม: บันทึกข้อมูล
    def save_data(e):
        if not selected_student.value or not status_group.value:
            result_text.value = "กรุณาเลือกชื่อนักเรียนและสถานะ"
            page.update()
            return

        with open(csv_filename, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([selected_student.value, status_group.value])
            result_text.value = f"✅ บันทึกข้อมูลเรียบร้อย: {selected_student.value} - {status_group.value}"
            page.update()

    # ปุ่มต่าง ๆ
    save_button = ft.ElevatedButton("บันทึก", on_click=save_data)
    show_button = ft.OutlinedButton("ดูข้อมูล", on_click=show_data)

    # เพิ่มทั้งหมดลงในหน้า
    page.add(
        selected_student,
        status_group,
        ft.Row([save_button, show_button]),
        result_text
    )

# เรียกใช้ Flet app
ft.app(target=main)
