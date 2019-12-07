import scipy.sparse as sp
import scipy.sparse.linalg as lg
import numpy as np
import tkinter as tk
from PIL import Image, ImageDraw
import PIL

# Указание и вычисление констант
def constant_init(speed_of_sound, height, width, frequency):
    global all_time, dt, freq
    global amplitude, len, hei, vec_lenght
    global x_center, y_center
    global A, B, C, D

    all_time = 0.01    # Время процесса
    dt = 0.000001   # Шаг по времени

    freq = frequency

    quan = 100      # Число симулируемых плиток вдоль оси

    amplitude = 0.005   # Амплитуда колебаний центральных плит

    h = min(width, height)/quan

    len = int(width/h)
    hei = int(height/h)

    x_center = [int(quan/2),int(quan/2+1)]
    y_center = [int(quan/2),int(quan/2+1)]

    vec_lenght = (len+2)*(hei+2)
    kappa = speed_of_sound * speed_of_sound
    A = 2-4*kappa*dt*dt/(h*h)
    B = kappa*dt*dt/(h*h)
    C = -1
    D = 1

# Пересчёт координат из матрицы в вектор (идёт построчно слева направо)
def vec_coords(x,y):
    n_in_vector = x*(len+2)+y
    return n_in_vector

# Инициализация матрици коэфициентов
def factor_matrix_init():
    diagonals = [[A]*vec_lenght + [0]*vec_lenght, [B]*(vec_lenght+1) + [0]*(vec_lenght-1),
                 [B]*(vec_lenght-1) + [0]*(vec_lenght+1), [B]*(vec_lenght+len+2) + [0]*(vec_lenght-len-2),
                 [B]*(vec_lenght-len-2) + [0]*(vec_lenght+len+2), [C]*2*vec_lenght, [D]*vec_lenght + [0]*vec_lenght]
    Matrix = sp.dia_matrix((diagonals, [0, 1, -1, len+2, -len-2, vec_lenght, -vec_lenght]), shape = (2*vec_lenght, 2*vec_lenght))
    return Matrix

# Инициализация вектора значений
def coords_vector_init():
    Vector = np.array(np.zeros(2*vec_lenght), dtype = float)
    return Vector

# Шаг процесса
def main_calculation(speed_of_sound, height, width, frequency, mode, canv):
    constant_init(speed_of_sound, height, width, frequency)
    time = 0
    frames = []
    image1 = PIL.Image.new("RGB", (2 * len, 2 * hei), (255, 255, 255))
    draw = ImageDraw.Draw(image1)
    Matrix = factor_matrix_init()
    Vector = coords_vector_init()
    M = lg.aslinearoperator(Matrix)
    # Ход времени
    for m in range(int(all_time/dt)):
        time += dt

        # Движение центральных плит
        for i in x_center:
            for j in y_center:
                Vector[vec_coords(i,j)] = amplitude*np.sin(2*np.pi*freq*time)

        # Итерация системы
        Vector = M.matvec(Vector)

        # Выравнивание краевых плит
        Vector[vec_coords(0,0):vec_coords(0,len+1)] = Vector[vec_coords(1,0):vec_coords(1,len+1)]
        Vector[vec_coords(hei+1, 0):vec_coords(hei+1, len+1)] = Vector[vec_coords(hei, 0):vec_coords(hei, len+1)]
        for i in range(hei+2):
            Vector[vec_coords(i, 0)] = Vector[vec_coords(i, 1)]
            Vector[vec_coords(i, len+1)] = Vector[vec_coords(i, len)]

        if mode == 3 and m % 10 == 0:
            for n in range(vec_lenght):
                j = 2 * (n // (len + 2) + 1)
                i = 2 * (n % (len + 2) + 1)
                draw.rectangle([i, j, i + 1, j + 1], outline=color_calculation(float(Vector[n])))
            frames.append(image1)
    if mode == 1:
        mode_1(canv, Vector)
    if mode == 3:
        frames[0].save('png_to_gif.gif', format='GIF', append_images=frames[0:len(frames)], save_all=True, duration=50, Loop=0)

def rgb(rgb):
    return "#%02x%02x%02x" % rgb

def color_calculation(h):
    if h >= 0:
        color = (255, round(255 * float(np.exp(-h / amplitude))), round(255 * float(np.exp(-h / amplitude))))
    else:
        color = (round(255 * float(np.exp(h / amplitude))), round(255 * float(np.exp(h / amplitude))), 255)
    return rgb(color)

def mode_1(canv, Vector):
    for n in range(vec_lenght):
        i = 2*(n // (len+2) +1)
        j = 2*(n % (len+2) +1)
        canv.create_rectangle(i, j, i + 1, j + 1, outline=color_calculation(float(Vector[n])))



