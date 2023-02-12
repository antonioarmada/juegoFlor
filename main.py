
# para compiliar .exe:
# pip install pyinstaller
# pyinstaller --onefile <your_script_name>.py
# ojo que no copia las carpetas con otros archivos, mover manualmente a "dist"


import pygame
import random
import time
import os
import random

#os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0) # posiciona la pantalla ANTE DE INICIALIZAR PYGAME!!!

pygame.init()


infoPantalla = pygame.display.Info()

print (infoPantalla)

display_width = infoPantalla.current_w
display_height =infoPantalla.current_h
velocRegadera=80

gameDisplay = pygame.display.set_mode((display_width,display_height),pygame.FULLSCREEN) #,pygame.RESIZABLE ,pygame.FULLSCREEN
pygame.display.set_caption('UN POCO DE JARDINERÍA')

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
frameGeneral=0

clock = pygame.time.Clock()

class Sprite_animado:
	frame= 1 #aca pongo  atributos comunes a todos las instancias de esta clase no va self
	fin=False
	

	def __init__(self,archivo,anchoFrame,cantFrames): # se ejecuta al iniciar la clase y contiene los atributos
		self.imagen = pygame.image.load(archivo).convert_alpha()
		self.ancho, self.alto = self.imagen.get_size()
		self.anchoFrame= anchoFrame
		self.cantFrames = cantFrames
		#self.invertido=False
	
	def mostrar(self,x,y,frame_,invertido): # es una accion que puede tomar la clase
		#print(self.invertido)
		if not invertido:
			gameDisplay.blit(self.imagen, (x,y),(self.anchoFrame*frame_,0,self.anchoFrame,self.alto)) #el ultimo parentisis es el recorte x_inicial,y_inicial,ancho,alto
		if invertido:
			gameDisplay.blit(pygame.transform.flip(self.imagen,True,False), (x,y),(self.anchoFrame*frame_,0,self.anchoFrame,self.alto))

def calcula_cuadrante():
	cuadrante= [random.randint(1, 2), random.randint(1, 2)] # print lista[0] # 1
	if cuadrante[0]==2 : cuadrante[0]=3
	return cuadrante

def calculaCuadrateMouse(mouseX,mouseY):
	cuadranteMouse=[1,1]
	if mouseX<=display_width/2:
		cuadranteMouse[0]=1
	else:
		cuadranteMouse[0]=3
	if mouseY<=display_height/2:
		cuadranteMouse[1]=1
	else:
		cuadranteMouse[1]=2
	return cuadranteMouse

def checkColision(cuadranteX_planta,cuadranteY_planta,cuadranteX_regadera,cuadranteY_regadera):
	colision=False
	if cuadranteX_planta==cuadranteX_regadera and cuadranteY_planta==cuadranteY_regadera:
		colision=True 
	else:
		colision=False
	return(colision)


