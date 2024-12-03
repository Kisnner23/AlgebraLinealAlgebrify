# EcuacionesLineales_MultiSolver_Tabbed.py
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import json
import os
import numpy as np  # Asegúrate de importar numpy

history_file = 'history.json'  # Nombre del archivo donde se almacenará el historial

def add_exercise(exercise_type, details):
    """
    Agrega un nuevo ejercicio al historial.

    Parámetros:
    - exercise_type: Tipo de ejercicio (e.g., 'Gauss', 'Escalonadas', 'Ecuaciones de Matrices')
    - detalles: Diccionario con detalles del ejercicio para graficar y pasos para mostrar
    """
    # Cargar el historial existente
    history = load_history()
    # Agregar el nuevo ejercicio
    history.append({'type': exercise_type, 'details': details})
    # Limitar el historial a los últimos 8 ejercicios
    history = history[-8:]
    # Guardar el historial actualizado con indentación para mejor legibilidad
    with open(history_file, 'w') as f:
        json.dump(history, f, indent=4)

def load_history():
    """
    Carga el historial de ejercicios desde el archivo JSON.

    Retorna:
    - Lista de ejercicios almacenados en history.json
    """
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            history = json.load(f)
    else:
        history = []
    return history

class MainApplication:
    def __init__(self, master):
        self.master = master
        master.title("Solver de Sistemas de Ecuaciones Lineales")
        master.geometry("800x600")
        master.configure(bg="#f9f9f9")

        # Estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TLabel", background="#f9f9f9", font=("Helvetica", 12))
        self.style.configure("TButton", font=("Helvetica", 12))
        self.style.configure("Header.TLabel", font=("Helvetica", 16, "bold"))

        # Frame Principal
        main_frame = ttk.Frame(master, padding="10 10 10 10")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Título
        title_label = ttk.Label(main_frame, text="Solver de Ecuaciones Lineales", style="Header.TLabel")
        title_label.pack(pady=(0, 20))

        # Selección de Método
        method_frame = ttk.Frame(main_frame, padding="10 10 10 10")
        method_frame.pack(fill=tk.X, pady=10)

        method_label = ttk.Label(method_frame, text="Selecciona un método:")
        method_label.pack(anchor='w')

        self.method_var = tk.StringVar()
        self.method_combobox = ttk.Combobox(method_frame, textvariable=self.method_var, state="readonly")
        self.method_combobox['values'] = ("Gauss", "Escalonadas", "Ecuaciones de Matrices")
        self.method_combobox.current(0)
        self.method_combobox.pack(fill=tk.X, pady=5)

        # Botón para Abrir Solver
        open_button = ttk.Button(main_frame, text="Abrir Solver", command=self.open_solver)
        open_button.pack(pady=20)

        # Información
        info_label = ttk.Label(main_frame, text="Puedes abrir múltiples solvers simultáneamente en pestañas diferentes.")
        info_label.pack()

        # Separador
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=10)

        # Notebook para las pestañas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(expand=True, fill=tk.BOTH)

        # Botón para cerrar pestañas
        close_button = ttk.Button(main_frame, text="Cerrar Pestaña Actual", command=self.close_current_tab)
        close_button.pack(pady=5)

    def open_solver(self):
        method = self.method_var.get()
        if method == "Gauss":
            solver = GaussSolver(self.notebook)
        elif method == "Escalonadas":
            solver = EscalonadasSolver(self.notebook)
        elif method == "Ecuaciones de Matrices":
            solver = MatrixSolver(self.notebook)
        else:
            messagebox.showerror("Método no reconocido", "Por favor, selecciona un método válido.")
            return
        # Agregar la pestaña al notebook
        self.notebook.add(solver, text=f"{method} Solver")
        self.notebook.select(solver)

    def close_current_tab(self):
        current_tab = self.notebook.select()
        if current_tab:
            self.notebook.forget(current_tab)

