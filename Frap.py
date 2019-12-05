from Screen_calc import *

def frap_process():
    Matrix = factor_matrix_init()
    Vector = coords_vector_init()
def main_calculation(Vector, Matrix):
    time = 0

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