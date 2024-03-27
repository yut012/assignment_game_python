import pyxel

class Player :
    def __init__(self):
        self.x = 10
        self.y = 100
        self.speed = 3
        self.life = 3

    def move (self):
        if self.y <= 200 or  self.y >= 0: 
            if pyxel.btn(pyxel.KEY_DOWN) and self.y<=200 :
                self.y += self.speed
    
            elif pyxel.btn(pyxel.KEY_UP) and self.y >= 0:
                self.y -= self.speed

class Object:
    def __init__(self):
        self.x = 200
        self.y = pyxel.rndi(5,195)
        self.speed = 3
        angle = pyxel.rndi(30, 150)
        self.vx = pyxel.cos(angle)
        self.vy = pyxel.sin(angle)

    def move(self,mode):
        if mode == 1 :    
           self.x -= self.speed
        if mode == 2:
            self.x -= self.vy*2
            self.y -= self.vx*2
            if self.y <=0 or self.y>=200:
                self.vx*=-1

class Point:
    def __init__(self):
        self.x = 200
        self.y = pyxel.rndi(5,195)
        self.speed = 4
    

    def move(self):
        self.x -= self.speed

class Start:
    def __init__(self):
        pyxel.init(200,200)
        Intro()

class Intro :
    def __init__(self):
        pyxel.run(self.update,self.draw)

    def update(self):
        if pyxel.btn(pyxel.KEY_E):
            App(1)
        elif pyxel.btn(pyxel.KEY_H):
            App(2)
        
    def draw (self):
        pyxel.cls(7)
        pyxel.text(20,20,'avoid pison ! ' ,2)
        pyxel.text(20,60,'pick points',11)
        pyxel.text(20,100,'easy ; push e',10)
        pyxel.text(20,140,'hard ; push h',10)

class Game_over:
    def __init__(self,score):
        self.score = score
        pyxel.run(self.update, self.draw)

    def update (self):
        if pyxel.btn(pyxel.KEY_SPACE):
            Intro()

    def draw (self):
        pyxel.cls(0)
        
        pyxel.text(50,50,'your score is '+str(self.score),9)
        a = "game over"
        b = pyxel.frame_count % (len(a) + 10)
        if b < len(a):
            pyxel.text(60 + b*3, 70, a[b], pyxel.frame_count%16)
        elif b % 3 <= 1:
            pyxel.text(60, 70, a, pyxel.frame_count%16)
        pyxel.text (30,100,'Press space key to space to the menu.',4)

class App:
    def __init__(self, mode):
        
        self.player = Player()
        self.objects = []
        self.points = []
        self.timer = 0
        self.score = 0
        self.mode_select = mode
        self.combo = 0
        self.combohantei = True
        pyxel.run(self.draw,self.update)
  
            

    def draw(self):
        pyxel.cls(7)
        pyxel.circ(self.player.x+5,self.player.y,10,11)
        pyxel.circb(self.player.x+5,self.player.y,10,pyxel.frame_count%16)
        for o in self.objects :
            pyxel.circ(o.x,o.y,16,2)
        for p in self.points :
            pyxel.circb(p.x,p.y,10,11)

 

        pyxel.text(130,190,'life : '+str(self.player.life),9)
        pyxel.text(5,5,'your score is '+ str(self.score),11)
        pyxel.text(130,5,str(self.combo)+'combo ! ',12)
    
            



    def update (self):

        self.player.move()
        self.timer = pyxel.frame_count
        
        if self.mode_select == 1:
            if self.timer % 40 == 0:  
                self.objects.append(Object())
        elif self.mode_select == 2:
            if self.timer % 30 == 0:
                self.objects.append(Object())

        if self.timer % 90 == 0 :
            self.points.append(Point())



        for obj in self.objects:
            obj.move(self.mode_select)
            if obj.x < -10:  
                self.objects.remove(obj)
        
        
        for pts in self.points:
            pts.move()
            if pts.x < -10:
                self.points.remove(pts)
                self.combo = 0

        for a in self.objects:
            if  ((a.x-self.player.x)**2+(a.y-self.player.y)**2)**0.5<=26 :
                self.player.life -= 1
                #self.combo = 0
                self.objects.remove(a)
                
        
        
        for b in self.points:
            if  ((b.x-self.player.x)**2+(b.y-self.player.y)**2)**0.5<=20 :
                self.score += 1
                self.combo += 1
                if self.combo%10 != 0:
                    self.combohantei = True
                self.points.remove(b)

        if self.combo % 10 == 0 and self.combo != 0 and self.combohantei == True:  
            self.score += 10
            self.combohantei = False

        if self.player.life == 0:
            Game_over(self.score)


Start()