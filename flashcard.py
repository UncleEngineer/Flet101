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

def updatecsvfile(data):
    with open('flashcard.csv','w',newline='',encoding='utf-8') as file:
        fw = csv.writer(file) # fw = file writer
        fw.writerows(data) # data = ['cat','แมว']



def main(page: Page):
    
    raw_data = readcsv()
    print(raw_data)
    
    raw_datadict = {}
    for v,t in raw_data:
        raw_datadict[v] = [v,t]

    page.horizontal_alignment = CrossAxisAlignment.CENTER
    page.vertical_alignment = MainAxisAlignment.CENTER

    global current
    text = Text('Flashcard')
    output = Text(size=30)
    vocab = TextField(label='คำศัพท์ใหม่',width=200)
    trans = TextField(label='คำแปล',width=200)

    current = 0
    
    global edit_state
    edit_state = 'edit' # edit / save_edit

    global vocab_text
    global trans_text
    vocab_text = ''
    trans_text = ''

    def update_page():
        global vocab_text
        global trans_text
        data = readcsv()
        current_vocab = data[-1]
        output.value = current_vocab[0] +' = ' + current_vocab[1]
        vocab_text = current_vocab[0]
        trans_text = current_vocab[1]
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
    
    def edit(e):
        global edit_state
        
        if edit_state == 'edit':
            # EDIT - SAVE
            button_edit.icon = Icons.SAVE
            edit_state = 'save_edit'
            print(vocab_text)
            print(trans_text)
            vocab.value = vocab_text
            trans.value = trans_text
        else:
            # SAVE - EDIT
            button_edit.icon = Icons.EDIT
            edit_state = 'edit'
            raw_datadict[vocab_text] = [vocab.value,trans.value]
            datareplace = list(raw_datadict.values())
            vocab.value = ''
            trans.value = ''
            updatecsvfile(datareplace)
            update_page()
            
                        
        page.update()
    
    button_edit = IconButton(icon=Icons.EDIT, on_click=edit)
    
    def delete(e):
        del raw_datadict[vocab_text]
        datareplace = list(raw_datadict.values())
        vocab.value = ''
        trans.value = ''
        updatecsvfile(datareplace)
        update_page()
        
    
    button_delete = IconButton(icon=Icons.DELETE, on_click=delete)

    def next(e):
        try:
            global current
            data = readcsv()
            output.value = data[current+1][0] + '=' + data[current+1][1]
            global vocab_text
            global trans_text
            vocab_text = data[current+1][0]
            trans_text = data[current+1][1]
            current = current + 1
            # clear state edit
            button_edit.icon = Icons.EDIT
            edit_state = 'edit'
            vocab.value = ''
            trans.value = ''
            page.update()
        except:
            pass

    b_next = ElevatedButton('next',on_click=next)

    def prev(e):
        # EP หน้ามาดูวิธีแก้เรื่อง index
        try:
            global current
            data = readcsv()
            output.value = data[current-1][0] + '=' + data[current-1][1]
            global vocab_text
            global trans_text
            vocab_text = data[current-1][0]
            trans_text = data[current-1][1]
            current = current -1
            # clear state edit
            button_edit.icon = Icons.EDIT
            edit_state = 'edit'
            vocab.value = ''
            trans.value = ''
            page.update()
        except:
            pass

    b_prev = ElevatedButton('prev',on_click=prev)

    rows = [text,
            vocab,
            trans,
            Row([button, button_edit,button_delete],alignment=MainAxisAlignment.CENTER),
            Row([b_next,b_prev],alignment=MainAxisAlignment.CENTER),
            output]
    
    update_page()
    page.add(Column(rows,horizontal_alignment=CrossAxisAlignment.CENTER,alignment=MainAxisAlignment.CENTER))


app(target=main)