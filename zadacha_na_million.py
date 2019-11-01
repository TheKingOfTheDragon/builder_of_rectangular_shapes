from tkinter import *
import os

os.system("mode con cols=105 lines=30")

""" ФУНКЦИЯ РЕАЛИЗУЮЩАЯ АЛГОРИТМ ЕВКЛИДА ДЛЯ НАХОЖДЕНИЯ ОБЩЕГО КРАТНОГО """
def NOK(a,b): 
    m = a*b
    while (a != 0) and (b != 0):
        if (a > b):
            a = a % b
        else:
            b = b % a
    return m // (a+b)
    
""" ФУНКЦИЯ ВЫВОДЯЩАЯ НА ЭКРАН МЕГА БЛОК"""
# x0,y0 - координаты левого верхнего угла мегаблока
# NA - количество блоков по горизонтали
# NB - количество блоков по вертикали
# A - длина блока в пикселях по горизонтали 
# B - длина блока в пикселях по горизонтали
# block_text - надпись в блоке    
def PrintMegaBlock(x0, y0, NA, NB, A, B, block_text):
    for i in range (NA):
        for j in range (NB):
            x1 = x0 + i*A + 4
            x2 = x1 + A
            y1 = y0 + j*B + 4
            y2 = y1 + B
            canvas.create_rectangle(x1, y1, x2, y2, fill = 'azure2', outline = 'black', width=2)
            canvas.create_text(0.5*x1 + 0.5*x2, 0.5*y1 + 0.5*y2, text = block_text, font = 'Verdana 12', fill='black')

""" ВВОД ДАННЫХ """
print (" Данная рограмма выводит прямоугольник из прямоугольных фигурок, располагая их в таком порядке, что в")
print (" центре находится фигурка под максимальным номером, окруженная фигурками под предыдущим номером, а те")
print (" в свою очередь, фигурками под предпредыдущим номером и т.д.")
print ("\n Автор программы: Юрий Землянский (также известный как Юрий Штейн)")
M = [] # создаем пустой список
print ("\n Введите количество фигурок:")
N = int(input(" N = "))
print (" Введите размеры сторон i-й фигурки ai и bi в пикселях через пробел")
for i in range(N): # массив считывающий размеры сторон фигурок от 0 до N (не включая N)
    print(" Введите a{0} и b{0}:".format(i+1)) # формат подставляет в {индекс} то что в скобках (идекс = порядок через запятую)
    print(end = ' ')
    row = input().split() #ввод чисел разделенных пробелом с записью в вектор
    for j in range(2): # массив от 0 до 1 (включительно)
        row[j] = int(row[j])
    M.append(row) # кладет вектор в конец списка

""" ОПРЕДЕЛЕНИЕ НОК ДЛЯ ВСЕХ МЕНЬШИХ И БОЛЬШИХ СТОРОН """ 
NOK_a = NOK(M[0][0], M[1][0]) # определяем начальный НОК для a
NOK_b = NOK(M[0][1], M[1][1]) # определяем начальный НОК для b
for i in range(2,N):
    NOK_a = NOK(NOK_a, M[i][0])
    NOK_b = NOK(NOK_b, M[i][1])
print ("\n Расчитан общий мега блок со сторонами: ", NOK_a, " и ", NOK_b)

""" ОПРЕДЕЛЕНИЕ НАЧАЛ КООРДИНАТ С УСТАНОВКОЙ СООТВЕТСТВИЯ НОМЕРУ ФИГУРКИ"""
# d1 [k][j][x0, y0, i]
d1 = []
for k in range(2*N-1):
    d2 = []
    for j in range(2*N-1):
        d3 = [int(NOK_a*k), int(NOK_b*j), min(k, j, 2*N-2-k, 2*N-2-j)]
        d2.append(d3)
    d1.append(d2)

""" ОПРЕДЕЛЕНИЕ ПАРАМЕТРОВ МЕГА БЛОКА """
# c1[i][NA, NB, A, B, block_text]
c1 = []    
for i in range(N):
    c2 = [int(NOK_a/M[i][0]), int(NOK_b/M[i][1]), M[i][0], M[i][1], str(i+1)]
    c1.append(c2)
print (" Для построения мегаблока необходимо:") 
for i in range(N):
    print (" Фигурок под номером {0}: {1}x{2} шт".format(i+1, c1[i][0], c1[i][1]))  

""" ГРАФИЧЕСКОЕ ОКНО И ХОЛСТ С ПОЛОСОЙ ПРОКРУТКИ"""
win = Tk() # TK - конструктор для графического окна, присваеваем созданное окно переменной "win"
win.configure(background="#FFFFFF") # цвет фона окна
win.title("РЕЗУЛЬТАТ РАБОТЫ ПРОГРАММЫ") # шапка
WS = win.winfo_screenwidth() # возвращает ширину экрана
HS = win.winfo_screenheight() # возвращает высоту экрана
WW = NOK_a*(2*N-1) + 2; # ширина холста c поправкой на контур
WH = NOK_b*(2*N-1) + 2; # высота холста с поправкой на контур
if (WW < WS) or (WH < HS): 
    if (WW < 380):
        WS = 390
    else:
        WS = WW + 28
    if (WH < 150):
        HS = 160
    else:    
        HS = WH + 28
else:    
    win.attributes("-fullscreen", True)
    WH = WH + 8
win.resizable(width = False, height = False) # запрещает изменять размер окна

frame=Frame(win, width=WS, height=HS)
frame.grid(row=0,column=0)
canvas=Canvas(frame,bg='#FFFFFF',width=WW,height=WH,scrollregion=(0,0,WW,WH))
hbar=Scrollbar(frame,orient=HORIZONTAL)
hbar.pack(side=BOTTOM,fill=X)
hbar.config(command=canvas.xview)
vbar=Scrollbar(frame,orient=VERTICAL)
vbar.pack(side=RIGHT,fill=Y)
vbar.config(command=canvas.yview)
canvas.config(width=WS-22,height=HS-22)
canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
canvas.pack(side=LEFT, expand=True,fill=BOTH)

for i in range(2*N-1):
    for j in range(2*N-1):
        g = int (d1[i][j][2])
        PrintMegaBlock(d1[i][j][0], d1[i][j][1], c1[g][0], c1[g][1], c1[g][2], c1[g][3], c1[g][4])
        
print ("\n Задача выполнена!")
input(" ")        

win.mainloop()  

