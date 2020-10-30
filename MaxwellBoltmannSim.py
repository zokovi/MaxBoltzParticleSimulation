# PYTHON VERSION 3.8
#------IMPORT PYTHON MODULES---------------
import time
import random 
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import warnings
import matplotlib.cbook
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)
#------------------------------------------

start_time = time.time()
current_time = time.strftime("%y-%m-%d-%H.%M.%S", time.localtime()) 

particles = []
# Particle Radius
r_ball = 2
# PANJANG KOTAK
box_size = 200
# JUMLAH PARTIKEL
n = 20
nball = n*n
# FRAME ANIMASI 
#frame = int(input("Jumlah iterasi: "))
frame = 200

# INISIASI CLASS---------------------------
class particle:
    def __init__(self,x,y,dx,dy,radii,color,shape):
        self.dx = dx
        self.dy = dy
        self.shape = shape
        self.color = color
        self.radii = radii
        self.x = x
        self.y = y
    
    def setx(self, xnew):
        self.x = xnew

    def sety(self, ynew):
        self.y = ynew

    def distance(self, p2):
        rx = self.x - p2.x
        ry = self.y - p2.y
        return np.sqrt(rx*rx + ry*ry)

    def collision(self,b): 
        #----TUMBUKAN ELASTIK function------------
        a = self
        v1 = np.array([a.dx, a.dy])
        v2 = np.array([b.dx, b.dy])
        x1 = np.array([a.x, a.y])
        x2 = np.array([b.x, b.y])
        v1new = v1 - (v1-v2).dot(x1-x2)/(np.linalg.norm(x1-x2))**2 *(x1-x2)
        v2new = v2 - (v2-v1).dot(x2-x1)/(np.linalg.norm(x2-x1))**2 *(x2-x1)
        return [v1new, v2new]
        #----------------------------------------

#------------ENERGI & KECEPATAN AWAL PARTIKEL--------------
EnergiTotal = nball*0.3
EnergiAwal = np.random.uniform(0.0,1.5,nball) 
EnergiAwal = EnergiAwal * EnergiTotal/EnergiAwal.sum()

vawal = np.sqrt(2*EnergiAwal)
print(f'energi = {np.array([p**2 for p in vawal]).sum()*1/2}')
for i in range(nball):
    rnd = 2*np.pi*random.random()
    dx = vawal[i]*np.cos(rnd)
    dy = vawal[i]*np.sin(rnd)
    shape = "circle"
    x = 0
    y = 0
    color = "red"
    particles.append(particle(x,y,dx,dy,r_ball,color,shape))
#-----------------------------------------------------------------

#--------------POSISI AWAL PARTIKEL ----------------------------
k=0
for i in range(n):
    for j in range(n):
        x_start = (box_size/2-box_size/n)/n*2 *i  +box_size/n
        y_start = (box_size/2-box_size/n)/n*2 *j  +box_size/n
        particles[k].setx(x_start)
        particles[k].sety(y_start)
        k += 1    
#-----------------------------------------------------------------
      

vi = np.zeros(nball)
Mx = np.array([])
My = np.array([])
v = np.array([])
number_of_frames = 0

