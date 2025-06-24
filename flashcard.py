from flet import *
import csv

def writecsv(data):
    with open('flashcard.csv','a',newline='',encoding='utf-8') as file:
        fw = csv.writer(file) # fw = file writer
        fw.writerow(data) # data = ['cat','แมว']

def readcsv():
    with open('flashcard.csv',newline='',encoding='utf-8') as file:
        fr = csv.reader(file) # fr = file reader
        data = list(fr)
        #print(data)
        return data


def main(page: Page):
    global current
    text = Text('Flashcard')
    output = Text(size=30)
    vocab = TextField(label='คำศัพท์ใหม่')
    trans = TextField(label='คำแปล')

    current = 0

    def update_page():
        data = readcsv()
        current_vocab = data[-1]
        output.value = current_vocab[0] +' = ' + current_vocab[1]
        page.update()

    
    def savevocab(e):
        data = readcsv()
        vocablist = []
        for d in data:
            vocablist.append(d[0])
        if vocab.value not in vocablist:
            data = [vocab.value, trans.value]
            writecsv(data)
            vocab.value = ''
            trans.value = ''
            update_page()
        else:
            print('มีคำศัพท์นี้อยู่แล้ว')

        
       
    
    button = ElevatedButton('save',on_click=savevocab)

    def next(e):
        try:
            global current
            data = readcsv()
            output.value = data[current+1][0] + '=' + data[current+1][1]
            current = current + 1
            page.update()
        except:
            pass

    b_next = ElevatedButton('next',on_click=next)

    def prev(e):
        # EP หน้ามาดูวิธีแก้เรื่อง index
        try:
            global current
            data = readcsv()
            output.value = data[current+1][0] + '=' + data[current+1][1]
            current = current -1
            page.update()
        except:
            pass

    b_prev = ElevatedButton('prev',on_click=prev)

    update_page()
    page.add(text,vocab,trans,button,b_next,b_prev,output)


app(target=main)