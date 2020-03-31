
from tkinter import *
import time
import random
import copy

gl_okno=Tk()#створення вікна
gl_okno.title('Шашки')#заголовок вінка
doska=Canvas(gl_okno, width=800,height=800,bg='#FFFFFF')
doska.pack()

n2_spisok=()#список ходів пк
ur=3#кількість перелбачуванних ходів
k_rez=0
o_rez=0
poz1_x=-1#клітка не задана
f_hi=True#визначення хода гравця

def izobrazheniya_peshek():#зображення пішок
    global peshki
    i1=PhotoImage(file="res\\1b.gif")
    i2=PhotoImage(file="res\\1bk.gif")
    i3=PhotoImage(file="res\\1h.gif")
    i4=PhotoImage(file="res\\1hk.gif")
    peshki=[0,i1,i2,i3,i4]

def novaya_igra():#початок гри
    global pole
    pole=[[0,3,0,3,0,3,0,3],
          [3,0,3,0,3,0,3,0],
          [0,3,0,3,0,3,0,3],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [1,0,1,0,1,0,1,0],
          [0,1,0,1,0,1,0,1],
          [1,0,1,0,1,0,1,0]]

def vivod(x_poz_1,y_poz_1,x_poz_2,y_poz_2):#малюємо поле
    global peshki
    global pole
    global kr_ramka,zel_ramka
    k=100
    x=0
    doska.delete('all')
    kr_ramka=doska.create_rectangle(-5, -5, -5, -5,outline="red",width=5)
    zel_ramka=doska.create_rectangle(-5, -5, -5, -5,outline="green",width=5)

    while x<8*k:#малюємо дошку
        y=1*k
        while y<8*k:
            doska.create_rectangle(x, y, x+k, y+k,fill="black")
            y+=2*k
        x+=2*k
    x=1*k
    while x<8*k:
        y=0
        while y<8*k:
            doska.create_rectangle(x, y, x+k, y+k,fill="black")
            y+=2*k
        x+=2*k

    for y in range(8):#малюємо стоячі шашки
        for x in range(8):
            z=pole[y][x]
            if z:  
                if (x_poz_1,y_poz_1)!=(x,y):#чи шашка стояча
                    doska.create_image(x*k,y*k, anchor=NW, image=peshki[z])
    #активна пішка
    z=pole[y_poz_1][x_poz_1]
    if z:
        doska.create_image(x_poz_1*k,y_poz_1*k, anchor=NW, image=peshki[z],tag='ani')
    #коефіцієнт анімації
    kx = 1 if x_poz_1<x_poz_2 else -1
    ky = 1 if y_poz_1<y_poz_2 else -1
    for i in range(abs(x_poz_1-x_poz_2)):#анімація руху шашки
        for ii in range(33):
            doska.move('ani',0.03*k*kx,0.03*k*ky)
            doska.update()#оновлення дошки
            time.sleep(0.01)

def soobsenie(s):
    global f_hi
    z='Гра завершена'
    if s==1:
        i=messagebox.askyesno(title=z, message='Вы перемогли!\nНатисність "Так" для початку нової гри', icon='info')
    if s==2:
        i=messagebox.askyesno(title=z, message='Вы програли!\nНатисність "Так" для початку нової гри', icon='info')
    if s==3:
        i=messagebox.askyesno(title=z, message='Ходів больше нема.\nНатисність "Так" для початку нової гри', icon='info')
    if i:
        novaya_igra()
        vivod(-1,-1,-1,-1)#нове поле
        f_hi=True#переход до ходу гравця

def pozici_1(event):#вибір клітинки для першого ходу
    x,y=(event.x)//100,(event.y)//100#координати
    doska.coords(zel_ramka,x*100,y*100,x*100+100,y*100+100)#малюємо рамку в вибраній клітинці

def pozici_2(event):#вибір клітинки для другого ходу
    global poz1_x,poz1_y,poz2_x,poz2_y
    global f_hi
    x,y=(event.x)//100,(event.y)//100#координати
    if pole[y][x]==1 or pole[y][x]==2:#перевірка, чи є тут шашка
        doska.coords(kr_ramka, x*100, y*100, x*100+100, y*100+100)#малюємо рамку в вибраній клітинці
        poz1_x,poz1_y=x,y
    else:
        if poz1_x!=-1:#перевірка вибору клітинки
            poz2_x,poz2_y=x,y
            if f_hi:#чи зараз хід гравця?
                hod_igroka()
                if not(f_hi):
                    time.sleep(0.5)
                    hod_kompjutera() #передача ходу

            poz1_x=-1#якщо клітинка не вибрана
            doska.coords(kr_ramka,-5,-5,-5,-5)#рамка за межами поля
     
