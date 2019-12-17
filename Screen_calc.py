import scipy.sparse as sp
import scipy.sparse.linalg as lg
import numpy as np
from PIL import Image, ImageDraw
import PIL
from glob import glob
import matplotlib.pyplot as plt


# ИНИЦИАЛИАЦИЯ
# Инициализация матрици коэфициентов
def factor_matrix_init(const):
    diagonals = [[const.A] * const.vec_lenght + [0] * const.vec_lenght,
                 [const.B] * (const.vec_lenght + 1) + [0] * (const.vec_lenght - 1),
                 [const.B] * (const.vec_lenght - 1) + [0] * (const.vec_lenght + 1),
                 [const.B] * (const.vec_lenght+const.len+2) + [0] * (const.vec_lenght - const.len - 2),
                 [const.B] * (const.vec_lenght-const.len-2) + [0] * (const.vec_lenght + const.len + 2),
                 [const.C] * 2 * const.vec_lenght, [const.D] * const.vec_lenght + [0] * const.vec_lenght]
    matrix = sp.dia_matrix((diagonals, [0, 1, -1, const.len + 2, - const.len - 2, const.vec_lenght, -const.vec_lenght]),
                           shape=(2 * const.vec_lenght, 2 * const.vec_lenght))
    return matrix


# Инициализация вектора значений
def coords_vector_init(const):
    vector = np.array(np.zeros(2*const.vec_lenght), dtype=float)
    return vector


# ПРОЦЕСС
def main_calculation(const, canv, mode):
    time = 0
    # РЕЖИМЫ ВХОД
    # для анимации
    image1 = PIL.Image.new("RGB", (2 * const.len, 2 * const.hei), (255, 255, 255))
    draw = ImageDraw.Draw(image1)
    # для фигур
    imvec = np.array(np.zeros(const.vec_lenght), dtype=float)
    # для графиков
    energy_mass = []
    time_mass = []
    # общее
    matrix = factor_matrix_init(const)
    vector = coords_vector_init(const)
    operator = lg.aslinearoperator(matrix)

    # Ход времени
    for m in range(int(const.all_time/const.dt)):
        time += const.dt
        # print(m)
        # ДЕЙСТВИЯ НАД СИСТЕМОЙ
        # Движение центральных плит
        for i in const.x_center:
            for j in const.y_center:
                vector[vec_coords(i, j, const)] = const.amplitude*np.sin(2 * np.pi * const.freq * time)

        # Итерация системы
        vector = operator.matvec(vector)

        # Выравнивание краевых плит
        vector[vec_coords(0, 0, const):vec_coords(0, const.len + 1, const)] = \
            vector[vec_coords(1, 0, const):vec_coords(1, const.len+1, const)]
        vector[vec_coords(const.hei+1, 0, const):vec_coords(const.hei+1, const.len+1, const)] = \
            vector[vec_coords(const.hei, 0, const):vec_coords(const.hei, const.len+1, const)]
        for i in range(const.hei + 2):
            vector[vec_coords(i, 0, const)] = vector[vec_coords(i, 1, const)]
            vector[vec_coords(i, const. len + 1, const)] = vector[vec_coords(i, const.len, const)]

        # РЕЖИМЫ ЦЕНТР
        if (mode == 2 or mode == 4) and time > (0.9*const.all_time):
            for i in range(const.vec_lenght):
                if abs(vector[i]) <= 10 ** (-5):
                    imvec[i] += 1

        elif mode == 3 and m % 2 == 0:
            for n in range(const.vec_lenght):
                j = 2 * (n // (const.len + 2) + 1)
                i = 2 * (n % (const.len + 2) + 1)
                draw.rectangle([i, j, i + 1, j + 1], outline=color_calculation(float(vector[n]), const))
            image1.save('Fraps/' + '00000'[:-len(str(int(m)))] + str(int(m)) + '.png')
        elif mode == 5:
            cut1 = vector[0:const.vec_lenght]
            cut2 = vector[const.vec_lenght: 2*const.vec_lenght + 1]
            vec_energy = cut1 - cut2
            vec_energy = vec_energy*vec_energy
            energy = np.sum(vec_energy)
            energy_mass.append(energy)
            time_mass.append(time)
    # РЕЖИМЫ ВЫХОД
    if mode == 1:
        for n in range(const.vec_lenght):
            j = 2 * (n // (const.len + 2) + 1)
            i = 2 * (n % (const.len + 2) + 1)
            canv.create_rectangle(i, j, i + 1, j + 1, outline=color_calculation(float(vector[n]), const))
        print('Кадр готов')
    elif mode == 2:
        show_figure(canv, const, imvec)
        print('Фигура Хладни готова')
    elif mode == 3:
        frames = roll()
        frames[0].save('Animation.gif', format='GIF', append_images=frames, save_all=True, duration=100, Loop=0)
        print('Анимация готова')
    elif mode == 4:
        const.n2 = grad_count(imvec, const)
        grad_step(const.n1, const.n2, const.freq, const)
        const.n1 = const.n2
        print(const.freq)
        if const.learning_step < const.learning_steps_amount:
            main_calculation(const, canv, mode)
        else:
            print('Фигура найдена')
            show_figure(canv, const, imvec)
    elif mode == 5:
        time_mass = time_mass
        energy_mass = energy_mass / max(energy_mass)
        plt.plot(time_mass, energy_mass)
        plt.title("Зависимость кинетической энергии системы от времени")
        plt.xlabel("Время, мc")
        plt.ylabel("Кинетическая энергия")
        plt.show()

# ФУНКЦИИ
# Пересчёт координат из матрицы в вектор (идёт построчно слева направо)
def vec_coords(x, y, const):
    n_in_vector = x * (const.len+2) + y
    return n_in_vector


def rgb(colors_kort):
    return "#%02x%02x%02x" % colors_kort


def color_calculation(h, const):
    if h >= 0:
        color = (255, round(255 * float(np.exp(-h / const.amplitude))), 
                 round(255 * float(np.exp(-h / const.amplitude))))
    else:
        color = (round(255 * float(np.exp(h / const.amplitude))), 
                 round(255 * float(np.exp(h / const.amplitude))), 255)
    return rgb(color)


def grey_calculation(n, const):
    color = (int(255*np.exp(-n/const.lim)), int(255*np.exp(-n/const.lim)), int(255*np.exp(-n/const.lim)))
    return rgb(color)


def roll():
    frames = []
    for i in glob('Fraps/*.png'):
        new_frame = Image.open(i)
        frames.append(new_frame)
    return frames


def grad_count(imvec, const):
    summ = 0
    for n in range(const.vec_lenght):
        if imvec[n] >= const.lim:
            summ += imvec[n]
    return summ


def grad_step(n1, n2, freq, const):
    new_freq = freq + const.learning_speed
    const.learning_speed = const.alpha * const.learning_speed - const.learning_rate * (n1 - n2)  # /(new_freq - freq)
    const.learning_step += 1
    const.freq = new_freq
    return new_freq


def show_figure(canv, const, imvec):
    for n in range(const.vec_lenght):
        j = 2 * (n // (const.len + 2) + 1)
        i = 2 * (n % (const.len + 2) + 1)
        canv.create_rectangle(i, j, i + 1, j + 1, outline=grey_calculation(imvec[n], const))