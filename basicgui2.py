from flet import *
import csv
from datetime import datetime

def writecsv(text):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # strftime.org
    with open('data.csv', 'a', newline='', encoding='utf-8') as file:
        fw = csv.writer(file)
        fw.writerow([ts, text])

def readcsv():
    # ฟังก์ชันสำหรับอ่านไฟล์ CSV
    with open('data.csv', 'r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        data = "\n".join([f"เวลา: {row[0]}, ชื่อ: {row[1]}" for row in csv_reader])  # แสดงในรูปแบบที่เข้าใจง่าย
    return data

def main(page: Page):
    print('this is a main function')
    text = Text('My Friend')
    output = Text(size=30)
    friend = TextField(label='Enter your friend')
    
    def showtext(e):
        output.value = 'สวัสดี ' + friend.value
        writecsv(friend.value)
        friend.value = ''
        page.update()

    def read_data(e):
        data = readcsv()  # เรียกฟังก์ชันอ่านข้อมูล
        output.value = data  # แสดงข้อมูลใน output
        page.update()

    button_greet = ElevatedButton('Hi!', on_click=showtext)
    button_read = ElevatedButton('อ่านข้อมูล', on_click=read_data)  # ปุ่มอ่านข้อมูล

    page.add(text, friend, button_greet, button_read, output)

app(target=main)