def hod_kompjutera():
    global f_hi
    global n2_spisok
    proverka_hk(1, (), [])
    if n2_spisok:#наявність доступних ходів
        kh=len(n2_spisok)#кі-ть ходів
        th=random.randint(0,kh-1)#випадковий хід
        dh=len(n2_spisok[th])#довжина ходу
        for i in range(dh-1):
            #виконування коду
            spisok=hod(1,n2_spisok[th][i][0], n2_spisok[th][i][1], n2_spisok[th][1+i][0], n2_spisok[th][1+i][1])
        n2_spisok=[]#очистка списку
        f_hi=True#передача ходу

    #визначення переможця
    s_k,s_i=skan()
    if not(s_i):
            soobsenie(2)
    elif not(s_k):
            soobsenie(1)
    elif f_hi and not(spisok_hi()):
            soobsenie(3)
    elif not(f_hi) and not(spisok_hk()):
            soobsenie(3)

def spisok_hk():#список ходів пк
    spisok=prosmotr_hodov_k1([])#обов'язкові ходи(бій, єдиний хід і т.д)
    if not(spisok):
        spisok=prosmotr_hodov_k2([])#ті ходи, що залишились
    return spisok

def proverka_hk(tur,n_spisok,spisok):
    global pole
    global n2_spisok
    global l_rez,k_rez,o_rez
    if not(spisok):#якщо список пустий
        spisok=spisok_hk()#йде заповнення

    if spisok:
        k_pole=copy.deepcopy(pole)#копіювання поля
        for ((poz1_x,poz1_y),(poz2_x,poz2_y)) in spisok:#проходимо всі ходи по списку ходів
            t_spisok=hod(0, poz1_x, poz1_y, poz2_x, poz2_y)
            if t_spisok:#якщо хід можливий
                proverka_hk(tur,(n_spisok+((poz1_x,poz1_y),)),t_spisok)
            else:
                proverka_hi(tur, [])
                if tur==1:
                    t_rez=o_rez/k_rez
                    if not(n2_spisok):#якщо список пустий, записуємо значення
                        n2_spisok=(n_spisok+((poz1_x,poz1_y),(poz2_x,poz2_y)),)
                        l_rez=t_rez#зберігаємо найкращий ходу
                    else:
                        if t_rez==l_rez:#якщо вже є елементи
                            n2_spisok=n2_spisok+(n_spisok+((poz1_x,poz1_y),(poz2_x,poz2_y)),)
                        if t_rez>l_rez:
                            n2_spisok=()
                            n2_spisok=(n_spisok+((poz1_x,poz1_y),(poz2_x,poz2_y)),)
                            l_rez=t_rez#зберігання кращого ходу
                    o_rez=0
                    k_rez=0

            pole=copy.deepcopy(k_pole)#повертмаємо поле
    else:#???
        s_k,s_i=skan()#результати ходу
        o_rez+=(s_k-s_i)
        k_rez+=1

def spisok_hi():#список ходів гравця
    spisok=prosmotr_hodov_i1([])#обов'язкові ходи
    if not(spisok):
        spisok=prosmotr_hodov_i2([])#ті, що залишаться
    return spisok
    
def proverka_hi(tur, spisok):
    global pole,k_rez,o_rez
    global ur
    if not(spisok):
        spisok=spisok_hi()
    if spisok:#наявність доступних ходів
        k_pole=copy.deepcopy(pole)#копіювання поля
        for ((poz1_x, poz1_y), (poz2_x, poz2_y)) in spisok:
            t_spisok=hod(0, poz1_x, poz1_y, poz2_x, poz2_y)
            if t_spisok:#якщо можливі декілька ходів
                proverka_hi(tur, t_spisok)
            else:
                if tur<ur:
                    proverka_hk(tur+1, (), [])
                else:
                    s_k,s_i=skan()#результати ходу
                    o_rez+=(s_k-s_i)
                    k_rez+=1

            pole=copy.deepcopy(k_pole)#повертаємо поле
    else:#якзо нема ходів
        s_k,s_i=skan()#результати ходу
        o_rez+=(s_k-s_i)
        k_rez+=1

