import scipy.sparse as sp
import scipy.sparse.linalg as lg
import numpy as np
from PIL import Image, ImageDraw
import PIL
from Classes import *

# Указание и вычисление констант
#def constant_init(speed_of_sound, height, width, frequency):
#    global all_time, dt, freq
#    global amplitude, len, hei, const.vec_lenght
#    global x_center, y_center
#    global A, B, C, D
#
#    all_time = 0.1    # Время процесса
#    dt = 0.000001   # Шаг по времени
#
#    freq = frequency
#
#    quan = 100      # Число симулируемых плиток вдоль оси
#
#    amplitude = 0.005   # Амплитуда колебаний центральных плит
#
#    h = min(width, height)/quan
#
#    len = int(width/h)
#    hei = int(height/h)
#
#    x_center = [int(quan/2),int(quan/2+1)]
#    y_center = [int(quan/2),int(quan/2+1)]
#
#    const.vec_lenght = (len+2)*(hei+2)
#    kappa = speed_of_sound * speed_of_sound
#    A = 2-4*kappa*dt*dt/(h*h)
#    B = kappa*dt*dt/(h*h)
#    C = -1
#    D = 1

# Пересчёт координат из матрицы в вектор (идёт построчно слева направо)
def vec_coords(x,y,const):
    n_in_vector = x*(const.len+2)+y
    return n_in_vector

# Инициализация матрици коэфициентов
def factor_matrix_init(const):
    diagonals = [[const.A]*const.vec_lenght + [0]*const.vec_lenght, [const.B]*(const.vec_lenght+1) + [0]*(const.vec_lenght-1),
                 [const.B]*(const.vec_lenght-1) + [0]*(const.vec_lenght+1), [const.B]*(const.vec_lenght+const.len+2) + [0]*(const.vec_lenght-const.len-2),
                 [const.B]*(const.vec_lenght-const.len-2) + [0]*(const.vec_lenght+const.len+2), [const.C]*2*const.vec_lenght, [const.D]*const.vec_lenght + [0]*const.vec_lenght]
    Matrix = sp.dia_matrix((diagonals, [0, 1, -1, const.len+2, -const.len-2, const.vec_lenght, -const.vec_lenght]), shape = (2*const.vec_lenght, 2*const.vec_lenght))
    return Matrix

# Инициализация вектора значений
def coords_vector_init(const):
    Vector = np.array(np.zeros(2*const.vec_lenght), dtype = float)
    return Vector

# Шаг процесса
def main_calculation(const, canv, mode):
    time = 0
    if mode == 2:
        Imvec = np.array(np.zeros(const.vec_lenght), dtype=float)
    elif mode == 3:
        image1 = PIL.Image.new("RGB", (2 * const.len, 2 * const.hei), (255, 255, 255))
        draw = ImageDraw.Draw(image1)
    Matrix = factor_matrix_init(const)
    Vector = coords_vector_init(const)
    M = lg.aslinearoperator(Matrix)
    # Ход времени
    for m in range(int(const.all_time/const.dt)):
        time += const.dt

        # Движение центральных плит
        for i in const.x_center:
            for j in const.y_center:
                Vector[vec_coords(i,j,const)] = const.amplitude*np.sin(2*np.pi*const.freq*time)

        # Итерация системы
        Vector = M.matvec(Vector)

        # Выравнивание краевых плит
        Vector[vec_coords(0,0,const):vec_coords(0,const.len+1,const)] = Vector[vec_coords(1,0,const):vec_coords(1,const.len+1,const)]
        Vector[vec_coords(const.hei+1, 0,const):vec_coords(const.hei+1, const.len+1,const)] = Vector[vec_coords(const.hei, 0,const):vec_coords(const.hei, const.len+1,const)]
        for i in range(const.hei+2):
            Vector[vec_coords(i, 0,const)] = Vector[vec_coords(i, 1,const)]
            Vector[vec_coords(i,const. len+1,const)] = Vector[vec_coords(i, const.len,const)]
        print(m)
        if mode == 2 and time > (0.9*const.all_time):
            for i in range(const.vec_lenght):
                #print(Vector[i])
                if abs(Vector[i]) <= 10 **(-5):
                    Imvec[i] += 1

        elif mode == 3 and m % 10 == 0:
            for n in range(const.vec_lenght):
                j = 2 * (n // (const.len + 2) + 1)
                i = 2 * (n % (const.len + 2) + 1)
                draw.rectangle([i, j, i + 1, j + 1], outline=color_calculation(float(Vector[n])))
            image1.save('plt/' + str(int(m / 100)) + '.png')
    if mode == 1:
        mode_1(canv, Vector, const)
    elif mode == 2:
        mode_2(canv, Imvec, const)
    elif mode == 3:
        mode_3(const)


def rgb(rgb):
    return "#%02x%02x%02x" % rgb

def color_calculation(h, const):
    if h >= 0:
        color = (255, round(255 * float(np.exp(-h / const.amplitude))), round(255 * float(np.exp(-h / const.amplitude))))
    else:
        color = (round(255 * float(np.exp(h / const.amplitude))), round(255 * float(np.exp(h / const.amplitude))), 255)
    return rgb(color)

def mode_1(canv, Vector, const):
    for n in range(const.vec_lenght):
        j = 2*(n // (const.len+2) +1)
        i = 2*(n % (const.len+2) +1)
        canv.create_rectangle(i, j, i + 1, j + 1, outline=color_calculation(float(Vector[n]),const))

def mode_2(canv, Imvec, const):
    for n in range(const.vec_lenght):
        if Imvec[n] > 80:
            i = 2 * (n // (const.len + 2) + 1)
            j = 2 * (n % (const.len + 2) + 1)
            canv.create_rectangle(i, j, i + 1, j + 1, outline='BLACK')

def mode_3(const):
    def roll():
        frames = []
        for i in range(int(const.all_time/(const.dt*10))):
            new_frame = Image.open('plt/' + str(i) + '.png')
            frames.append(new_frame)
        return frames
    frames = roll()
    frames[0].save('png_to_gif.gif', format='GIF', append_images=frames[0:int(const.all_time/(const.dt*10))], save_all=True, duration=100, Loop=0)
    print('Анимация готова')