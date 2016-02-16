import os, inspect, sys, math, random, pygame, pygame.mixer
from time import time
from random import random
from pygame.locals import *

screen_size = screen_width, screen_height = 1200, 800
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
pygame.display.set_caption('Juego Chachidiver')
vel_anim = 10
key_controls = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
bucle = True
exit_game_forever = False
dimensiones_laberinto = (25, 25)

camino = inspect.getfile(inspect.currentframe())
print("Fichero:", camino)
print("Camino:", camino[:-8])

img_h = 64
img_w = 80
img_1 = pygame.image.load(camino[:-8] + "bicho_2.png")
rectangulo = img_1.get_rect().move(-img_w/2, -img_h/2)

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

def poner_texto(cadena, alto):
	screen.fill((0, 0, 0))
	pygame.font.init()
	fuente = pygame.font.Font(None, 50)
	dy = alto*len(cadena)/2
	for ind in range(len(cadena)):
		texto = fuente.render(cadena[ind], True, (255, 255, 255), (0, 0, 0))
		dx = texto.get_rect().width/2
		screen.blit(texto, texto.get_rect().move(screen_width/2 - dx, screen_height/2 + alto*ind - dy))
	pygame.display.flip()

poner_texto(["Un jueguecito", "de la mano de", "ANGOSOFT"], 50)

pygame.mixer.init()
print('Volumen:', pygame.mixer.music.get_volume())
pygame.mixer.music.load(camino[:-8] + "Introduccion.mp3")
pygame.mixer.music.play()

print "Haciendo bichitos de colores:",
time0 = time()

bichos_de_colores = []
for ii in range(4):
	bichos_de_colores.append([])
	for jj in range(4):
		#print(ii, jj)
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

print int((time() - time0)*100)/100.0, 'segundos' 

class Imagen:
	def __init__(self, file_name):
		self.area = pygame.image.load(camino[:-8] + file_name)
		self.rect = self.area.get_rect()
	def poner(self, i_x, i_y, phi=0):
		screen.blit(pygame.transform.rotate(self.area, phi), self.rect.move(i_x, i_y))

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
		screen.blit(pygame.transform.rotate(bichos_de_colores[self.color[0]/85][self.color[1]/85][self.color[2]/85], self.phi/math.pi*180),rectangulo.move(self.x, self.y))
		#pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.radio) + 1, 1)
	def mover(self):
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

def delta(r):
	r = r%4
	aaa = (r == 3) - (r == 2)
	bbb = (r == 1) - (r == 0)
	return aaa, bbb

class Laberinto:
	size = (12, 12)
	start = (5, 5)
	matris = [[True for ii in range(size[0])] for jj in range(size[1])]
	def __init__(self, file_name, file_name2, size):
		self.size = size
		self.start = (int(self.size[0]/2), int(self.size[1]/2))
		self.wall_file = file_name
		self.ground_file = file_name2
		self.pared = Imagen(self.wall_file)
		self.suelo = Imagen(self.ground_file)
		self.matris = [[True for ii in range(self.size[0])] for jj in range(self.size[1])]
	def make_exit(self, point, last):
		xx, yy = point
		if xx in [self.size[0] - 1, 0] or yy in [self.size[1] - 1, 0]:
			self.matris[xx][yy] = False
			return [point]
		ccc = 0
		for ii in range(4):
			aa, bb = delta(ii)
			if not self.matris[xx + aa][yy + bb]:
				ccc += 1
			if ccc == 2:
				return False
		self.matris[xx][yy] = False
		r = int(random()*4)
		for ii in range(4):
			if (r + ii)%4 != last%4:
				aa, bb = delta(r + ii)
				result = self.make_exit((xx + aa, yy + bb), r + ii + 2)
				if result != False:
					#self.hacer_camino(point, False)
					return [point] + result
		self.matris[xx][yy] = True
		return False
	def hacer_camino(self, point, sub, depth):
		xx, yy = point
		if xx in [self.size[0] - 1, 0] or yy in [self.size[1] - 1, 0] or depth == 0:
			return None
		if sub:
			ccc = 0
			for ii in range(4):
				aa, bb = delta(ii)
				if not self.matris[xx + aa][yy + bb]:
					ccc += 1
				if ccc == 2:
					return None
		self.matris[xx][yy] = False
		r = int(random()*4)
		for ii in range(4):
			aa, bb = delta(r + ii)
			if self.matris[xx + aa][yy + bb]:
				self.hacer_camino((xx + aa, yy + bb), True, depth - 1)
	def generar(self):
		#self.make_exit(self.start, 4)
		#self.hacer_camino(self.start, False)
		lista_de_puntos = self.make_exit(self.start, 4)
		for punto in lista_de_puntos:
			self.hacer_camino(punto, False, int(self.size[0] + self.size[1]))
	def dibujar(self, center):
		dx = self.pared.rect.width
		dy = self.pared.rect.height
		for ii in range(self.size[0]):
			for jj in range(self.size[1]):
				if self.matris[ii][jj]:
					self.pared.poner(screen_width/2 + dx*(ii - center[0] - 0.5), screen_height/2 + dy*(jj - center[1] - 0.5))
				else:
					self.suelo.poner(screen_width/2 + dx*(ii - center[0] - 0.5), screen_height/2 + dy*(jj - center[1] - 0.5))
		#bieeeeeen dibujos


