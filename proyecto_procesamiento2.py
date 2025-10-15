"""proyecto_procesamiento2.py"""
import pandas as pd
import matplotlib.pyplot as plt
#Wollman Madiedo Hoyos T00065230
# --- Importar datos ---
# Leer archivo Excel
df = pd.read_excel("temperaturas_ordenadas.xlsx")

# Crear los arreglos
x = list(range(len(df)))  # índice de cada fila
y = list(df["temperature_2m"])  # valores de la columna 'temperature_2m'

# Tamaño de los datos
n = len(x)

# --- Funciones auxiliares ---
def suma(valores):
    return sum(valores)

def producto(lista1, lista2):
    return [a * b for a, b in zip(lista1, lista2)]

def potencia(lista, exp):
    return [a ** exp for a in lista]

# --- REGRESIÓN LINEAL ---
sum_x = suma(x)
sum_y = suma(y)
sum_xy = suma(producto(x, y))
sum_x2 = suma(potencia(x, 2))

b = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
a = (sum_y - b * sum_x) / n

y_pred_lineal = [a + b * xi for xi in x]

print(f"Recta de regresión lineal: y = {a:.3f} + {b:.3f}x")

# --- REGRESIÓN POLINOMIAL DE SEGUNDO GRADO ---
sum_x3 = suma(potencia(x, 3))
sum_x4 = suma(potencia(x, 4))
sum_x2y = suma(producto(potencia(x, 2), y))

# Matrices del sistema
A = [
    [n, sum_x, sum_x2],
    [sum_x, sum_x2, sum_x3],
    [sum_x2, sum_x3, sum_x4]
]
B = [sum_y, sum_xy, sum_x2y]

# Resolver el sistema 3x3 con eliminación de Gauss
def gauss_elimination(A, B):
    n = len(B)
    for i in range(n):
        # variable auxiliar de pivoteo
        pivot = A[i][i]
        for j in range(i, n):
            A[i][j] /= pivot
        B[i] /= pivot
        # Eliminación
        for k in range(i + 1, n):
            factor = A[k][i]
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]
            B[k] -= factor * B[i]
    # Sustitución hacia atrás
    X = [0] * n
    for i in range(n - 1, -1, -1):
        X[i] = B[i] - sum(A[i][j] * X[j] for j in range(i + 1, n))
    return X

a2, b2, c2 = gauss_elimination(A, B)
y_pred_poly = [a2 + b2 * xi + c2 * (xi ** 2) for xi in x]

print(f"Ecuación polinomial: y = {a2:.3f} + {b2:.3f}x + {c2:.3f}x²")

# --- GRAFICAR ---
plt.figure(figsize=(10, 6))
plt.scatter(x, y, color='black', label='Datos reales', s=50)
plt.plot(x, y_pred_lineal, color='blue', label='Regresión lineal')
plt.plot(x, y_pred_poly, color='red', linestyle='--', label='Regresión polinomial (grado 2)')
plt.title("Regresión de temperatura respecto al tiempo (Cartagena)")
plt.xlabel("Tiempo (horas)")
plt.ylabel("Temperatura (°C)")
plt.legend()
plt.grid(True)
plt.show()