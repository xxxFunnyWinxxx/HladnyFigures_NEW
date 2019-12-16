import tkinter
from tkinter.filedialog import *
from Screen_calc import main_calculation
from Classes import *

window_width = 600

window_height = 600


# mode = 1
def frap_method():
    start(1)


# mode = 2
def figure_method():
    start(2)


# mode = 3
def animation_method():
    start(3)


# mode = 4
def figure_search():
    start(4)


def start(mode):
    plate.delete(ALL)
    const = Constant(speed_of_sound.get(), height.get(), width.get(), float(frequency.get()))
    main_calculation(const, plate, mode)


def main():
    global speed_of_sound
    global frequency
    global height
    global width
    global plate

    print('Программа запущена')

    root = tkinter.Tk()
    root.title('Симуляция')

    plate = tkinter.Canvas(root, width=window_width, height=window_height, bg="white")
    plate.pack(side=tkinter.LEFT)

    frame = tkinter.Frame(root)
    frame.pack(side=tkinter.RIGHT)

    speed_of_sound_label = Label(text='Скорость звука, м/с')
    speed_of_sound_label.pack()

    speed_of_sound = tkinter.DoubleVar()
    speed_of_sound.set(1000)
    speed_of_sound_entry = tkinter.Entry(textvariable=speed_of_sound)
    speed_of_sound_entry.pack()

    frequency_label = Label(text='Частота, Гц')
    frequency_label.pack()

    frequency = tkinter.DoubleVar()
    frequency.set(1000)
    frequency = tkinter.Entry(textvariable=frequency)
    frequency.pack()

    height_label = Label(text='Высота, м')
    height_label.pack()

    height = tkinter.DoubleVar()
    height.set(0.3)
    height_entry = tkinter.Entry(textvariable=height)
    height_entry.pack()

    width_label = Label(text='Ширина, м')
    width_label.pack()

    width = tkinter.DoubleVar()
    width.set(0.3)
    width_entry = tkinter.Entry(textvariable=width)
    width_entry.pack()

    frap_method_button = tkinter.Button(text="Кадр", command=frap_method)
    frap_method_button.pack()
    figure_method_button = tkinter.Button(text="Фигура", command=figure_method)
    figure_method_button.pack()
    animation_method_button = tkinter.Button(text="Анимация", command=animation_method)
    animation_method_button.pack()
    figure_search_button = tkinter.Button(text="Поиск фигур", command=figure_search)
    figure_search_button.pack()

    root.mainloop()
    print('Работа завершена')


if __name__ == "__main__":
    main()