def skan():#підрахунок кількості шашок
    global pole
    s_i=0
    s_k=0
    for i in range(8):
        for ii in pole[i]:
            if ii==1:s_i+=1
            if ii==2:s_i+=3
            if ii==3:s_k+=1
            if ii==4:s_k+=3
    return s_k,s_i

def hod_igroka():
    global poz1_x,poz1_y,poz2_x,poz2_y
    global f_hi
    f_hi=False#завершення ходу
    spisok=spisok_hi()
    if spisok:
        if ((poz1_x,poz1_y),(poz2_x,poz2_y)) in spisok:#чи хід зроблений по правилах
            t_spisok=hod(1,poz1_x,poz1_y,poz2_x,poz2_y)#виконнаня ходу
            if t_spisok:#якщо декілька варіантів ходу
                f_hi=True#хід невиповненим
        else:
            f_hi=True#хід не виконаний
    doska.update()#!!!обновление

def hod(f,poz1_x,poz1_y,poz2_x,poz2_y):
    global pole
    if f:vivod(poz1_x,poz1_y,poz2_x,poz2_y)#малюємо поле
    #зміна позиції білих
    if poz2_y==0 and pole[poz1_y][poz1_x]==1:
        pole[poz1_y][poz1_x]=2
    #зміна позиції чорних
    if poz2_y==7 and pole[poz1_y][poz1_x]==3:
        pole[poz1_y][poz1_x]=4
    #робимо хід
    pole[poz2_y][poz2_x]=pole[poz1_y][poz1_x]
    pole[poz1_y][poz1_x]=0

    #взяття шашки
    kx=ky=1
    if poz1_x<poz2_x:kx=-1
    if poz1_y<poz2_y:ky=-1
    x_poz,y_poz=poz2_x,poz2_y
    while (poz1_x!=x_poz) or (poz1_y!=y_poz):
        x_poz+=kx
        y_poz+=ky
        if pole[y_poz][x_poz]!=0:
            pole[y_poz][x_poz]=0
            if f:vivod(-1,-1,-1,-1)#малюємо поле
            #перевіряємо хід шашкою, що мала бити
            if pole[poz2_y][poz2_x]==3 or pole[poz2_y][poz2_x]==4:#для взяття пк
                return prosmotr_hodov_k1p([],poz2_x,poz2_y)#лоступні ходи
            elif pole[poz2_y][poz2_x]==1 or pole[poz2_y][poz2_x]==2:#для гравця
                return prosmotr_hodov_i1p([],poz2_x,poz2_y)#доступні ходи
    if f:vivod(poz1_x,poz1_y,poz2_x,poz2_y)#малюємо поле заново

def prosmotr_hodov_k1(spisok):#обов'зкові ходи
    for y in range(8):#скануємо поле
        for x in range(8):
            spisok=prosmotr_hodov_k1p(spisok,x,y)
    return spisok

def prosmotr_hodov_k1p(spisok,x,y):
    if pole[y][x]==3:#вибір шашки
        for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
            if 0<=y+iy+iy<=7 and 0<=x+ix+ix<=7:
                if pole[y+iy][x+ix]==1 or pole[y+iy][x+ix]==2:
                    if pole[y+iy+iy][x+ix+ix]==0:
                        spisok.append(((x,y),(x+ix+ix,y+iy+iy)))#запис ходу в кінець списку
    if pole[y][x]==4:#дамка
        for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
            osh=0#чи хід є вірним
            for i in  range(1,8):
                if 0<=y+iy*i<=7 and 0<=x+ix*i<=7:
                    if osh==1:
                        spisok.append(((x,y),(x+ix*i,y+iy*i)))#запис ходу в кінець списку
                    if pole[y+iy*i][x+ix*i]==1 or pole[y+iy*i][x+ix*i]==2:
                        osh+=1
                    if pole[y+iy*i][x+ix*i]==3 or pole[y+iy*i][x+ix*i]==4 or osh==2:
                        if osh>0:spisok.pop()#якщо є помилка, видаляємо зі списку
                        break
    return spisok