class BaseSolver(ttk.Frame):
    def __init__(self, parent, method_name):
        super().__init__(parent)
        self.parent = parent
        self.method_name = method_name
        self.configure(style="BaseSolver.TFrame")

        # Estilo
        self.style = ttk.Style()
        self.style.configure("BaseSolver.TFrame", background="#ffffff")
        self.style.configure("TLabel", background="#ffffff", font=("Helvetica", 12))
        self.style.configure("TButton", font=("Helvetica", 12))
        self.style.configure("Header.TLabel", font=("Helvetica", 14, "bold"))

        # Frame de Configuración
        config_frame = ttk.Frame(self, padding="10 10 10 10")
        config_frame.pack(fill=tk.X)

        # Título del Solver
        title_label = ttk.Label(config_frame, text=f"{method_name} Solver", style="Header.TLabel")
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 10))

        # Número de Ecuaciones
        self.num_eq_label = ttk.Label(config_frame, text="Número de Ecuaciones:")
        self.num_eq_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.num_eq_entry = ttk.Entry(config_frame, width=5)
        self.num_eq_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # Número de Variables
        self.num_var_label = ttk.Label(config_frame, text="Número de Variables:")
        self.num_var_label.grid(row=1, column=2, padx=5, pady=5, sticky='e')
        self.num_var_entry = ttk.Entry(config_frame, width=5)
        self.num_var_entry.grid(row=1, column=3, padx=5, pady=5, sticky='w')

        # Botón para Generar la Matriz
        self.generate_button = ttk.Button(config_frame, text="Generar Matriz", command=self.generate_matrix_entries)
        self.generate_button.grid(row=1, column=4, padx=10, pady=5)

        # Separador
        separator = ttk.Separator(self, orient='horizontal')
        separator.pack(fill=tk.X, pady=10)

        # Frame para las Entradas de la Matriz
        self.matrix_frame = ttk.Frame(self, padding="10 10 10 10")
        self.matrix_frame.pack(fill=tk.BOTH, expand=True)

        # Botón para Resolver
        self.solve_button = ttk.Button(self, text="Resolver", command=self.solve_system, state=tk.DISABLED)
        self.solve_button.pack(pady=10)

        # Área de Texto para Resultados (se puede eliminar si no se usa)
        self.result_text = scrolledtext.ScrolledText(self, width=70, height=15, state='disabled', bg="#f0f0f0", font=("Courier", 10))
        self.result_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Variables para las Entradas de la Matriz
        self.entries = []

    def generate_matrix_entries(self):
        # Limpiar el Frame Anterior
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()

        try:
            self.num_eq = int(self.num_eq_entry.get())
            self.num_var = int(self.num_var_entry.get())
            if self.num_eq <= 0 or self.num_var <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Entrada inválida", "Por favor, ingresa números enteros positivos para las dimensiones.")
            return

        # Crear Encabezados de Variables
        for j in range(self.num_var):
            var_label = ttk.Label(self.matrix_frame, text=f"x{j+1}")
            var_label.grid(row=0, column=j, padx=5, pady=5)
        b_label = ttk.Label(self.matrix_frame, text="b")
        b_label.grid(row=0, column=self.num_var, padx=5, pady=5)

        # Crear Entradas de la Matriz
        self.entries = []
        for i in range(1, self.num_eq + 1):
            row_entries = []
            for j in range(self.num_var + 1):
                entry = ttk.Entry(self.matrix_frame, width=7, justify='center')
                entry.grid(row=i, column=j, padx=5, pady=5)
                row_entries.append(entry)
            self.entries.append(row_entries)

        self.solve_button.config(state=tk.NORMAL)
        self.result_text.config(state='normal')
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state='disabled')

    def solve_system(self):
        raise NotImplementedError("Este método debe ser implementado por las clases hijas.")

    def read_augmented_matrix(self):
        """
        Lee la matriz aumentada ingresada por el usuario.

        Retorna:
        - Lista de listas que representa la matriz aumentada, o None si hay un error.
        """
        augmented_matrix = []
        try:
            for row in self.entries:
                current_row = []
                for entry in row:
                    val = float(entry.get())
                    current_row.append(val)
                augmented_matrix.append(current_row)
        except ValueError:
            messagebox.showerror("Entrada inválida", "Por favor, asegúrate de que todas las entradas sean números válidos.")
            return None
        return augmented_matrix

    def display_results(self, steps, solution_type, solution=None, solution_expressions=None, plot_data=None):
        """
        Muestra los pasos y resultados en una nueva ventana y agrega el ejercicio al historial.

        Parámetros:
        - steps: Lista de cadenas que representan los pasos del cálculo.
        - solution_type: Cadena que describe el tipo de solución.
        - solution: Lista con los valores de las variables (opcional).
        - solution_expressions: Diccionario con expresiones de las variables en caso de soluciones infinitas (opcional).
        - plot_data: Diccionario con datos para graficar (opcional).
        """
        # Crear una nueva ventana para los resultados
        result_window = tk.Toplevel(self)
        result_window.title("Resultados")
        result_window.geometry("600x400")

        exact_text = scrolledtext.ScrolledText(result_window, width=70, height=25, state='normal', bg="#f0f0f0", font=("Courier", 10))
        exact_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        for step in steps:
            exact_text.insert(tk.END, step + "\n")
        exact_text.insert(tk.END, "\n" + solution_type + "\n")

        if solution:
            solution_str = "Solución:\n"
            for idx, val in enumerate(solution):
                solution_str += f"x{idx + 1} = {val:.4f}\n"
            exact_text.insert(tk.END, solution_str)
        elif solution_expressions:
            solution_str = "Solución General:\n"
            for var, expr in solution_expressions.items():
                solution_str += f"{var} = {expr}\n"
            exact_text.insert(tk.END, solution_str)
        elif solution_type == "El sistema tiene infinitas soluciones.":
            exact_text.insert(tk.END, "Existen parámetros libres. Se requieren métodos adicionales para expresar las soluciones.\n")

        exact_text.config(state='disabled')

        # Agregar el ejercicio al historial
        exercise_type = self.method_name
        details = {'steps': '\n'.join(steps) + f"\n{solution_type}\n"}
        if solution:
            details['solution'] = {f"x{idx+1}": val for idx, val in enumerate(solution)}
        if solution_expressions:
            details['solution_expressions'] = solution_expressions
        if plot_data:
            details.update(plot_data)
        add_exercise(exercise_type, details)

    def calculate_rank(self, matrix):
        """
        Calcula el rango de una matriz utilizando eliminación Gaussiana.
        """
        m = len(matrix)
        n = len(matrix[0]) if m > 0 else 0
        rank = 0
        for r in range(m):
            if r + rank >= n:
                break
            if matrix[r][rank] == 0:
                for i in range(r + 1, m):
                    if matrix[i][rank] != 0:
                        matrix[r], matrix[i] = matrix[i], matrix[r]
                        break
                else:
                    rank += 1
                    continue
            for i in range(r + 1, m):
                if matrix[i][rank] != 0:
                    factor = matrix[i][rank] / matrix[r][rank]
                    matrix[i][rank] = 0  # Eliminamos el valor exacto
            rank += 1
        return rank

    def format_matrix(self, matrix):
        """
        Formatea una matriz para mostrarla como cadena de texto.

        Parámetros:
        - matrix: Lista de listas que representa la matriz.

        Retorna:
        - Cadena de texto formateada.
        """
        formatted = ""
        for row in matrix:
            formatted += " | ".join(f"{num:8.2f}" for num in row) + "\n"
        return formatted

