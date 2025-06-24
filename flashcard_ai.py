from flet import *
import csv

def writecsv(data):
    with open('flashcard.csv','a',newline='',encoding='utf-8') as file:
        fw = csv.writer(file)
        fw.writerow(data)

def readcsv():
    with open('flashcard.csv',newline='',encoding='utf-8') as file:
        fr = csv.reader(file)
        return list(fr)

def main(page: Page):
    page.title = "Flashcard App"
    page.bgcolor = Colors.BLUE_GREY_50
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    page.vertical_alignment = MainAxisAlignment.CENTER

    global current
    current = 0

    output = Text(size=30, weight=FontWeight.BOLD, color=Colors.BLUE_900)
    vocab = TextField(label='คำศัพท์ใหม่', width=300)
    trans = TextField(label='คำแปล', width=300)

    def update_page():
        data = readcsv()
        if data:
            current_vocab = data[-1]
            output.value = f"{current_vocab[0]} = {current_vocab[1]}"
        else:
            output.value = "ยังไม่มีคำศัพท์"
        page.update()

    def savevocab(e):
        data = readcsv()
        vocablist = [d[0] for d in data]
        if vocab.value not in vocablist and vocab.value.strip() != "":
            writecsv([vocab.value, trans.value])
            vocab.value = ''
            trans.value = ''
            update_page()
        else:
            output.value = "⚠️ มีคำศัพท์นี้อยู่แล้ว หรือข้อมูลไม่ครบ"
            page.update()

    def next(e):
        global current
        data = readcsv()
        if current + 1 < len(data):
            current += 1
            output.value = f"{data[current][0]} = {data[current][1]}"
            page.update()

    def prev(e):
        global current
        data = readcsv()
        if current > 0:
            current -= 1
            output.value = f"{data[current][0]} = {data[current][1]}"
            page.update()

    # UI Layout
    page.appbar = AppBar(
        title=Text("📘 Flashcard App", style=TextStyle(size=20, weight=FontWeight.BOLD)),
        bgcolor=Colors.BLUE_400,
        center_title=True,
    )

    button = ElevatedButton("💾 บันทึกคำศัพท์", on_click=savevocab, color=Colors.WHITE, bgcolor=Colors.GREEN)
    b_next = ElevatedButton("➡️ ถัดไป", on_click=next, color=Colors.WHITE, bgcolor=Colors.BLUE)
    b_prev = ElevatedButton("⬅️ ก่อนหน้า", on_click=prev, color=Colors.WHITE, bgcolor=Colors.ORANGE)

    layout = Column(
        [
            Container(
                Column([
                    output,
                    vocab,
                    trans,
                    Row([button], alignment=MainAxisAlignment.CENTER),
                    Row([b_prev, b_next], alignment=MainAxisAlignment.SPACE_EVENLY),
                ],
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER),
                padding=20,
                bgcolor=Colors.WHITE,
                border_radius=10,
                width=400,
                shadow=BoxShadow(blur_radius=10, color=Colors.BLACK12),
            )
        ],
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
    )

    update_page()
    page.add(layout)

app(target=main)
