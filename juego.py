import os, inspect, time, sys, math, random, pygame, pygame.mixer
from time import time
from random import random
from pygame.locals import *

screen_size = screen_width, screen_height = 1000, 600
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
pygame.display.set_caption('Juego Chachidiver')
vel_anim = 10
bucle = True

camino = inspect.getfile(inspect.currentframe())
print "Fichero:", camino
print "Camino:", camino[:-8]

bicho_1 = pygame.image.load(camino[:-8] + "bicho_2.png")
img_h = 64
img_w = 80

def rand():
	return random()*2 - 1

def signo(x):
	if x < 0:
		return -1
	return 1

def mezclar(color1, color2):
	media = sum(list(color1))
	colorm = [(color1[ii] + color2[ii])/2 for ii in range(3)]
	media2 = sum(list(colorm)) + 0.1
	f = media*1.0/media2
	return tuple(colorm)#tuple([int(f*colorm[ii] + 0.5) for ii in range(3)])

bichos_de_colores = []
for ii in range(4):
	bichos_de_colores.append([])
	for jj in range(4):
		print ii, jj
		bichos_de_colores[ii].append([])
		for kk in range(4):
			color_ijk = (85*ii, 85*jj, 85*kk)
			bichos_de_colores[ii][jj].append(pygame.image.load(camino[:-8] + "bicho_2.png"))
			for xx in range(img_w):
				for yy in range(img_h):
					cccc = bichos_de_colores[ii][jj][kk].get_at((xx, yy))
					tttt = (cccc.r, cccc.g, cccc.b)
					tttt = mezclar(tttt, color_ijk)
					cccc.r, cccc.g, cccc.b = tttt
					bichos_de_colores[ii][jj][kk].set_at((xx, yy), cccc)


class Bicho:
	iden = -1
	x = random()*screen_width
	y = random()*screen_height
	vx = rand()*3
	vy = rand()*3
	phi = random()*2*math.pi
	color = [int(random()*256) for ii in range(3)]
	radio = random()*20
	def __init__(self, iden):
		self.iden = iden
		self.x = random()*screen_width
		self.y = random()*screen_height
		self.vx = rand()*3
		self.vy = rand()*3
		self.phi = random()*2*math.pi
		self.color = tuple([int(random()*4)*85 for ii in range(3)])
		self.radio = random()*20
	def dibujar(self):
		screen.blit(pygame.transform.rotate(bichos_de_colores[self.color[0]/85][self.color[1]/85][self.color[2]/85], self.phi/math.pi*180), rectangulo.move(self.x, self.y))
		#pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.radio) + 1, 1)
	def mover(self, ran):
		self.x += self.vx
		self.y += self.vy
		self.phi = math.atan(-self.vy/self.vx)
		if self.x + img_w/1.4 < 0:
			self.x += screen_width + img_w*1.4
		if self.x - img_w/1.4 > screen_width:
			self.x -= screen_width + img_w*1.4
		if self.y + img_h/1.4 < 0:
			self.y += screen_height + img_h*1.4
		if self.y - img_h/1.4 > screen_height:
			self.y -= screen_height + img_h*1.4
		if self.vx < 0:
			self.phi += math.pi

class Laberinto:
	size = 10
	start = (5, 5)
	matris = [[True for ii in range(size)] for jj in range(size)]
	def __init__(self):
		self.size = 10
		self.matris = [[True for ii in range(size)] for jj in range(size)]
	def make_exit(self, point):
		xx, yy = point
		matris[xx][yy] = False
		if self.matris[xx][yy + 1]:
			self.make_exit((xx, yy + 1))
	def hacer_camino(self, point):
		xx, yy = point
		matris[xx][yy] = False
		r = int(random()*4)
		for ii in range(4):
			if self.matris[xx][yy + 1]:
				self.make_exit((xx, yy + 1))
				return None
	def generar(self):
		self.make_exit(self.start)
		for ii in range(5):
			self.hacer_camino(self.start)


pygame.display.set_icon(pygame.image.load(camino[:-8] + "bicho_icono.png"))
bichitos = []
index = 0
pygame.mixer.init()
print 'Volumen:', pygame.mixer.music.get_volume()

pygame.mixer.music.load(camino[:-8] + "Chopin.mp3")
pygame.mixer.music.play()

rectangulo = bicho_1.get_rect().move(-40, -32)

while bucle:
	for evento in pygame.event.get():
		if evento.type == pygame.QUIT:
			bucle = False

	#pygame.draw.circle(screen, (200, 200, 200), (index, 200), 20, 2)height
	clock.tick(vel_anim)
	screen.fill((255, 255, 255))
	#print 'bucle', index
	#mierda(mierda, mas_mierda)
	buggy = Bicho(index)
	bichitos.append(buggy)
	for bichito in bichitos:
		bichito.mover(math.sqrt(index)/2)
		bichito.dibujar()
	index += 1
	#blablabla()

	pygame.display.flip()



