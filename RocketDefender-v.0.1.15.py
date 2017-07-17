
import tkinter, time, threading, winsound, random
    
def go(event):
##    print('entered')
    global hit
##    if hit == True:
##        print(hit)
    if hit == False:
##        print('go')
        global a
        global canvas, ship
        a+=10
        canvas.move(ship, 10, 0)
##        print(a,b)

def gameover_func():
    global gameover, canvas, ship, alien, fon1, threads, alien_movement_thread
    gameover = True
    canvas.delete(ship)
    canvas.delete(alien)
    canvas.delete(planet)
    canvas.delete(fon1)
    gameoverscreen = tkinter.PhotoImage(file = 'game_over.gif')
    gos = canvas.create_image(0,600, anchor = 'sw', image = gameoverscreen)
    winsound.Beep(800,170)
    winsound.Beep(1000,170)
    winsound.Beep(1200,170)
    winsound.Beep(600,400)
    for thread in threads:
        thread.join()
    time.sleep(2)
##    alien_movement_thread.join()
    print('Your score   '+str(kills_count))

def back(event):
    global hit
    if hit == False:
        global a
        global canvas, ship
        a-=10
        canvas.move(ship, -10, 0)
##        print(a,b)


def jump(event):
    global hit
    if hit == False:
        global b
        global canvas, ship
        b-=10
        canvas.move(ship, 0, -10)
##        print(a,b)

def fall(event):
    global hit
    if hit == False:
        global b
        global canvas, ship
        b+=10
        canvas.move(ship, 0, 10)
##        print(a,b)

def fire():
    global hit
    if hit == False:
        global canvas
        global a,b
        global threadsnumber, alien, alienx, alieny, dead, kills_count
    ##    print('Fire')
        bullet = canvas.create_rectangle(a+24,b-58,a+32, b-67,fill="red")
        bulletx_1 = a+24
        bulletx_2 = a+32
        bullety_1 = b-58
        bullety_2 = b-67
        winsound.Beep(800,100)
        for i in range(int(abs(b-70)/3)):
            canvas.move(bullet, 0, -3)
            bullety_1 -= 3
            bullety_2 -= 3
            bullet_cords = [{'x':bulletx_1,'y': bullety_1}, {'x': bulletx_2,'y': bullety_2}]
            for i in bullet_cords:
##                print(i, alienx, alieny)
                if (alienx <= i['x'] <= alienx+60) and (alieny-68 <= i['y'] <= alieny) and (dead == False) and (started == True) and (closed == False):
##                    print('got')
##                    print('shot at '+str(alienx)+' '+str(alieny))
                    canvas.delete(alien)
                    canvas.delete(bullet)
                    kills_count += 1
                    dead = True
                    blow = canvas.create_rectangle(alienx, alieny, alienx+60, alieny-68, fill = 'yellow')
                    winsound.Beep(300,100)
                    canvas.delete(blow)
                    break
            time.sleep(0.04)
        canvas.delete(bullet)
        threads.pop(threadsnumber-1)
        threadsnumber -= 1

def firinit(event):
    global hit
    if hit == False:
        global threads
        global threadsnumber
        if threadsnumber < 3:
            t = threading.Thread(target = fire)
            if len(threads) <= threadsnumber:
                threads.append(t)
            threads[threadsnumber].start()
            threadsnumber += 1

def alien_movement():
    global canvas, alien, alienx, alieny, closed, dead, live, ship, a, b,gameover, hit, root, fon1, gos
    while (closed == False) and (gameover == False):
        xspeed = random.randint(-7,7)
##        print(xspeed)
        yspeed = random.randint(-7,7)
##        print(yspeed)
        if dead == False:
            alienx, alieny = random.randint(300,500),100
##            print('created at '+str(alienx)+' '+str(alieny))
            alien  = canvas.create_image(alienx,alieny, anchor = 'sw', image = alien_image)
            global started
            started = False
        time.sleep(0.05)
        while dead == False and gameover == False:
##            print('ok')
            if (20 >= alienx) or (alienx >= 700):
##                print(xspeed)
                xspeed = -xspeed
            elif (20 >= alieny) or (alieny >= 500):
##                print(yspeed)
                yspeed = -yspeed
            if (closed ==  False) and (dead == False):
                if started == False:
                    started = True
                canvas.move(alien,xspeed,yspeed)
                alienx += xspeed
                alieny += yspeed
                aliencords = [{'x':alienx, 'y':alieny},{'x':alienx+60, 'y':alieny-68}]
                for i in aliencords:
                    if (a <= i['x'] <= a + 56) and (b-53 <= i['y'] <= b) and (hit == False) and (closed == False):
    ##                    print('hit')
                        hit = True
                        live -= 1
                        if closed == False:
                            bang = canvas.create_rectangle(a,b,a+56,b-53,fill = "yellow")
                            winsound.Beep(1800,250)
                            canvas.delete(bang)
                            canvas.move(ship, 70, 70)
                            a += 70
                            b += 70
                            if (live == 0) and (closed == False):
                                gameover_func()
                        break
            time.sleep(0.04)
##            print(alienx, alieny)
            hit = False
        time.sleep(1)
        dead = False

hit = False   
kills_count = 0
live = 4
closed = False
dead = False
gameover = False
bullets = []
threads = []
threadsnumber = 0
root = tkinter.Tk()
root.geometry('800x600')
canvas = tkinter.Canvas(root,width = 800, height = 600)
img1 = 'spaceship.gif'
planet_image = tkinter.PhotoImage(file = 'planet.gif')
ship_image = tkinter.PhotoImage(file = img1)
alien_image = tkinter.PhotoImage(file = 'alien.gif')
fon = tkinter.PhotoImage(file = 'space.gif')
fon1 = canvas.create_image(0,600, anchor = 'sw', image = fon)
a=70   #абсцисса кораблика
b=500 #ордината кораблика
ship = canvas.create_image(a,b, anchor = 'sw', image=ship_image)
planet = canvas.create_image(200,300, anchor = 'sw', image = planet_image)
alien_movement_thread = threading.Thread(target = alien_movement)
canvas.place(x = 0, y = 600, anchor = 'sw')
canvas.focus_set()
canvas.bind("d", go)
canvas.bind("a",back)
canvas.bind("w",jump)
canvas.bind("s",fall)
canvas.bind('<space>',firinit)
alien_movement_thread.start()
root.mainloop()
closed = True