def game_loop():
	x =  (display_width * 0.45)
	y = (display_height * 0.8)

	global frameGeneral
	global cuadranteY_regadera, cuadranteX_regadera
	global cuadranteY_planta, cuadranteX_planta
	regaderaX= display_width/2
	regaderaY= display_height/2
	regaderaXactual=regaderaX
	regaderaYactual=regaderaY
	abejaX,abejaY= 0,100
	abejaIda=True
	iniciaColicion=True

	gameExit = False

	pygame.mouse.set_pos([display_width/2, display_height/2])


	while not gameExit:
		frameGeneral +=1
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameExit = True
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if  pygame.key.name(event.key) == "escape":
					pygame.quit()
					quit()
			if event.type == pygame.MOUSEMOTION:
				mouseX, mouseY = pygame.mouse.get_pos()
				cuadranteX_regadera= calculaCuadrateMouse(mouseX,mouseY)[0]
				cuadranteY_regadera= calculaCuadrateMouse(mouseX,mouseY)[1]
				#print (mouseX,mouseY)

		# Anima regadera
		if frameGeneral%3==0: # hago que sea mas lento el framerate de la planta
			if regadera.frame < regadera.cantFrames-1:
				regadera.frame +=1
			else:
				regadera.frame=1
				if not flor_der.fin : aguaSND.play()


		# Anima planta
		if frameGeneral%3==0: # hago que sea mas lento el framerate de la planta
			if planta.frame < planta.cantFrames-1:
				planta.frame +=1
			else:
				planta.frame=1

		# si la regadera esta en el cuadrante crece la flor
		if checkColision(cuadranteX_planta,cuadranteY_planta,cuadranteX_regadera,cuadranteY_regadera):
			if iniciaColicion:
				if not flor_der.fin : plantaCreceSND.play(-1)
				iniciaColicion= False
			# Anima Flor,
			if frameGeneral%4==0 and not tallo.fin: # hago que sea mas lento el framerate del tallo
				if tallo.frame < tallo.cantFrames-1:
					tallo.frame +=1
				else:
					tallo.fin=True

			if frameGeneral%4==0 and not flor_izq.fin and tallo.fin: # hago que sea mas lento el framerate del tallo
				if flor_izq.frame < flor_izq.cantFrames-1:
					flor_izq.frame +=1
				else:
					flor_izq.fin=True

			if frameGeneral%4==0 and not flor_der.fin and flor_izq.fin: # hago que sea mas lento el framerate del tallo
				if flor_der.frame < flor_der.cantFrames-1:
					flor_der.frame +=1
				else:
					flor_der.fin=True
					aguaSND.stop()
					plantaCreceSND.stop()
					abejaIdaSND.play()
					magiaSND.play()

		else:
			iniciaColicion=True
			plantaCreceSND.stop()



		if frameGeneral%4==0 and abejaIda and flor_der.fin:
			if rayos.frame < rayos.cantFrames-1:
				rayos.frame +=1
			else:
				rayos.frame=1
        	

		 # Si temirno el ciclo planta empiezo de nuevo
		if abeja.fin==True:
			cuadranteX_planta=calcula_cuadrante()[0]
			cuadranteY_planta=calcula_cuadrante()[1]
			tallo.fin=False
			tallo.frame=1
			flor_izq.fin=False
			flor_izq.frame=1
			flor_der.fin=False
			flor_der.frame=1
			rayos.fin=False
			rayos.frame=1
			abeja.fin=False
			abeja.frame=1
			abejaX=0
			abejaIda=True
			iniciaColicion=True
						
		
		plantaTodaX, plantaTodaY=cuadranteX_planta*display_width/4-planta.anchoFrame/2,cuadranteY_planta*display_height/2-planta.alto*1.3
		regaderaX,regaderaY=cuadranteX_regadera*display_width/4-regadera.anchoFrame/2*0.2,cuadranteY_regadera*display_height/2-regadera.alto*1.45

		
		gameDisplay.fill(white)

		if regaderaX>regaderaXactual:
			regaderaXactual+=velocRegadera
		if regaderaX<regaderaXactual:
			regaderaXactual-=velocRegadera
		if regaderaY>regaderaYactual:
			regaderaYactual+=velocRegadera
		if regaderaY<regaderaYactual:
			regaderaYactual-=velocRegadera

		if abejaIda : rayos.mostrar(plantaTodaX-100,plantaTodaY-130,rayos.frame,0)	
		if not flor_der.fin: regadera.mostrar(regaderaXactual,regaderaYactual,regadera.frame,False)
		planta.mostrar(plantaTodaX+10,plantaTodaY,planta.frame,False)
		tallo.mostrar(plantaTodaX,plantaTodaY+30,tallo.frame,False)
		flor_izq.mostrar(plantaTodaX+2,plantaTodaY+47,flor_izq.frame,False)
		flor_der.mostrar(plantaTodaX-10,plantaTodaY+34,flor_der.frame,False)
		roca.mostrar(rocaX[0]+10,rocaY[0],0,False)
		roca.mostrar(rocaX[1]+10,rocaY[0],0,False)
		roca.mostrar(rocaX[0]+10,rocaY[1],0,False)
		roca.mostrar(rocaX[1]+10,rocaY[1],0,False)
		gameDisplay.blit(txtEscape,(display_width/2-txtEscape.get_width()/2,display_height*.92))
		
        #Anima llegada de abeja
		if flor_der.fin:
			# Anima aleteo abeja
			if frameGeneral%3==0: # hago que sea mas lento el framerate de la planta
				if abeja.frame < abeja.cantFrames-1:
					abeja.frame +=1
				else:
					abeja.frame=1
			# Anima ida o vuelta de abeja
			if abejaIda:
				if abejaX<plantaTodaX+10:
					abejaX+=5
				else:
					abejaIda=False
					abejaIdaSND.stop()
					abejaVueltaSND.play()
				abeja.mostrar(abejaX,plantaTodaY+30,abeja.frame,False)
			if not abejaIda:
				if abejaX>-1200: #me paso un poco para que hacer una pausa
					abejaX-=20
				else:
					abeja.fin=True
				abeja.mostrar(abejaX,plantaTodaY+30,abeja.frame,True)
			

		
		pygame.display.update()
		clock.tick(30)

planta= Sprite_animado("img/sheet_planta.png",260,8)
tallo= Sprite_animado("img/sheet_tallo.png",260,16)
flor_izq= Sprite_animado("img/sheet_flor_izq.png",260,17)
flor_der= Sprite_animado("img/sheet_flor_der.png",260,17)
regadera= Sprite_animado("img/sheet_regadera.png",400,16)
roca=Sprite_animado("img/piedras.png",260,1)
rayos=Sprite_animado("img/sheet_rayos.png",500,7)
abeja=Sprite_animado("img/abeja.png",89,4)

rocaX= [1*display_width/4-roca.anchoFrame/2,3*display_width/4-roca.anchoFrame/2]
rocaY= [1*display_height/2-roca.alto*1.3, 2*display_height/2-roca.alto*1.3]


pygame.mixer.music.load('snd/musica.mp3') #music es streaming no esta en buffer como .sound
pygame.mixer.music.set_volume(0.2) #0 a 1
pygame.mixer.music.play(-1) #-1 para loop 
aguaSND = pygame.mixer.Sound("snd/agua.wav")
aguaSND.set_volume(0.5)
abejaIdaSND= pygame.mixer.Sound("snd/abeja_ida.wav")
abejaVueltaSND= pygame.mixer.Sound("snd/abeja_vuelta.wav")
plantaCreceSND= pygame.mixer.Sound("snd/planta_crece.wav")
magiaSND= pygame.mixer.Sound("snd/magia.wav")
 
#Posicion inicial de elementos
cuadranteX_planta=calcula_cuadrante()[0]
cuadranteY_planta=calcula_cuadrante()[1]
cuadranteX_regadera=1
cuadranteY_regadera=1
plantaTodaX, plantaTodaY=cuadranteX_planta*display_width/4-planta.anchoFrame/2,cuadranteY_planta*display_height/2-planta.alto*1.3
regaderaX,regaderaY=cuadranteX_regadera*display_width/4-regadera.anchoFrame/2*0.2,cuadranteY_regadera*display_height/2-regadera.alto*1.7

fuenteArial = pygame.font.SysFont('Arial', 15)
txtEscape = fuenteArial.render('presionar ESCAPE para salir', True, (200, 200, 200))

game_loop()
pygame.quit()
quit()