class GaussSolver(BaseSolver):
    def __init__(self, parent):
        super().__init__(parent, "Gauss")

    def solve_system(self):
        augmented_matrix = self.read_augmented_matrix()
        if augmented_matrix is None:
            return

        matrix = [row[:] for row in augmented_matrix]
        steps = ["Matriz Aumentada Inicial:"]
        steps.append(self.format_matrix(matrix))

        num_eq = self.num_eq
        num_var = self.num_var

        # Implementación de Eliminación de Gauss
        for i in range(min(num_eq, num_var)):
            # Buscar el máximo en la columna i para evitar división por cero
            max_row = i
            for k in range(i + 1, num_eq):
                if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                    max_row = k
            if matrix[max_row][i] == 0:
                steps.append(f"No se puede encontrar un pivote en la columna {i+1}.")
                continue  # No se puede usar esta columna para pivote

            # Intercambiar filas si es necesario
            if max_row != i:
                matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
                steps.append(f"Intercambiar fila {i + 1} con fila {max_row + 1}:")
                steps.append(self.format_matrix(matrix))

            # Eliminar las filas debajo del pivote
            for j in range(i + 1, num_eq):
                if matrix[j][i] != 0:
                    factor = matrix[j][i] / matrix[i][i]
                    matrix[j] = [a - factor * b for a, b in zip(matrix[j], matrix[i])]
                    steps.append(f"Eliminar la variable x{i + 1} de la fila {j + 1} (Factor: {factor:.2f}):")
                    steps.append(self.format_matrix(matrix))

        # Retro sustitución
        solution = [0 for _ in range(num_var)]
        steps.append("Retro sustitución:")
        try:
            for i in range(min(num_eq, num_var) - 1, -1, -1):
                if matrix[i][i] == 0:
                    if matrix[i][-1] != 0:
                        raise ValueError("Sistema inconsistente")
                    continue  # Infinitas soluciones
                solution[i] = matrix[i][-1] / matrix[i][i]
                for k in range(i):
                    matrix[k][-1] -= matrix[k][i] * solution[i]
                steps.append(f"Solución para x{i + 1}: {solution[i]:.4f}")
        except ValueError:
            self.display_results(steps, "El sistema es inconsistente. No tiene solución.")
            return

        # Verificar si hay soluciones infinitas
        rank = self.calculate_rank(matrix)
        if rank < num_var:
            solution_type = "El sistema tiene infinitas soluciones."
            solution = None
        else:
            solution_type = "El sistema tiene una única solución."

        # Preparar datos para graficar (por ejemplo, la matriz final)
        plot_data = {
            'matriz': matrix
        }

        # Mostrar los pasos y resultados
        self.display_results(steps, solution_type, solution if rank == num_var else None, plot_data=plot_data)