#------LOOP SIMULASI-------------------------
print('simulating.....')
iterr = -1
while (iterr < frame):
    iterr +=1
    k=0
    xap = np.array([])
    yap = np.array([])

    #--------- CEK TUMBUKAN ANTAR PARTIKEL--------------
    for i in range(0,len(particles)):
        for j in range(i,len(particles)): 
            if i < j:
                if particles[i].distance(particles[j]) < r_ball*2:
                    [particles[i].dx, particles[i].dy], [particles[j].dx, particles[j].dy] = particles[i].collision(particles[j])

    #---------- CEK TUMBUKAN DENGAN DINDING KOTAK----------
    for ball in particles:

        xap = np.append(xap, ball.x)
        yap = np.append(yap, ball.y)

        ball.sety(ball.y + ball.dy)
        ball.setx(ball.x + ball.dx)

        if ball.y > box_size-r_ball:
            ball.dy *= -1
            ball.y = box_size-r_ball
        if ball.y < 0+r_ball:
            ball.dy *= -1
            ball.y = 0+r_ball

        if ball.x >  box_size-r_ball:
            ball.dx *= -1
            ball.x = box_size-r_ball
        if ball.x < 0+r_ball:
            ball.dx *= -1  
            ball.x = 0+r_ball                 

        vi[k] = np.sqrt(ball.dx**2 + ball.dy**2)
        k+=1

    if iterr == 0:
        v = vi
        Mx = xap
        My = yap
        number_of_frames = number_of_frames +1
    elif iterr % 1 == 0:
        v = np.vstack([v, vi])
        Mx = np.vstack([Mx, xap])
        My = np.vstack([My, yap])
        number_of_frames = number_of_frames +1

    if iterr%10==0:
        print('------iteration: {}------------'.format(iterr))
        print(f'energi = {np.array([p**2 for p in vi]).sum()*1/2}')
    

print('===========================================')
print(f"Iteration finished. It took {time.time()-start_time} seconds")
print(f"Plotting...")


num = 0
bins1 = np.linspace(0,3,18)
weight = np.ones_like(v[0]) / len(v[0])

#--------kurva PDF--------------
vpdf = np.linspace(0,3)
def MBvpdf(v):
    beta = 3.08
    c = 0.56
    a = c * v * np.exp(-(beta*v**2)/2) 
    return a
#-------------------------------


def updateanim(num, Mx, My):
    weight = np.ones_like(v[num]) / len(v[num])
    plt.subplot(211)
    plt.cla()
    plt.scatter(Mx[num], My[num],s=18)
    plt.xlim(0,box_size)
    plt.ylim(0,box_size)
    plt.title('Plot posisi partikel')
    plt.subplot(212)
    plt.cla()
    plt.hist(v[num], bins=bins1,edgecolor='black',weights=weight)
    plt.text(1.25,0.375,f'(Energi Sistem = {np.array([p**2 for p in v[num]]).sum()*0.5:.7})')
    plt.text(1.25,0.35,f'Iterasi no: {num}')
    plt.plot(vpdf,MBvpdf(vpdf))
    plt.title('Distribusi kecepatan')
    plt.ylim(0,0.4)
    plt.xlim(0,3)
    plt.xlabel('v')
    plt.ylabel('Probability Desity')



wha = 0
while True:
    wha = int(input('input (1 to show plot, 2 to save to mp4, 0 to exit): '))
    if wha == 1:
        fig = plt.figure()
        fig.set_size_inches(5, 11)
        fig.canvas.draw()
        anim = animation.FuncAnimation(fig, updateanim, int(number_of_frames), fargs=(Mx,My), interval=1, blit=False)
        plt.show()
        plt.draw()
    elif wha == 2:
        fig = plt.figure()
        fig.set_size_inches(5, 11)
        fig.canvas.draw()
        anim = animation.FuncAnimation(fig, updateanim, int(number_of_frames), fargs=(Mx,My), interval=1, blit=False)
        # USE THIS TO SAVE TO MP4
        plt.rcParams['animation.ffmpeg_path'] ='C:\\ffmpeg\\bin\\ffmpeg.exe'
        FFwriter = animation.FFMpegWriter(fps=15)
        video_path = f'hasil-{current_time}.mp4'  #PATH TO SAVE VIDEO
        anim.save(video_path, writer=FFwriter)
        break
    elif wha == 0:
        break


print(f'energi = {np.array([p**2 for p in v[number_of_frames-1]]).sum()*1/2}')


# fig = plt.figure()
# hist = plt.hist(data[0])
# animation = animation.FuncAnimation(fig, update_hist, int(number_of_frames), fargs=(data, ), interval=1 )
# plt.show()


























