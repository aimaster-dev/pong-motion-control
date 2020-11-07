import pygame
import tensorflow as tf
import cv2
from src.utils import load_graph, detect_hands, predict
import numpy as np
GREEN = (0, 255, 0)
RED = (0, 0, 255)
ORANGE = (0,128,255)
WIDTH = 1200
HEIGHT = 600
BORDER = 20
FRAMERATE=30
fgcolor = pygame.Color("white")
bgcolor = pygame.Color("black")
tf.compat.v1.flags.DEFINE_integer("width", 640, "Screen width")
tf.compat.v1.flags.DEFINE_integer("height", 480, "Screen height")
tf.compat.v1.flags.DEFINE_float("threshold", 0.6, "Threshold for score")
tf.compat.v1.flags.DEFINE_float("alpha", 0.3, "Transparent level")
tf.compat.v1.flags.DEFINE_string("pre_trained_model_path", "src/pretrained_model.pb", "Path to pre-trained model")
FLAGS = tf.compat.v1.flags.FLAGS
graph, sess = load_graph(FLAGS.pre_trained_model_path)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, FLAGS.width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FLAGS.height)
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
print("PRESS SPACE TO START PRESS ASCAPE TO QUIT")
class Ball:
	RADIUS = 20
	VELOCITY = 25
	def __init__(self, x,y,vx,vy):
		self.x = x
		self.y = y
		self.vx=vx
		self.vy=vy
	def show(self,colour):
		pygame.draw.circle(screen,colour,(self.x,self.y),Ball.RADIUS)
	def update(self):
		newx=self.x +self.vx
		newy=self.y +self.vy
		if newy<BORDER+Ball.RADIUS or newy>HEIGHT-BORDER-Ball.RADIUS:
			self.vy= - self.vy
		elif newx+Ball.RADIUS>WIDTH-Paddle.WIDTH and abs(newy-paddle1.y)<Paddle.HEIGHT//2:
			self.vx= - self.vx
		elif newx-Ball.RADIUS<Paddle.WIDTH and abs(newy-paddle2.y)<Paddle.HEIGHT//2:
			self.vx= - self.vx
		else:
			self.show(bgcolor)
			self.x= newx
			self.y= newy
			self.show(fgcolor)
