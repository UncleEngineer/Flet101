# basic_crud.py
# C-Create, R-Read, U-Update, D-Delete
import csv

# C-Create
# กรอกข้อมูลลงในช่องกรอก > เมื่อกดปุ่มบันทึก > ข้อมูลจะถูกบันทึกลง CSV

def writecsv(data):
    with open('flashcard.csv','a',newline='',encoding='utf-8') as file:
        fw = csv.writer(file) # fw = file writer
        fw.writerow(data) # data = ['cat','แมว']


# myvocab = ['cat','แมว']
# writecsv(myvocab)

# R-Read
# โปรแกรมสามารถอ่านไฟล์ CSV ได้ แล้วมาโชว่์ในหน้าโปรแกรมหลัก

def readcsv():
    with open('flashcard.csv',newline='',encoding='utf-8') as file:
        fr = csv.reader(file) # fr = file reader
        data = list(fr)
        #print(data)
        return data

# data = readcsv()
# print(data)
# U-Update
# ต้องการแก้ไขข้อมูลบางตัว 
# อ่านไฟล์ทั้งหมดเข้ามาใส่ในตัวแปร > แก้ไขข้อมูลในตัวแปร > [['dog', 'สุนัข'], ['cat', 'แมว']] > บันทึกใหม่ทั้งหมด (replace file) 
# [Step-A]> กลับมาอ่านไฟล์ใหม่ readcsv() ข้อมูลจะถูกอัพเดทเป็นตัวที่แก้ไข > นำไปโชว์ในโปรแกรม
def updatecsv(eng,newvalue,edit='thai'):
    
    vocab = []
    data = readcsv()
    for d in data:
        vocab.append(d[0])
    
    editindex = vocab.index(eng)
    
    if edit == 'thai':
        data[editindex][1] = newvalue
    elif edit == 'eng':
        data[editindex][0] = newvalue
    else:
        pass


    with open('flashcard.csv','w',newline='',encoding='utf-8') as file:
        fw = csv.writer(file) # fw = file writer ('w' is replace)
        fw.writerows(data)

# updatecsv('cat','แมว')
# D-Delete 
# ต้องการลบข้อมูล
# อ่านไฟล์ทั้งหมดเข้ามาใส่ในตัวแปร > ลบข้อมูลตัวที่ต้องการออก > บันทึกใหม่ทั้งหมด (replace file) > Step-A

def deletecsv(eng):
    
    vocab = []
    data = readcsv()
    for d in data:
        vocab.append(d[0])
    
    delete_index = vocab.index(eng)
    del data[delete_index]

    with open('flashcard.csv','w',newline='',encoding='utf-8') as file:
        fw = csv.writer(file) # fw = file writer ('w' is replace)
        fw.writerows(data)