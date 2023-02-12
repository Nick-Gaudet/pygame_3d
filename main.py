'''
Making 3d shapes using pygame, cool rotation and stuff, math is hard
By: Nick-Gaudet

'''

import pygame 
import random
import numpy as np

window = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()


projection_matrix = [[1, 0, 0], 
                     [0, 1, 0],
                     [0, 0, 0]]

def connection(a, b, point):
    pygame.draw.line(window, (255,255,255),
     (int(point[a][0]), int(point[a][1])), 
     (int(point[b][0]), int(point[b][1])), 1)
    
# if using torus r < R
R = 3
r = 5
num_theta = 30
num_phi = 30
theta = np.linspace(0, 2 * np.pi, num_theta)
phi = np.linspace(0, 2 * np.pi, num_phi)

# torus_points = []
# for i in range(num_theta):
#     for j in range(num_phi):
#         x = (R + r * np.cos(theta[i])) * np.cos(phi[j])
#         y = (R + r * np.cos(theta[i])) * np.sin(phi[j])
#         z = r * np.sin(theta[i])
#         torus_points.append([[x], [y], [z]])

sphere_points = []
for i in range(num_theta):
    for j in range(num_phi):
        x = r * np.sin(theta[i]) * np.cos(phi[j])
        y = r * np.sin(theta[i]) * np.sin(phi[j])
        z = r * np.cos(theta[i])
        sphere_points.append([[x], [y], [z]])
        
# The number of edges for each point
num_edges = 4

edges = []
for i in range(num_theta):
    for j in range(num_phi):
        current_index = i * num_phi + j
        for k in range(num_edges):

            # calculate the next index
            next_index = current_index + num_phi
            if next_index >= num_theta * num_phi:
                next_index -= num_theta * num_phi
            
            edges.append((current_index, next_index))

            # calculate the next index
            next_index = current_index + 1
            if (j + 1) % num_phi == 0:
                next_index -= num_phi
            
            edges.append((current_index, next_index))

# edges = [(0,1), (1,2), (2,3), (3,0), (4,5), (5,6), (6,7), (7,4), (0,4), (1,5), (2,6), (3,7)]

def rotateX(angle, point):
    rotation_matrix_X = [[1, 0, 0],
                         [0, np.cos(angle), -np.sin(angle)],
                         [0, np.sin(angle), np.cos(angle)]]
    return np.dot(rotation_matrix_X, point)

def rotateY(angle, point):
    rotation_matrix_Y = [[np.cos(angle), 0, np.sin(angle)],
                         [0, 1, 0],
                         [-np.sin(angle), 0, np.cos(angle)]]
    return np.dot(rotation_matrix_Y, point)

def rotateZ(angle, point):
    rotation_matrix_Z = [[np.cos(angle), -np.sin(angle), 0],
                         [np.sin(angle), np.cos(angle), 0],
                         [0, 0, 1]]
    return np.dot(rotation_matrix_Z, point)

angle = 0
while True:
    clock.tick(60)
    window.fill((0,0,0))
    angle += 0.01
    points = [0 for i in range(len(sphere_points))]
    i = 0
    for p in sphere_points:
        r_x = rotateX(angle, p)
        r_y = rotateY(angle, r_x)
        r_z = rotateZ(angle, r_y)
        # p2d = np.dot(projection_matrix, r_z)
        p2d = r_z
        x = int(p2d[0][0]*50+400)
        y = int(p2d[1][0]*50+400)
        points[i] = (x,y)
        i += 1
        pygame.draw.circle(window, (255,255,255), (x,y), 1) 
    
    for edge in edges:  
        connection(edge[0] , edge[1], points)   
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    pygame.display.update()