class Paddle:
	WIDTH = 20
	HEIGHT = 100
	STEP = 20
	def __init__(self, y ,id):
		self.y = y
		self.id = id
	def show(self,colour):
		if self.id==1:
			pygame.draw.rect(screen,colour,pygame.Rect(WIDTH-self.WIDTH,self.y-self.HEIGHT//2,self.WIDTH,self.HEIGHT))
		if self.id==2:
			pygame.draw.rect(screen,colour,pygame.Rect(0,self.y-self.HEIGHT//2,self.WIDTH,self.HEIGHT))
	@staticmethod
	def update():
		paddle1.show(bgcolor)
		paddle2.show(bgcolor)
		if len(results1) == 1 :
			x_min, x_max, y_min, y_max, category = results1[0]
			x = int((x_min + x_max) / 2) + int(FLAGS.width / 2)
			y = int((y_min + y_max) / 2)
			cv2.circle(frame, (x, y), 5, RED, -1)
			if x >=  2 * FLAGS.width / 3 and y <= FLAGS.height / 2 and category == "Open" :
				paddle1.y -= Paddle.STEP
			elif x >= 2 * FLAGS.width / 3 and y >= FLAGS.height / 2 and category == "Open" :
				paddle1.y += Paddle.STEP
		if len(results2) == 1 :
			x_min, x_max, y_min, y_max, category = results2[0]
			x = int((x_min + x_max) / 2)
			y = int((y_min + y_max) / 2)
			cv2.circle(frame, (x, y), 5, RED, -1)
			if x <= FLAGS.width / 3 and y <= FLAGS.height / 2 and category == "Open" :
				paddle2.y -= Paddle.STEP
			elif x <= FLAGS.width / 3 and y >= FLAGS.height / 2 and category == "Open" :
				paddle2.y += Paddle.STEP
		if paddle1.y < BORDER + Paddle.HEIGHT//2:
			paddle1.y= BORDER + Paddle.HEIGHT//2
		if paddle1.y +  Paddle.HEIGHT//2 > HEIGHT - BORDER:
			paddle1.y = HEIGHT - BORDER - Paddle.HEIGHT//2
		if paddle2.y < BORDER + Paddle.HEIGHT//2:
			paddle2.y= BORDER + Paddle.HEIGHT//2
		if paddle2.y +  Paddle.HEIGHT//2 > HEIGHT - BORDER:
			paddle2.y = HEIGHT - BORDER - Paddle.HEIGHT//2
		paddle1.show(fgcolor)
		paddle2.show(fgcolor)
while True:
	ballplay=Ball((WIDTH-Ball.RADIUS)//2,HEIGHT//2,-Ball.VELOCITY,-Ball.VELOCITY)
	paddle1=Paddle(HEIGHT//2,1)
	paddle2=Paddle(HEIGHT//2,2)
	clock=pygame.time.Clock()
	screen.fill(bgcolor)
	pygame.draw.rect(screen,fgcolor,pygame.Rect(0,0,WIDTH,BORDER))
	pygame.draw.rect(screen,fgcolor,pygame.Rect(0,HEIGHT-BORDER,WIDTH,BORDER))
	ballplay.show(fgcolor)
	paddle1.show(fgcolor)
	paddle2.show(fgcolor)
	pygame.display.flip()
	e=pygame.event.poll()
	if e.type == pygame.QUIT:
		pygame.quit()
		cap.release()
		cv2.destroyAllWindows()
		break
	if e.type == pygame.KEYDOWN:
		if e.key == pygame.K_ESCAPE:
			pygame.quit()
			cap.release()
			cv2.destroyAllWindows()
			break
	if e.type == pygame.KEYDOWN:
		if e.key == pygame.K_SPACE:
			while True:
				ret, frame = cap.read()
				frame = cv2.flip(frame, 1)
				frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
				frame1=frame.copy()
				frame2=frame.copy()
				frame1[:,:2*int(FLAGS.width / 3)]=0
				frame2[:,int(FLAGS.width / 3):]=0
				boxes1, scores1, classes1 = detect_hands(frame1, graph, sess)
				boxes2, scores2, classes2 = detect_hands(frame2, graph, sess)
				frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
				results1 = predict(boxes1, scores1, classes1, FLAGS.threshold, FLAGS.width/3, FLAGS.height)
				results2 = predict(boxes2, scores2, classes2, FLAGS.threshold, FLAGS.width/3, FLAGS.height)
				overlay = frame.copy()
				cv2.rectangle(overlay, (0, 0), (int(FLAGS.width / 3), int(FLAGS.height/2)), ORANGE, -1)
				cv2.rectangle(overlay, (0, int(FLAGS.height/2)), (int(FLAGS.width / 3), FLAGS.height), GREEN, -1)
				cv2.rectangle(overlay, (int(2 * FLAGS.width / 3), 0), (FLAGS.width, int(FLAGS.height/2)), ORANGE, -1)
				cv2.rectangle(overlay, (int(2 * FLAGS.width / 3), int(FLAGS.height/2)), (FLAGS.width, FLAGS.height), GREEN, -1)
				cv2.addWeighted(overlay, FLAGS.alpha, frame, 1 - FLAGS.alpha, 0, frame)
				if e.type == pygame.QUIT:
					pygame.quit()
					cap.release()
					cv2.destroyAllWindows()
					break
				clock.tick(FRAMERATE)
				pygame.display.flip()
				ballplay.update()
				if ballplay.x > WIDTH:
					cv2.destroyAllWindows()
					break
				if ballplay.x < 0:
					cv2.destroyAllWindows()
					break
				Paddle.update()
				cv2.imshow('Detection', np.array(frame, dtype = np.uint8 ))
				if cv2.waitKey(1) & 0xFF == ord('q'):
					cv2.destroyAllWindows()
					break