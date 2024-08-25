import numpy as np
import math
import os
import time

A = 0
B = 0
C = 0

cube_width = 20
width, height = 160, 44
background_ascii_code = ' '
distance_from_cam = 100
horizontal_offset = 0
K1 = 40
increment_speed = 0.6

buffer = np.full((height, width), background_ascii_code)
z_buffer = np.zeros((height, width))

def calculate_x(i, j, k):
    return j * math.sin(A) * math.sin(B) * math.cos(C) - k * math.cos(A) * math.sin(B) * math.cos(C) + \
           j * math.cos(A) * math.sin(C) + k * math.sin(A) * math.sin(C) + i * math.cos(B) * math.cos(C)

def calculate_y(i, j, k):
    return j * math.cos(A) * math.cos(C) + k * math.sin(A) * math.cos(C) - \
           j * math.sin(A) * math.sin(B) * math.sin(C) + k * math.cos(A) * math.sin(B) * math.sin(C) - \
           i * math.cos(B) * math.sin(C)

def calculate_z(i, j, k):
    return k * math.cos(A) * math.cos(B) - j * math.sin(A) * math.cos(B) + i * math.sin(B)

def calculate_for_surface(cube_x, cube_y, cube_z, char):
    global buffer, z_buffer, horizontal_offset
    x = calculate_x(cube_x, cube_y, cube_z)
    y = calculate_y(cube_x, cube_y, cube_z)
    z = calculate_z(cube_x, cube_y, cube_z) + distance_from_cam

    ooz = 1 / z if z != 0 else float('inf')

    xp = int(width / 2 + horizontal_offset + K1 * ooz * x * 2)
    yp = int(height / 2 + K1 * ooz * y)

    if 0 <= xp < width and 0 <= yp < height:
        if ooz > z_buffer[yp, xp]:
            z_buffer[yp, xp] = ooz
            buffer[yp, xp] = char

def main():
    global A, B

    while True:
        buffer.fill(background_ascii_code)
        z_buffer.fill(0)
        cube_width = 20
        horizontal_offset = -2 * cube_width

        for cube_x in np.arange(-cube_width, cube_width, increment_speed):
            for cube_y in np.arange(-cube_width, cube_width, increment_speed):
                calculate_for_surface(cube_x, cube_y, -cube_width, '@')
                calculate_for_surface(cube_width, cube_y, cube_x, '$')
                calculate_for_surface(-cube_width, cube_y, -cube_x, '~')
                calculate_for_surface(-cube_x, cube_y, cube_width, '#')
                calculate_for_surface(cube_x, -cube_width, -cube_y, ';')
                calculate_for_surface(cube_x, cube_width, cube_y, '+')

        os.system('cls' if os.name == 'nt' else 'clear')
        for row in buffer:
            print(''.join(row))

        A += 0.15
        B += 0.15

if __name__ == "__main__":
    main()
