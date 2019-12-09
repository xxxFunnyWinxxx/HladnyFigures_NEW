class constant:
    def __init__(self, speed_of_sound, height, width, frequency):

        self.all_time = 0.01  # Время процесса
        self.dt = 0.000001  # Шаг по времени

        self.freq = frequency

        quan = 100  # Число симулируемых плиток вдоль оси

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


