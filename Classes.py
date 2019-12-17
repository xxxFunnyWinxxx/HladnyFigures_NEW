class Constant:
    def __init__(self, speed_of_sound, height, width, frequency):

        iterations = 1000   # Число итераций

        dt0 = 0.000001
        speed0 = 800
        self.dt = round(speed0*dt0/speed_of_sound, 8)  # Шаг по времени
        self.all_time = iterations*self.dt  # Время процесса

        self.lim = 0.004*iterations

        self.freq = frequency

        quan = 120  # Число симулируемых плиток вдоль оси

        self.amplitude = 0.005  # Амплитуда колебаний центральных плит

        h = min(width, height) / quan

        self.len = int(width / h)
        self.hei = int(height / h)

        self.x_center = [int(quan / 2), int(quan / 2 + 1)]
        self.y_center = [int(quan / 2), int(quan / 2 + 1)]

        self.vec_lenght = (self.len + 2) * (self.hei + 2)
        kappa = speed_of_sound * speed_of_sound
        self.A = 2 - 4 * kappa * self.dt * self.dt / (h * h)
        self.B = kappa * self.dt * self.dt / (h * h)
        self.C = -1
        self.D = 1

        self.n1 = 0
        self.n2 = 0
        self.learning_speed = 0.1
        self.learning_rate = 0.01
        self.alpha = 0.9
        self.learning_steps_amount = 40
        self.learning_step = 0