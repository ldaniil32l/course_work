# Автор: Попов Даниил
# Группа 121-Мко
from math import factorial


# Функция произведения матриц (для поиска степеней матриц)
def multi_matrix(A, B):
    multi_AB = []
    for i in range(len(A)):
        multi_row = []
        for j in range(len(A)):
            multi_row.append(0)
        multi_AB.append(multi_row)
    for i in range(len(A)):
        for j in range(len(A)):
            for k in range(len(A)):
                multi_AB[i][j] += A[i][k] * B[k][j]
    return multi_AB


# Функция умножения матрицы на число
def multi_matrix_number(A, k):
    for i in range(len(A)):
        for j in range(len(A)):
            A[i][j] = A[i][j] * k
    return A


# Функция сложения матриц
def sum_matrix(A, B):
    for i in range(len(A)):
        for j in range(len(A)):
            A[i][j] += B[i][j]
    return A


# Функция нахождения коэффициентов p характеристического многочлена
def coefficients_p(A):
    p = []
    s = []
    first_degree_A = A
    for i in range(len(A)):
        s.append(trace_matrix(first_degree_A))
        first_degree_A = multi_matrix(first_degree_A, A)
        if i == 0:
            p.append(s[i])
        else:
            p.append(s[i])
            k = i - 1
            for j in range(i):
                p[i] -= p[j] * s[k]
                k -= 1
            p[i] /= (i + 1)
    return p


# Функция поиска следа матрицы
def trace_matrix(A):
    tr = 0
    for i in range(len(A)):
        tr += A[i][i]
    return tr


# Функция поиска переменной B из формулы (18)
def B_in_kappa (g, n, p):
    if g >= 0 and g <= (n - 2):
        return 0
    elif g == (n - 1):
        return 1
    elif g >= n:
        b_sum = 0
        for l in range(1, n):
            b_sum += p[l - 1] * B_in_kappa(g - l, n, p)
        return b_sum
    else:
        return "ERROR"


# Функция поиска переменной каппа из формулы (17)
def search_for_kappa (index, n, Np, p):
    kappa =  1 / factorial(index)
    for g in range(index):
        temp_p = p[n - index + g - 1]
        for j in range(n, (n + Np)):
            temp_sum = B_in_kappa(j - 1 - g, n, p) / factorial(j)
        kappa += temp_p * temp_sum
    return kappa


# Основная часть программы

# Данные из задачи 10
Np = 11
n = 6
Wd = [
    [0, 11.38, 0, complex(0, -5.60), 0, 0],
    [-5.32, 0, -5.97, 0, 0, complex(0, -1.53)],
    [0, 0, 0, complex(0, -4.79), 11.38, 0],
    [-1.53, 0, complex(0, -1.28), 0, 0, 3.32],
    [-5.97, 0, complex(0, -4.06), 0, 0, complex(0, -1.28)],
    [0, complex(0, -0.04), 0, -16.18, complex(0, -4.70), 0]
]

print("Task 10. Selected action.\n1) Enter your details\n2) Use data from the issue")
while True:
    choice = input("enter 1 or 2: ")
    if choice == "1":
        n = int(input("Enter the order of the Wd matrix "))
        Wd = []
        for i in range(n):
            Wd_row = []
            for j in range(n):
                print("Введите [", i, ",", j, "] элемент ")
                Wd_row.append(complex(input()))
            Wd.append(Wd_row)
        for i in range(n):
            for j in range(n):
                print(Wd[i][j], end="\t")
            print()
        Np = int(input("Enter the number Np\t"))
        break
    if choice == "2":
        break

# Теорема
# Поиск максимального элемента матрицы Wd
maxWd = 0
for i in range(n):
    for j in range(n):
        if abs(Wd[i][j]) >= abs(maxWd):
            maxWd = Wd[i][j]

# Поиск m
m = 2
count_j = 1
while (True):
    temp_beta = abs(maxWd) * (n + 4) / 2 / m
    if temp_beta < 1:
        print("The minimum possible m is", m, ".")
        while True:
            choice = input( "If you are satisfied with this value, enter Y; if not, enter N: " )
            if choice == "Y" or choice == "y":
                break
            if choice == "N" or choice == "n":
                m *= 2
                count_j += 1
                if abs(maxWd) * (n + 4) / 2 / m < 1:
                    print("The possible m is", m, ".")
        break
    else:
        m *= 2
        count_j += 1

# Полиномиальная аппроксимация

A = []
for i in range(n):
    temp_row = []
    for j in range(n):
        temp_row.append(Wd[i][j] / m)
    A.append(temp_row)

p = coefficients_p(A)

first_degree_A = A
for i in range(n):
    if i == 0:
        identity_matrix = []
        for l in range(len(A)):
            identity_row = []
            for m in range(len(A)):
                if l == m:
                    identity_row.append(1)
                else:
                    identity_row.append(0)
            identity_matrix.append(identity_row)
        exp_A = multi_matrix_number(identity_matrix, search_for_kappa(i, n, Np, p))
    else:
        exp_A = sum_matrix(exp_A, multi_matrix_number(A, search_for_kappa(i, n, Np, p)))
        A = multi_matrix(A, first_degree_A)

# Возведение exp_A в степень m
for i in range(count_j):
    exp_A = multi_matrix(exp_A, exp_A)

# Вывод элементов матрицы Wd
exp_Wd = exp_A
print("Exponent of the Wd matrix:")
for i in range(n):
    for j in range(n):
        print ("%.3f+%.3fj" % (exp_Wd[i][j].real, exp_Wd[i][j].imag), end="  ")
    print()