def prosmotr_hodov_k2(spisok):#перевірка інших ходів
    for y in range(8):#скануємо поле
        for x in range(8):
            if pole[y][x]==3:#вибір шашки
                for ix,iy in (-1,1),(1,1):
                    if 0<=y+iy<=7 and 0<=x+ix<=7:
                        if pole[y+iy][x+ix]==0:
                            spisok.append(((x,y),(x+ix,y+iy)))#запис ходу в кінець списку
                        if pole[y+iy][x+ix]==1 or pole[y+iy][x+ix]==2:
                            if 0<=y+iy*2<=7 and 0<=x+ix*2<=7:
                                if pole[y+iy*2][x+ix*2]==0:
                                    spisok.append(((x,y),(x+ix*2,y+iy*2)))#запис ходу в кінець списку
            if pole[y][x]==4:#дамка
                for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
                    osh=0#чи хід вірний
                    for i in range(1,8):
                        if 0<=y+iy*i<=7 and 0<=x+ix*i<=7:
                            if pole[y+iy*i][x+ix*i]==0:
                                spisok.append(((x,y),(x+ix*i,y+iy*i)))#запис ходу в кінець списку
                            if pole[y+iy*i][x+ix*i]==1 or pole[y+iy*i][x+ix*i]==2:
                                osh+=1
                            if pole[y+iy*i][x+ix*i]==3 or pole[y+iy*i][x+ix*i]==4 or osh==2:
                                break
    return spisok

def prosmotr_hodov_i1(spisok):#обов'язкові ходи
    spisok=[]#список ходів
    for y in range(8):#скануємо поле
        for x in range(8):
            spisok=prosmotr_hodov_i1p(spisok,x,y)
    return spisok

def prosmotr_hodov_i1p(spisok,x,y):
    if pole[y][x]==1:#вибір шашки
        for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
            if 0<=y+iy+iy<=7 and 0<=x+ix+ix<=7:
                if pole[y+iy][x+ix]==3 or pole[y+iy][x+ix]==4:
                    if pole[y+iy+iy][x+ix+ix]==0:
                        spisok.append(((x,y),(x+ix+ix,y+iy+iy)))#запис ходу в кінець списку
    if pole[y][x]==2:#дамка
        for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
            osh=0#вірність ходу
            for i in  range(1,8):
                if 0<=y+iy*i<=7 and 0<=x+ix*i<=7:
                    if osh==1:
                        spisok.append(((x,y),(x+ix*i,y+iy*i)))#запис ходу в кінець списку
                    if pole[y+iy*i][x+ix*i]==3 or pole[y+iy*i][x+ix*i]==4:
                        osh+=1
                    if pole[y+iy*i][x+ix*i]==1 or pole[y+iy*i][x+ix*i]==2 or osh==2:
                        if osh>0:spisok.pop()#видалення ходу зі списку
                        break
    return spisok

def prosmotr_hodov_i2(spisok):#наявність всіх інших ходів
    for y in range(8):#скан поля
        for x in range(8):
            if pole[y][x]==1:#пешка
                for ix,iy in (-1,-1),(1,-1):
                    if 0<=y+iy<=7 and 0<=x+ix<=7:
                        if pole[y+iy][x+ix]==0:
                            spisok.append(((x,y),(x+ix,y+iy)))#запис ходу в кінець списку
                        if pole[y+iy][x+ix]==3 or pole[y+iy][x+ix]==4:
                            if 0<=y+iy*2<=7 and 0<=x+ix*2<=7:
                                if pole[y+iy*2][x+ix*2]==0:
                                    spisok.append(((x,y),(x+ix*2,y+iy*2)))#запис ходу в кінець списку
            if pole[y][x]==2:#дамка
                for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
                    osh=0#чи нема помилок
                    for i in range(1,8):
                        if 0<=y+iy*i<=7 and 0<=x+ix*i<=7:
                            if pole[y+iy*i][x+ix*i]==0:
                                spisok.append(((x,y),(x+ix*i,y+iy*i)))#запис ходу в кінець списку
                            if pole[y+iy*i][x+ix*i]==3 or pole[y+iy*i][x+ix*i]==4:
                                osh+=1
                            if pole[y+iy*i][x+ix*i]==1 or pole[y+iy*i][x+ix*i]==2 or osh==2:
                                break
    return spisok

izobrazheniya_peshek()#грузимо зображеня
novaya_igra()#початок гри
vivod(-1, -1, -1, -1)#малювання поля
doska.bind("<Motion>", pozici_1)#считування координат миші
doska.bind("<Button-1>", pozici_2)#лкм натиск

mainloop()
