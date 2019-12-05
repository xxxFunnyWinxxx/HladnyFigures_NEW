# coding: utf-8
# license: GPLv3

import tkinter
from tkinter.filedialog import *
from Screen import *

perform_execution = False
"""Флаг цикличности выполнения расчёта"""

physical_time = 0
"""Физическое время от начала расчёта.
Тип: float"""

displayed_time = None
"""Отображаемое на экране время.
Тип: переменная tkinter"""

time_step = None
"""Шаг по времени при моделировании.
Тип: float"""

def frap_method():
    print('1')
def figure_method():
    print('2')
def animation_method():
    print('3')

def main():
    """Главная функция главного модуля.
    Создаёт объекты графического дизайна библиотеки tkinter: окно, холст, фрейм с кнопками, кнопки.
    """
    global physical_time
    global displayed_time
    global time_step
    global time_speed
    global space
    global start_button

    print('Modelling started!')
    physical_time = 0

    root = tkinter.Tk()

    plate = tkinter.Canvas(root, width=window_width, height=window_height, bg="white")
    plate.pack(side=tkinter.LEFT)

    frame = tkinter.Frame(root)
    frame.pack(side=tkinter.RIGHT)

    speed_of_sound_label = Label(text = 'Скорость звука')
    speed_of_sound_label.pack()

    speed_of_sound = tkinter.DoubleVar()
    speed_of_sound.set(1000)
    speed_of_sound_entry = tkinter.Entry(frame, textvariable=speed_of_sound)
    speed_of_sound_entry.pack()

    height_label = Label(text='Высота, м')
    height_label.pack()

    height = tkinter.DoubleVar()
    height.set(0.3)
    height_entry = tkinter.Entry(frame, textvariable=speed_of_sound)
    height_entry.pack()

    height_label = Label(text='Ширина, м')
    height_label.pack()

    width = tkinter.DoubleVar()
    width.set(0.3)
    width_entry = tkinter.Entry(frame, textvariable=speed_of_sound)
    width_entry.pack()

    frap_method_button = tkinter.Button(frame, text="Кадр", command=frap_method)
    frap_method_button.pack()
    figure_method_button = tkinter.Button(frame, text="Фигура", command=figure_method)
    figure_method_button.pack()
    animation_method_button = tkinter.Button(frame, text="Анимация", command=animation_method)
    animation_method_button.pack()

    root.mainloop()
    print('Modelling finished!')

if __name__ == "__main__":
    main()