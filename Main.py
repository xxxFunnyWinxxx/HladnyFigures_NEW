import tkinter
from tkinter.filedialog import *
from Screen_calc import main_calculation
from Classes import *

window_width = 600

window_height = 600


# mode = 1
def frap_method():
    start(1)
    progress_bar['text'] = 'Кадр готов'


# mode = 2
def figure_method():
    start(2)
    progress_bar['text'] = 'Фигура готова'


# mode = 3
def animation_method():
    start(3)
    progress_bar['text'] = 'Анимация готова'


# mode = 4
def figure_search():
    progress_bar['text'] = 'Процесс поиска...'
    freq = start(4)
    freq = round(freq, 1)
    progress_bar['text'] = str(freq) + ' Гц'


# mode = 5
def energy_graph():
    start(5)
    progress_bar['text'] = 'График готов'


def start(mode):
    plate.delete(ALL)
    const = Constant(speed_of_sound.get(), height.get(), width.get(), float(frequency.get()))
    plate['width'] = 2 * const.len
    plate['height'] = 2 * const.hei
    main_calculation(const, plate, mode)
    return const.freq


def main():
    global speed_of_sound
    global frequency
    global height
    global width
    global plate
    global progress_bar

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
    energy_graph_button = tkinter.Button(text="График энергии", command=energy_graph)
    energy_graph_button.pack()

    progress_bar = Label(root, relief = SUNKEN, anchor = W, text = 'Программа запущена')
    progress_bar.pack(side = tkinter.BOTTOM)


    root.mainloop()
    print('Работа завершена')


if __name__ == "__main__":
    main()