class EscalonadasSolver(BaseSolver):
    def __init__(self, parent):
        super().__init__(parent, "Escalonadas")

    def solve_system(self):
        augmented_matrix = self.read_augmented_matrix()
        if augmented_matrix is None:
            return

        matrix = [row[:] for row in augmented_matrix]
        steps = ["Matriz Aumentada Inicial:"]
        steps.append(self.format_matrix(matrix))

        num_eq = self.num_eq
        num_var = self.num_var

        # Implementación de Escalonadas (Forma Escalonada)
        pivot_columns = []
        for i in range(min(num_eq, num_var)):
            # Hacer el pivote 1
            if matrix[i][i] == 0:
                # Buscar una fila para intercambiar
                for k in range(i + 1, num_eq):
                    if matrix[k][i] != 0:
                        matrix[i], matrix[k] = matrix[k], matrix[i]
                        steps.append(f"Intercambiar fila {i + 1} con fila {k + 1}:")
                        steps.append(self.format_matrix(matrix))
                        break
                else:
                    continue  # No se puede pivotear en esta columna

            pivot = matrix[i][i]
            matrix[i] = [x / pivot for x in matrix[i]]
            steps.append(f"Normalizar fila {i + 1} (dividir por el pivote {pivot:.2f}):")
            steps.append(self.format_matrix(matrix))
            pivot_columns.append(i)

            # Eliminar las filas debajo del pivote
            for j in range(i + 1, num_eq):
                factor = matrix[j][i]
                matrix[j] = [a - factor * b for a, b in zip(matrix[j], matrix[i])]
                steps.append(f"Eliminar la variable x{i + 1} de la fila {j + 1} (Factor: {factor:.2f}):")
                steps.append(self.format_matrix(matrix))

        # Determinar el tipo de solución
        rank = self.calculate_rank([row[:-1] for row in matrix])
        augmented_rank = self.calculate_rank(matrix)

        if rank < augmented_rank:
            solution_type = "El sistema es inconsistente. No tiene solución."
            solution = None
            solution_expressions = None
        elif rank == augmented_rank:
            if rank == num_var:
                # Sistema tiene una única solución
                solution_type = "El sistema tiene una única solución."
                solution = [0 for _ in range(num_var)]
                for i in range(num_var):
                    for j in range(num_eq):
                        if abs(matrix[j][i] - 1) < 1e-10:
                            solution[i] = matrix[j][-1]
                            break
                solution_expressions = None
            else:
                # Sistema tiene infinitas soluciones
                solution_type = "El sistema tiene infinitas soluciones."
                solution = None
                # Identificar variables libres y básicas
                pivot_vars = pivot_columns
                free_vars = [j for j in range(num_var) if j not in pivot_vars]
                # Asignar parámetros a variables libres
                parameters = [f"t{idx+1}" for idx in range(len(free_vars))]
                solution_expressions = {}
                for i in range(len(pivot_vars)):
                    expr = f"{matrix[i][-1]:.4f}"
                    for j, free_var in enumerate(free_vars):
                        coef = -matrix[i][free_var]
                        if coef != 0:
                            expr += f" + ({coef:.4f})*{parameters[j]}"
                    solution_expressions[f"x{pivot_vars[i]+1}"] = expr
                for idx, free_var in enumerate(free_vars):
                    solution_expressions[f"x{free_var+1}"] = parameters[idx]
        else:
            solution_type = "El sistema no pudo ser resuelto."
            solution = None
            solution_expressions = None

        # Preparar datos para graficar (por ejemplo, la matriz final escalonada)
        plot_data = {
            'matriz': matrix
        }

        # Mostrar los pasos y resultados
        self.display_results(steps, solution_type, solution, solution_expressions, plot_data=plot_data)

