from flet import *
import csv
from datetime import datetime

def writecsv(text):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # strftime.org
    with open('data.csv','a',newline='',encoding='utf-8') as file:
        fw = csv.writer(file)
        fw.writerow([ts,text])

def main(page: Page):
    print('this is a main function')
    text = Text('My Friend')
    output = Text(size=30)
    friend = TextField(label='enter your friend')
    
    def showtext(e):
        output.value = 'สวัสดี'+friend.value
        writecsv(friend.value)
        friend.value = ''
        page.update()
        
    
    button = ElevatedButton('Hi!',on_click=showtext)

    page.add(text,friend,button,output)


app(target=main)