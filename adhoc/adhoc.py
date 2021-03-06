#!/usr/bin/python

import pygame
import math
import random
import time
import numpy as np

WIDTH, HEIGHT = 600, 500

def distance(p1, p2):
  x1, y1 = p1
  x2, y2 = p2
  return math.sqrt( (y2 - y1)**2 + (x2 - x1)**2)

class Matrix:
  
  def __init__(self, width = WIDTH, height = HEIGHT):
    self.window = np.zeros((WIDTH, HEIGHT+100))
    
  def reset(self):
    self.window = np.zeros((WIDTH, HEIGHT+100))

  def add_node(self, (pos)):
    self.window[pos] = 1

  def is_occupied(self, pos):
    #print pos, self.window.shape
    if pos[0] > 0 and pos[0] < WIDTH and pos[1] > 0 and pos[1] < HEIGHT:
      if self.window[pos] == 1:
        return True
      else:
        return False
    else:
      return False
  

matrix = Matrix()

class Node:

  def __init__(self, pos, color = (0, 0, 255), radius = 3):
    self.x, self.y = pos
    self.pos = pos
    self.color = color
    self.radius = radius
    self.connected = False
    self.life = random.randint(50, 100)
    #self.img = pygame.load_image('node.png')

  def draw(self, surface, color = (255, 255, 255)):
    circle = pygame.draw.circle(surface, color, self.pos, self.radius, 0)    
    #surface.blit(circle, self.pos)
    #surface.blit(self.img, self.pos)

  def move(self, p, q):
    if self.x + p > 0 and self.x + p < WIDTH and self.y + q > 0 and self.y + q < HEIGHT:
      new_pos = self.x + p, self.y + q
      if not matrix.is_occupied(new_pos):
        self.life -= 1
        self.x += p
        self.y += q
        self.pos = new_pos
      else:
        print "No puedo moverme"
    else:
      pass

class Connection:
  
  def __init__(self, node1, node2):
    node1.connected = True
    node2.connected = True
    self.nodes = [node1, node2]
    self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

  def draw_conn(self, surface):
    for node in self.nodes:
      color = (255, 255, 255)
      node.draw(surface, color = self.color)
      #pygame.draw.line(surface, color, self.node.pos, node.pos, 1)

  def add_node(self, node):
    if len(self.nodes) >= 3:
      return False #Ya existen 3 conexiones
    else:
      node.connected = True
      self.nodes.append(node)
      return True

  def move_nodes(self, mission):
    p, q = 0, 0
    #escoger movimiento vertical u horizontal
    if distance((self.nodes[0].x, 0), (mission[0], 0)) > distance((0, self.nodes[0].y), (0, mission[1])):
      if mission[0] > self.nodes[0].x:
        p, q = 1, 0
      elif mission[0] < self.nodes[0].x:
        p, q = -1, 0
    else:
      if mission[1] > self.nodes[0].y:
        p, q = 0, 1
      elif mission[1] < self.nodes[0].y:
        p, q = 0, -1

    for node in self.nodes: #moverse siguiendo al lider
      node.move(p, q)

#    for node in self.nodes:
#      if distance((node.x, 0), (mission[0], 0)) > distance((0, node.y), (0, mission[1])):
#        if mission[0] > node.x:
#          node.move(1, 0)
#        elif mission[0] < node.x:
#          node.move(-1, 0)
#      else:
#        if mission[1] > node.y:
#          node.move(0, 1)
#        elif mission[1] < node.y:
#          node.move(0, -1)
      
  def kill_node(self, node):
    tmp = self.nodes
    for i, n in enumerate(tmp):
      if n == node:
        tmp.pop(i)
        return True #se encontro y elimino
    return False #no se encontro

class Network:
  
  def __init__(self, n_nodes):
    self.n_nodes = n_nodes
    self.connections = []
    self.nodes = []
    n = 100
    for i in range(n_nodes):
      pos = random.randint(WIDTH/n, WIDTH - WIDTH/n), random.randint(HEIGHT/n, HEIGHT-HEIGHT/n)
      while matrix.is_occupied(pos): 
        pos = random.randint(WIDTH/n, WIDTH - WIDTH/n), random.randint(HEIGHT/n, HEIGHT-HEIGHT/n)
      matrix.window[pos] = 1
      node = Node(pos)
      self.add_connection(node)
    for node in self.nodes:
      if not node.connected:
        conn = self.add_connection(node)

  def draw_network(self, surface):
    for conn in self.connections:
      conn.draw_conn(surface)

  def add_connection(self, node):
    conn = None
    if len(self.nodes) < self.n_nodes:
      self.nodes.append(node)
      if len(self.nodes) > 1:
        n = random.randint(0, len(self.nodes)-1)
        m = random.randint(0, len(self.nodes)-1)
        while n == m:
          n = random.randint(0, len(self.nodes)-1)
          m = random.randint(0, len(self.nodes)-1)
        conn = Connection(self.nodes[n], self.nodes[m])
        self.connections.append(conn)
    else:
      n = random.randint(0, len(self.nodes)-1)
      m = random.randint(0, len(self.nodes)-1)
      while n == m:
        n = random.randint(0, len(self.nodes)-1)
        m = random.randint(0, len(self.nodes)-1)
      conn = Connection(self.nodes[n], self.nodes[m])
      self.connections.append(conn)
    return conn

#  def check_network(self):
#    tmp = self.nodes
#    for i, node in enumerate(tmp):  eliminar nodos muertos de la lista
#      if node.life <= 0: self.nodes.pop(i)
#    tmp = self.connections
#    for conn in self.connections:
#      
#      
#    for node in self.nodes:
#      if not node.connected:
#        conn = self.add_connection(node)
        
  
  
  def move_network(self, mission):
    #self.check_network() #checar si hay nodos sin bateria
    matrix.reset()
    for node in self.nodes:
      matrix.window[node.pos] = 1
    for conn in self.connections:
      conn.move_nodes(mission)
    
        
   

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))
#background = pygame.load_image()

adhoc = Network(50)

INICIO = time.time()
mission = random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1)
clock = pygame.time.Clock()
while True:  
  screen.blit(background, (0, 0))
  adhoc.move_network(mission)
  adhoc.draw_network(screen)
  pygame.draw.circle(screen, (0, 0, 255), mission, 5, 1) 
  pygame.display.update()
  clock.tick(5)
  FIN = time.time()
  t = FIN - INICIO
  if t > 5:
    prev_mission = mission
    INICIO = time.time()
    while distance(prev_mission, mission) < 300:
      mission = random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1)
  #time.sleep(0.5)























