import tkinter
from tkinter.filedialog import *
#from Screen_calc import *

physical_time = 0

time_step = None

window_width = 800

window_height = 800

def frap_method():
    print('1')
def figure_method():
    print('2')
def animation_method():
    print('3')

def main():
    global physical_time
    global displayed_time
    global speed_of_sound
    global frequency
    global height
    global width
    global plate

    print('Modelling started!')
    physical_time = 0

    root = tkinter.Tk()

    plate = tkinter.Canvas(root, width=window_width, height=window_height, bg="white")
    plate.pack(side=tkinter.LEFT)

    frame = tkinter.Frame(root)
    frame.pack(side=tkinter.RIGHT)

    speed_of_sound_label = Label(text = 'Скорость звука, м/с')
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

    root.mainloop()
    print('Modelling finished!')

if __name__ == "__main__":
    main()