class MatrixSolver(BaseSolver):
    def __init__(self, parent):
        super().__init__(parent, "Ecuaciones de Matrices")

    def solve_system(self):
        augmented_matrix = self.read_augmented_matrix()
        if augmented_matrix is None:
            return

        matrix = [row[:] for row in augmented_matrix]
        steps = ["Matriz Aumentada Inicial:"]
        steps.append(self.format_matrix(matrix))

        num_eq = self.num_eq
        num_var = self.num_var

        # Verificar si la matriz cuadrada
        if num_eq != num_var:
            messagebox.showerror("Error", "Para resolver mediante matrices, el sistema debe ser cuadrado (número de ecuaciones igual al de variables).")
            return

        # Calcular el determinante para verificar si la matriz es invertible
        det = self.determinant([row[:-1] for row in matrix])
        steps.append(f"Determinante de la matriz A: {det:.2f}")
        if det == 0:
            solution_type = "La matriz A no es invertible. El sistema puede tener infinitas soluciones o no tener solución."
            self.display_results(steps, solution_type)
            return

        # Calcular la matriz inversa
        try:
            inverse = self.inverse([row[:-1] for row in matrix])
            steps.append("Matriz Inversa de A:")
            steps.append(self.format_matrix(inverse))
        except ValueError as e:
            steps.append(str(e))
            self.display_results(steps, "La matriz es singular y no tiene inversa.")
            return

        # Extraer el vector b
        b = [row[-1] for row in augmented_matrix]

        # Calcular la solución: x = A_inv * b
        solution = self.matrix_vector_multiply(inverse, b)
        steps.append("Solución (x = A⁻¹ * b):")
        for idx, val in enumerate(solution):
            steps.append(f"x{idx + 1} = {val:.4f}")

        solution_type = "El sistema tiene una única solución."

        # Preparar datos para graficar (por ejemplo, la matriz inversa)
        plot_data = {
            'matriz': [row[:-1] for row in matrix],  # Matriz de coeficientes
            'resultados': b
        }

        # Mostrar los pasos y resultados
        self.display_results(steps, solution_type, solution, plot_data=plot_data)

    def determinant(self, matrix):
        """
        Calcula el determinante de una matriz cuadrada utilizando eliminación Gaussiana.

        Parámetros:
        - matrix: Lista de listas que representa la matriz.

        Retorna:
        - Determinante de la matriz.
        """
        n = len(matrix)
        mat = [row[:] for row in matrix]
        det = 1
        for i in range(n):
            # Buscar el pivote
            if mat[i][i] == 0:
                for j in range(i + 1, n):
                    if mat[j][i] != 0:
                        mat[i], mat[j] = mat[j], mat[i]
                        det *= -1
                        break
                else:
                    return 0
            det *= mat[i][i]
            # Eliminar las filas debajo del pivote
            for j in range(i + 1, n):
                factor = mat[j][i] / mat[i][i]
                for k in range(i, n):
                    mat[j][k] -= factor * mat[i][k]
        return det

    def inverse(self, matrix):
        """
        Calcula la inversa de una matriz cuadrada utilizando el método de Gauss-Jordan.

        Parámetros:
        - matrix: Lista de listas que representa la matriz.

        Retorna:
        - Matriz inversa como lista de listas.

        Lanza:
        - ValueError si la matriz es singular.
        """
        n = len(matrix)
        mat = [row[:] for row in matrix]
        inverse = [[float(i == j) for j in range(n)] for i in range(n)]

        for i in range(n):
            # Hacer el pivote 1
            pivot = mat[i][i]
            if pivot == 0:
                for j in range(i + 1, n):
                    if mat[j][i] != 0:
                        mat[i], mat[j] = mat[j], mat[i]
                        inverse[i], inverse[j] = inverse[j], inverse[i]
                        pivot = mat[i][i]
                        break
                else:
                    raise ValueError("La matriz es singular y no tiene inversa.")
            factor = pivot
            mat[i] = [x / factor for x in mat[i]]
            inverse[i] = [x / factor for x in inverse[i]]

            # Eliminar los demás elementos en la columna
            for j in range(n):
                if j != i:
                    factor = mat[j][i]
                    mat[j] = [a - factor * b for a, b in zip(mat[j], mat[i])]
                    inverse[j] = [a - factor * b for a, b in zip(inverse[j], inverse[i])]

        return inverse

    def matrix_vector_multiply(self, matrix, vector):
        """
        Multiplica una matriz por un vector.

        Parámetros:
        - matrix: Lista de listas que representa la matriz.
        - vector: Lista que representa el vector.

        Retorna:
        - Lista que representa el resultado de la multiplicación.
        """
        result = []
        for row in matrix:
            val = sum(a * b for a, b in zip(row, vector))
            result.append(val)
        return result

def main():
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()

if __name__ == "__main__":
    main()