pygame.display.set_icon(pygame.image.load(camino[:-8] + "bicho_icono.png"))
bichitos = []
index = 0

"""
screen.fill((255, 255, 255))
mylab = Laberinto("bricks.png", (14, 14))
mylab.generar()
mylab.dibujar(mylab.start)
pygame.display.flip()

for iii in range(1000):
	for evento in pygame.event.get():
		if evento.type == pygame.QUIT:
			bucle = False
	clock.tick(200)

pygame.font.init()
fuente = pygame.font.Font(None, 50)
cadena = ['Una ma\xf1ana, tras un sue\xf1o intranquilo, ', 'Gregorio Samsa se despert\xf3 convertido en un monstruoso insecto.']
for ind in range(2):
	texto = fuente.render(cadena[ind], True, (255, 255, 255), (0, 0, 0))
	screen.blit(texto, texto.get_rect().move(0, 50*ind))

pygame.display.flip()
"""
for iii in range(1000):
	for evento in pygame.event.get():
		if evento.type == pygame.QUIT:
			exit_game_forever = True
	clock.tick(200)

#Samsa esta en el laberinto:
pygame.mixer.music.stop()
pygame.mixer.music.load(camino[:-8] + "Laberinto.mp3")
pygame.mixer.music.play(-1)

samsa_img = Imagen("bicho_3.png")
maze = Laberinto("bricks_75.png", "ground_75.png", dimensiones_laberinto)
maze.generar()
screen.fill((255, 255, 255))
samsa_x, samsa_y = maze.start
longitud = maze.pared.rect.width
maze.dibujar((samsa_x, samsa_y))
samsa_width, samsa_height = samsa_img.rect.width, samsa_img.rect.height
samsa_img.poner(screen_width/2 - samsa_width/2, screen_height/2 - samsa_height/2)

while bucle and not exit_game_forever:
	for evento in pygame.event.get():
		if evento.type == pygame.QUIT:
			exit_game_forever = True
	clock.tick(vel_anim)
	teclas = [pygame.key.get_pressed()[ii]!=0 for ii in key_controls]
	if sum(teclas)!=0:
		dx, dy = delta(teclas.index(True))
		if not maze.matris[samsa_x + dx][samsa_y + dy]:
			samsa_x += dx
			samsa_y += dy
			screen.fill((255, 255, 255))
			maze.dibujar((samsa_x, samsa_y))
			samsa_img.poner(screen_width/2 - samsa_width/2, screen_height/2 - samsa_height/2, phi = [90, 270, 180, 0][teclas.index(True)])
		#samsa_img.poner(screen_width/2 - samsa_width/2, screen_height/2 - samsa_height/2, phi = [90, 270, 180, 0][teclas.index(True)])
	pygame.display.flip()
	if samsa_y == 0 or samsa_y == maze.size[1] - 1 or samsa_x == 0 or samsa_x == maze.size[0] - 1:
		bucle = False

#bichitos de colores moviendose por toda la pantalla:
bucle = True

pygame.mixer.music.stop()
pygame.mixer.music.load(camino[:-8] + "Chopin.mp3")
pygame.mixer.music.play()

while bucle and not exit_game_forever:
	for evento in pygame.event.get():
		if evento.type == pygame.QUIT:
			exit_game_forever = True

	#pygame.draw.circle(screen, (200, 200, 200), (index, 200), 20, 2)height
	clock.tick(vel_anim)
	screen.fill((255, 255, 255))
	buggy = Bicho(index)
	bichitos.append(buggy)
	for bichito in bichitos:
		bichito.mover()
		bichito.dibujar()
	index += 1
	#blablabla()

	pygame.display.flip()



