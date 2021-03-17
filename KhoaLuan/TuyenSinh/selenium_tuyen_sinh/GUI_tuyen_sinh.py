# -*- coding: utf-8 -*-
from tkinter import *
from tkinter.ttk import Frame, Button, Style
import similar
from tkinter import Tk, Frame, BOTH

def search():
    global query
    query = questionText.get()
    print(query)
    kq = similar.format_output(query)
    outputLb.delete('1.0', END)
    if kq == 0:
        outputLb.insert(END, "Không có kết quả phù hợp\n")

    elif len(kq) <= 2:
        for j in range(len(kq)):
            if j == 0:
                outputLb.insert(END, 'Tiền sử lý câu truy vấn:\n')
                outputLb.insert(END, kq[j])


            else:
                outputLb.insert(END, kq[j])
                outputLb.insert(END, '\n')
    else:
        for i in range(len(kq)):
            for j in range(len(kq[i])):
                if j == 1:
                    outputLb.insert(END, kq[i][j])
                    outputLb.insert(END, '\n')
                    outputLb.insert(END, '==============================\n')
                else:
                    outputLb.insert(END, kq[i][j][1])
                    outputLb.insert(END, '\n')
                    outputLb.insert(END, '==============================\n')



root = Tk()
root.geometry("750x500+300+100")
root.config(background="#63DDBF")
root.title("Hệ thống tư vấn tuyển sinh tự động")


questionLab = Label(root, text='Hệ thống tư vấn tuyển sinh tự động\n', font=('Arial', 15, 'bold', 'italic'), background="#63DDBF")
questionLab.grid(row=0, column=8, columnspan=9)

questionText = StringVar()
el = Entry(root, textvariable=questionText, width=50)
el.grid(row=1, column=6, columnspan=12)


quitButton = Button(root, text="TRẢ LỜI", width=12, command=search)

quitButton.grid(row=3, column=11)

outputLb = Text(root, height=18)
outputLb.grid(column=1, columnspan=22, row=4, rowspan=6,  sticky='W')

scrollbar = Scrollbar(root, orient=VERTICAL)
outputLb.config(yscrollcommand=scrollbar.set, font=('Arial', 13))
scrollbar.config(command=outputLb.yview)

scrollbar.grid(row=4, column=23, rowspan=6,  sticky='W')

outputLb.insert(END, "")

root.mainloop()