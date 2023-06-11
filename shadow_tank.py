import tkinter as tk
from tkinter import filedialog
import ttkbootstrap
import cv2
import os

try:
    os.mkdir("tmp")
    print("Successfully Created Direction 'tmp'!")
except FileExistsError:
    print("Successfully Created Direction 'tmp'!")

style = ttkbootstrap.Style(theme="darkly")    #利用ttkbootstrap快捷部署gui主题
win = style.master

def xc_max_than_yc(xc, yc, color_ratio=0.5):
    threshold = 255 * color_ratio
    xc = (xc / 255) * (255 - threshold) + threshold
    yc = (yc / 255) * threshold
    return xc, yc 

def create_tank(white, black):
    za = black - white + 255
    zc = black.copy()
    idx = black != 0
    zc[idx] = black[idx] * 255 / za[idx]
    img = cv2.merge((zc, zc, zc, za))
    return img

def selectfile(txt: tk.Entry, lab: tk.Label):
    status.configure(text="")     #清空status，便于多次生成图片
    filepath = filedialog.askopenfilename()   #请求寻找一个图片文件,返回路径字符串
    txt.delete(0, 'end')
    txt.insert(0,filepath)   #将先前选择的路径填入对应地址栏
    
    tmp = cv2.imread(filepath, 0)    #将选中图片resize成(120,120)来展示缩略图
    tmp = cv2.resize(tmp, (120, 120))
    cv2.imwrite("tmp/tmp.png", tmp)
    panel = tk.Label(master=win)    #新建一个Label类panel引用photo，防止函数执行结束时释放内存导致photo丢失。
    panel.photo = tk.PhotoImage(file="tmp/tmp.png")
    lab.configure(image=panel.photo)

def generate():
    Img_1 = Txt1.get()
    Img_2 = Txt2.get()
    img_false = cv2.imread(Img_1, 0)     #掩体
    img_true = cv2.imread(Img_2, 0)     #底图
    x, y = img_true.shape
    img_false = cv2.resize(img_false, (y, x))
    xc, yc = xc_max_than_yc(img_false, img_true)
    Img_output = create_tank(xc, yc)
    
    tmp = cv2.resize(Img_output, (120,120))   #生成成品缩略图
    cv2.imwrite("tmp/Img_output.png", tmp)

    cv2.imwrite("Img_output.png", Img_output) 

    panel_ = tk.Label(master=win)
    panel_.photo = tk.PhotoImage(master=win, file="tmp/Img_output.png")
    Img_output_L.configure(image=panel_.photo)
    status.configure(text="成功生成！图片已保存至当前目录。")

# win = tk.Tk()
win.title("幻影坦克生成器")
win.geometry('600x500')

# Labels
title = tk.Label(master=win, text="幻影坦克生成器", anchor='center', font=('楷体',16))
title.place(x=220, y=0, width=165, height=40)
status = tk.Label(master=win,text="",anchor='center', font=("楷体",16))
status.place(x=100,y=390,width=400,height=30)
Img1_L = tk.Label(master=win, text="图片1",anchor='center')
Img1_L.place(x=0, y=60, width=120, height=120)
Img2_L = tk.Label(master=win, text="图片2",anchor="center")
Img2_L.place(x=0,y=260,width=120,height=120)
Img_output_L =tk.Label(master=win, text="输出图片",anchor="center")
Img_output_L.place(x=470, y=160, width=120, height=120)
Address_1 = tk.Label(master=win,text="图片1地址",anchor='center', font=("楷体",12))
Address_1.place(x=190, y=90, width=80, height=30)
Address_2 = tk.Label(master=win, text="图片2地址",anchor='center', font=("楷体",12))
Address_2.place(x=190, y=290, width=80, height=30)

# Entrys
Txt1 = tk.Entry(master=win)
Txt1.place(x=140, y=60, width=180, height=30)
Txt2 = tk.Entry(master=win)
Txt2.place(x=140, y=260, width=180, height=30)

# Buttons
Cmd1 = tk.Button(master=win, text="导入上层掩体图", font=("楷体",10), command=lambda :selectfile(Txt1, Img1_L))
Cmd1.place(x=180, y=130, width=100, height=40)
Cmd2 = tk.Button(master=win, text="导入下层真实图", font=("楷体",10), command=lambda : selectfile(Txt2, Img2_L))
Cmd2.place(x=180, y=330, width=100, height=40)
Cmd3 = tk.Button(master=win, text="生成并保存图片", font=("楷体",10), command=lambda : generate())
Cmd3.place(x=340, y=190, width=120, height=40)

win.mainloop()
