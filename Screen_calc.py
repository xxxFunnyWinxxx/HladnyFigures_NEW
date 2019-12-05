import scipy.sparse as sp
import scipy.sparse.linalg as lg
import numpy as np
import tkinter as tk


all_time = 1
dt = 0.000001

freq = 5000

lenght = 0.3 # метры
height = 0.4 # метры

quan = 100

h = min(lenght, height)/quan

len = int(lenght/h)
hei = int(height/h)

x_center = [int(quan/2),int(quan/2+1)]
y_center = [int(quan/2),int(quan/2+1)]

vec_lenght = (len+2)*(hei+2)

kappa = speed_of_sound*speed_of_sound

A = 2-4*kappa*dt*dt/(h*h)
B = kappa*dt*dt/(h*h)
C = -1
D = 1

# Пересчёт координат из матрицы в вектор идёт построчно слева направо
def vec_coords(x,y):
    n_in_vector = x*(len+2)+y
    return n_in_vector

def factor_matrix_init():
    diagonals = [[A]*vec_lenght + [0]*vec_lenght, [B]*(vec_lenght+1) + [0]*(vec_lenght-1),
                 [B]*(vec_lenght-1) + [0]*(vec_lenght+1), [B]*(vec_lenght+len+2) + [0]*(vec_lenght-len-2),
                 [B]*(vec_lenght-len-2) + [0]*(vec_lenght+len+2), [C]*2*vec_lenght, [D]*vec_lenght + [0]*vec_lenght]
    Matrix = sp.dia_matrix((diagonals, [0, 1, -1, len+2, -len-2, vec_lenght, -vec_lenght]), shape = (2*vec_lenght, 2*vec_lenght))
    return Matrix

def coords_vector_init():
    Vector = np.array(np.zeros(2*vec_lenght), dtype = float)
    return Vector

def main_calculation(Vector, Matrix):
    time = 0
    amplitude = 0.005
    M = lg.aslinearoperator(Matrix)
    # Ход времени
    for i in range(int(all_time/dt)):
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
    return Vector

def make_image(Vector):
    root = tk.Tk()
    root.geometry(str(2*len) + 'x' + str(2*hei))
    root.title("Симуляция")
    canv = tk.Canvas(root, width= 2*len, height= 2*hei, bg='white')
    canv.pack()
    amplitude = 0.005

    def rgb(rgb):
        return "#%02x%02x%02x" % rgb

    def color_calculation(h):
        if h >= 0:
            color = (255, round(255 * float(np.exp(-h / amplitude))), round(255 * float(np.exp(-h / amplitude))))
        else:
            color = (round(255 * float(np.exp(h / amplitude))), round(255 * float(np.exp(h / amplitude))), 255)
        return rgb(color)

    def create_board_image(canv, Vector, vec_lenght):
        for n in range(vec_lenght):
            i = 2*(n // (len+2) +1)
            j = 2*(n % (len+2) +1)
            canv.create_rectangle(i, j, i + 1, j + 1, outline=color_calculation(float(Vector[n])))
    print('end')
    create_board_image(canv, Vector, vec_lenght)
    root.mainloop()

Matrix = factor_matrix_init()
Vector = coords_vector_init()
Vector = main_calculation(Vector, Matrix)
make_image(Vector)