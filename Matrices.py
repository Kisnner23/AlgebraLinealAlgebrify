# matrices.py
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import json
import os
import platform

# Ruta al archivo history.json
HISTORY_FILE = 'history.json'

# Función para guardar en el historial
def save_to_history(entry):
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r') as f:
                history = json.load(f)
        else:
            history = []
        history.append(entry)
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=4)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar en el historial.\n{e}")

class GridEntry:
    def __init__(self, parent, rows=3, cols=3, title="Matriz"):
        self.parent = parent
        self.rows = rows
        self.cols = cols
        self.title = title
        self.entries = []
        self.frame = tk.LabelFrame(parent, text=title, bg="#2E2E2E", fg="white",
                                   font=("Segoe UI", 12, "bold"), bd=2, relief=tk.GROOVE)
        self.frame.pack(pady=10, padx=10, fill=tk.X)

        # Controls for dimensions
        control_frame = tk.Frame(self.frame, bg="#2E2E2E")
        control_frame.pack(pady=5, padx=5, anchor='w')

        tk.Label(control_frame, text="Filas:", bg="#2E2E2E", fg="white",
                 font=("Segoe UI", 10)).grid(row=0, column=0, padx=5, pady=2)
        self.rows_var = tk.IntVar(value=self.rows)
        self.rows_spin = tk.Spinbox(control_frame, from_=1, to=10, width=5, textvariable=self.rows_var, command=self.update_grid)
        self.rows_spin.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(control_frame, text="Columnas:", bg="#2E2E2E", fg="white",
                 font=("Segoe UI", 10)).grid(row=0, column=2, padx=5, pady=2)
        self.cols_var = tk.IntVar(value=self.cols)
        self.cols_spin = tk.Spinbox(control_frame, from_=1, to=10, width=5, textvariable=self.cols_var, command=self.update_grid)
        self.cols_spin.grid(row=0, column=3, padx=5, pady=2)

        # Frame for entries
        self.entries_frame = tk.Frame(self.frame, bg="#2E2E2E")
        self.entries_frame.pack(pady=5, padx=5)

        self.create_grid()

    def create_grid(self):
        # Clear previous entries
        for widget in self.entries_frame.winfo_children():
            widget.destroy()
        self.entries = []

        # Create new grid of entries
        for r in range(self.rows):
            row_entries = []
            for c in range(self.cols):
                entry = tk.Entry(self.entries_frame, width=5, font=("Segoe UI", 12),
                                 bg="#3C3C3C", fg="white", justify='center')
                entry.grid(row=r, column=c, padx=2, pady=2)
                row_entries.append(entry)
            self.entries.append(row_entries)

    def update_grid(self):
        try:
            self.rows = self.rows_var.get()
            self.cols = self.cols_var.get()
            self.create_grid()
        except tk.TclError:
            messagebox.showerror("Error", "Dimensiones inválidas. Deben ser números enteros positivos.")

    def get_matrix(self):
        try:
            matrix = []
            for row in self.entries:
                current_row = []
                for entry in row:
                    val = entry.get()
                    if val == '':
                        raise ValueError("Todos los campos deben estar llenos.")
                    current_row.append(float(val))
                matrix.append(current_row)
            return np.array(matrix)
        except ValueError as ve:
            messagebox.showerror("Error de Entrada", str(ve))
            return None

class MatricesApp:
    def __init__(self, root):
        self.window = root
        self.window.title("📊 Matrices - Algebrify")
        self.window.geometry("1400x900")
        self.window.configure(bg="#2E2E2E")

        self.current_entry = None  # Para el teclado virtual

        # Estilos
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TButton",
                             background="#3C3C3C",
                             foreground="white",
                             font=("Segoe UI", 10, "bold"))
        self.style.map("TButton",
                       background=[('active', '#505050')])
        self.style.configure("Treeview",
                             background="#2E2E2E",
                             foreground="white",
                             fieldbackground="#2E2E2E",
                             font=("Segoe UI", 10))
        self.style.map("Treeview",
                       background=[('selected', '#575757')],
                       foreground=[('selected', 'white')])

        # Crear panel de navegación
        self.nav_panel = tk.Frame(self.window, bg="#1E1E1E", width=200)
        self.nav_panel.pack(side=tk.LEFT, fill=tk.Y)
        # Crear Treeview para la navegación
        self.tree = ttk.Treeview(self.nav_panel, show="tree")
        self.tree.pack(expand=True, fill=tk.BOTH, pady=20, padx=10)

        # Definir los nodos del Treeview
        self.define_tree()

        # Bind para la selección de nodos
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Área de contenido
        self.content_frame = tk.Frame(self.window, bg="#2E2E2E")
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Se elimina la incorporación automática del Teclado Virtual
        # self.virtual_keyboard = VirtualKeyboard(self)

    def define_tree(self):
        temas_principales = self.tree.insert("", "end", text="📚 Temas de Matrices", open=True)

        temas_relevantes = [
            "Suma y Resta de Matrices",
            "Multiplicación de Matrices",
            "Transpuesta de una Matriz",
            "Inversa de una Matriz",
            "Determinante de una Matriz",
            "Resolución de Sistemas de Ecuaciones",
            "Autovalores y Autovectores",
            "Descomposición LU",
            "Descomposición QR"
        ]

        for tema in temas_relevantes:
            self.tree.insert(temas_principales, "end", text=tema)

    def on_tree_select(self, event):
        selected_item = self.tree.selection()[0]
        item_text = self.tree.item(selected_item, "text")
        parent = self.tree.parent(selected_item)
        if parent:
            self.clear_content()
            self.display_content(item_text)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def display_content(self, topic):
        if topic == "Suma y Resta de Matrices":
            self.show_suma_resta_matrices()
        elif topic == "Multiplicación de Matrices":
            self.show_multiplicacion_matrices()
        elif topic == "Transpuesta de una Matriz":
            self.show_transpuesta_matriz()
        elif topic == "Inversa de una Matriz":
            self.show_inversa_matriz()
        elif topic == "Determinante de una Matriz":
            self.show_determinante_matriz()
        elif topic == "Resolución de Sistemas de Ecuaciones":
            self.show_resolucion_sistemas()
        elif topic == "Autovalores y Autovectores":
            self.show_autovalores_autovectores()
        elif topic == "Descomposición LU":
            self.show_descomposicion_lu()
        elif topic == "Descomposición QR":
            self.show_descomposicion_qr()
        else:
            self.show_placeholder(topic)

    def show_placeholder(self, topic):
        label = tk.Label(self.content_frame, text=f"Funcionalidad para '{topic}' aún no implementada.",
                         bg="#2E2E2E", fg="white", font=("Segoe UI", 14))
        label.pack(pady=20)

    def open_result_window(self, operation, procedure, result):
        result_window = tk.Toplevel(self.window)
        result_window.title(f"Resultado - {operation}")
        result_window.geometry("800x600")
        result_window.configure(bg="#2E2E2E")

        # Título
        title_label = tk.Label(result_window, text=f"{operation} - Resultado", bg="#2E2E2E",
                               fg="white", font=("Segoe UI", 16, "bold"))
        title_label.pack(pady=10)

        # Procedimiento
        procedure_label = tk.Label(result_window, text="Procedimiento Detallado:", bg="#2E2E2E",
                                   fg="white", font=("Segoe UI", 12, "bold"))
        procedure_label.pack(pady=5, padx=10, anchor='w')

        procedure_text = tk.Text(result_window, height=20, width=90, font=("Segoe UI", 10),
                                 bg="#3C3C3C", fg="white", wrap='word')
        procedure_text.insert(tk.END, procedure)
        procedure_text.config(state='disabled')
        procedure_text.pack(pady=5, padx=10)

        # Resultado
        result_label = tk.Label(result_window, text="Resultado:", bg="#2E2E2E",
                                fg="white", font=("Segoe UI", 12, "bold"))
        result_label.pack(pady=5, padx=10, anchor='w')

        result_display = tk.Text(result_window, height=10, width=90, font=("Segoe UI", 12),
                                 bg="#3C3C3C", fg="lightgreen", wrap='word')
        result_display.insert(tk.END, result)
        result_display.config(state='disabled')
        result_display.pack(pady=5, padx=10)

    def parse_matriz(self, grid_entry):
        return grid_entry.get_matrix()

    def show_suma_resta_matrices(self):
        # Crear GridEntry para Matriz 1
        matriz1 = GridEntry(self.content_frame, title="Matriz 1")
        # Crear GridEntry para Matriz 2
        matriz2 = GridEntry(self.content_frame, title="Matriz 2")

        # Botones de operación
        buttons_frame = tk.Frame(self.content_frame, bg="#2E2E2E")
        buttons_frame.pack(pady=10)

        suma_button = ttk.Button(buttons_frame, text="Sumar", command=lambda: self.calcular_suma(matriz1, matriz2), width=15)
        suma_button.pack(side=tk.LEFT, padx=10)

        resta_button = ttk.Button(buttons_frame, text="Restar", command=lambda: self.calcular_resta(matriz1, matriz2), width=15)
        resta_button.pack(side=tk.LEFT, padx=10)

    def calcular_suma(self, matriz1, matriz2):
        A = self.parse_matriz(matriz1)
        B = self.parse_matriz(matriz2)
        if A is None or B is None:
            return
        try:
            if A.shape != B.shape:
                raise ValueError("Las matrices deben tener las mismas dimensiones para sumar.")
            suma = A + B
            resultado = np.array2string(suma, precision=2, separator=', ')
            # Procedimiento detallado
            procedure = f"Para sumar las matrices, se suma cada elemento correspondiente:\n\nMatriz 1 (A):\n{A}\n\nMatriz 2 (B):\n{B}\n\nSuma (A + B):\n{suma}"
            self.open_result_window("Suma de Matrices", procedure, resultado)
            save_to_history({
                "Operación": "Suma de Matrices",
                "Matriz 1": A.tolist(),
                "Matriz 2": B.tolist(),
                "Resultado": suma.tolist()
            })
        except Exception as e:
            messagebox.showerror("Error", f"Error al sumar matrices:\n{e}")

    def calcular_resta(self, matriz1, matriz2):
        A = self.parse_matriz(matriz1)
        B = self.parse_matriz(matriz2)
        if A is None or B is None:
            return
        try:
            if A.shape != B.shape:
                raise ValueError("Las matrices deben tener las mismas dimensiones para restar.")
            resta = A - B
            resultado = np.array2string(resta, precision=2, separator=', ')
            # Procedimiento detallado
            procedure = f"Para restar las matrices, se resta cada elemento correspondiente:\n\nMatriz 1 (A):\n{A}\n\nMatriz 2 (B):\n{B}\n\nResta (A - B):\n{resta}"
            self.open_result_window("Resta de Matrices", procedure, resultado)
            save_to_history({
                "Operación": "Resta de Matrices",
                "Matriz 1": A.tolist(),
                "Matriz 2": B.tolist(),
                "Resultado": resta.tolist()
            })
        except Exception as e:
            messagebox.showerror("Error", f"Error al restar matrices:\n{e}")

    def show_multiplicacion_matrices(self):
        # Crear GridEntry para Matriz 1
        matriz1 = GridEntry(self.content_frame, title="Matriz 1")
        # Crear GridEntry para Matriz 2
        matriz2 = GridEntry(self.content_frame, title="Matriz 2")

        # Botón de operación
        buttons_frame = tk.Frame(self.content_frame, bg="#2E2E2E")
        buttons_frame.pack(pady=10)

        calc_button = ttk.Button(buttons_frame, text="Calcular Producto", command=lambda: self.calcular_producto(matriz1, matriz2), width=20)
        calc_button.pack(pady=10)

    def calcular_producto(self, matriz1, matriz2):
        A = self.parse_matriz(matriz1)
        B = self.parse_matriz(matriz2)
        if A is None or B is None:
            return
        try:
            if A.shape[1] != B.shape[0]:
                raise ValueError("El número de columnas de la primera matriz debe ser igual al número de filas de la segunda matriz.")
            producto = np.dot(A, B)
            resultado = np.array2string(producto, precision=2, separator=', ')
            # Procedimiento detallado
            procedure = f"Para multiplicar las matrices, se realiza el producto punto entre filas de la primera matriz y columnas de la segunda matriz:\n\nMatriz 1 (A):\n{A}\n\nMatriz 2 (B):\n{B}\n\nProducto (A * B):\n{producto}"
            self.open_result_window("Multiplicación de Matrices", procedure, resultado)
            save_to_history({
                "Operación": "Producto de Matrices",
                "Matriz 1": A.tolist(),
                "Matriz 2": B.tolist(),
                "Resultado": producto.tolist()
            })
        except Exception as e:
            messagebox.showerror("Error", f"Error al multiplicar matrices:\n{e}")

    def show_transpuesta_matriz(self):
        # Crear GridEntry para Matriz
        matriz = GridEntry(self.content_frame, title="Matriz")

        # Botón de operación
        calc_button = ttk.Button(self.content_frame, text="Calcular Transpuesta", command=lambda: self.calcular_transpuesta(matriz), width=25)
        calc_button.pack(pady=10)

    def calcular_transpuesta(self, matriz_entry):
        A = self.parse_matriz(matriz_entry)
        if A is None:
            return
        try:
            transpuesta = A.T
            resultado = np.array2string(transpuesta, precision=2, separator=', ')
            # Procedimiento detallado
            procedure = f"Para calcular la transpuesta de la matriz, se intercambian las filas por columnas:\n\nMatriz Original (A):\n{A}\n\nMatriz Transpuesta (Aᵀ):\n{transpuesta}"
            self.open_result_window("Transpuesta de una Matriz", procedure, resultado)
            save_to_history({
                "Operación": "Transpuesta de Matriz",
                "Matriz": A.tolist(),
                "Resultado": transpuesta.tolist()
            })
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular la transpuesta:\n{e}")

    def show_inversa_matriz(self):
        # Crear GridEntry para Matriz Cuadrada
        matriz = GridEntry(self.content_frame, rows=3, cols=3, title="Matriz Cuadrada")

        # Botón de operación
        calc_button = ttk.Button(self.content_frame, text="Calcular Inversa", command=lambda: self.calcular_inversa(matriz), width=20)
        calc_button.pack(pady=10)

    def calcular_inversa(self, matriz_entry):
        A = self.parse_matriz(matriz_entry)
        if A is None:
            return
        try:
            if A.shape[0] != A.shape[1]:
                raise ValueError("La matriz debe ser cuadrada para calcular su inversa.")
            inversa = np.linalg.inv(A)
            resultado = np.array2string(inversa, precision=2, separator=', ')
            # Procedimiento detallado
            procedure = f"Para calcular la inversa de la matriz, se utiliza la función inversa de NumPy:\n\nMatriz Original (A):\n{A}\n\nMatriz Inversa (A⁻¹):\n{inversa}"
            self.open_result_window("Inversa de una Matriz", procedure, resultado)
            save_to_history({
                "Operación": "Inversa de Matriz",
                "Matriz": A.tolist(),
                "Resultado": inversa.tolist()
            })
        except np.linalg.LinAlgError:
            messagebox.showerror("Error", "La matriz es singular y no tiene inversa.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular la inversa:\n{e}")

    def show_determinante_matriz(self):
        # Crear GridEntry para Matriz Cuadrada
        matriz = GridEntry(self.content_frame, rows=3, cols=3, title="Matriz Cuadrada")

        # Botón de operación
        calc_button = ttk.Button(self.content_frame, text="Calcular Determinante", command=lambda: self.calcular_determinante(matriz), width=25)
        calc_button.pack(pady=10)

    def calcular_determinante(self, matriz_entry):
        A = self.parse_matriz(matriz_entry)
        if A is None:
            return
        try:
            if A.shape[0] != A.shape[1]:
                raise ValueError("La matriz debe ser cuadrada para calcular su determinante.")
            determinante = np.linalg.det(A)
            resultado = f"{determinante:.2f}"
            # Procedimiento detallado
            procedure = f"Para calcular el determinante de la matriz, se utiliza la función de NumPy:\n\nMatriz (A):\n{A}\n\nDeterminante (det(A)): {determinante:.2f}"
            self.open_result_window("Determinante de una Matriz", procedure, resultado)
            save_to_history({
                "Operación": "Determinante de Matriz",
                "Matriz": A.tolist(),
                "Resultado": determinante
            })
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular el determinante:\n{e}")

    def show_resolucion_sistemas(self):
        # Crear GridEntry para Sistema de Ecuaciones
        sistema_frame = tk.LabelFrame(self.content_frame, text="Sistema de Ecuaciones", bg="#2E2E2E", fg="white",
                                      font=("Segoe UI", 12, "bold"), bd=2, relief=tk.GROOVE)
        sistema_frame.pack(pady=10, padx=10, fill=tk.X)

        # Selección de dimensiones
        dim_frame = tk.Frame(sistema_frame, bg="#2E2E2E")
        dim_frame.pack(pady=5, padx=5, anchor='w')

        tk.Label(dim_frame, text="Ecuaciones:", bg="#2E2E2E", fg="white",
                 font=("Segoe UI", 10)).grid(row=0, column=0, padx=5, pady=2)
        self.ecuaciones_var = tk.IntVar(value=3)
        self.ecuaciones_spin = tk.Spinbox(dim_frame, from_=1, to=10, width=5, textvariable=self.ecuaciones_var, command=self.update_sistema)
        self.ecuaciones_spin.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(dim_frame, text="Variables:", bg="#2E2E2E", fg="white",
                 font=("Segoe UI", 10)).grid(row=0, column=2, padx=5, pady=2)
        self.variables_var = tk.IntVar(value=3)
        self.variables_spin = tk.Spinbox(dim_frame, from_=1, to=10, width=5, textvariable=self.variables_var, command=self.update_sistema)
        self.variables_spin.grid(row=0, column=3, padx=5, pady=2)

        # Frame para entradas de sistema
        self.sistema_entries_frame = tk.Frame(sistema_frame, bg="#2E2E2E")
        self.sistema_entries_frame.pack(pady=5, padx=5)

        self.sistema_entries = []
        self.update_sistema()

        # Botón de operación
        calc_button = ttk.Button(self.content_frame, text="Resolver Sistema", command=lambda: self.resolver_sistema(), width=20)
        calc_button.pack(pady=10)

    def update_sistema(self):
        # Limpiar entradas anteriores
        for widget in self.sistema_entries_frame.winfo_children():
            widget.destroy()
        self.sistema_entries = []

        ecuaciones = self.ecuaciones_var.get()
        variables = self.variables_var.get()

        # Crear nuevas entradas
        for i in range(ecuaciones):
            fila = []
            for j in range(variables + 1):  # Última columna para términos independientes
                entry = tk.Entry(self.sistema_entries_frame, width=5, font=("Segoe UI", 12),
                                 bg="#3C3C3C", fg="white", justify='center')
                entry.grid(row=i, column=j, padx=2, pady=2)
                fila.append(entry)
            self.sistema_entries.append(fila)

        # Etiquetas para variables
        for j in range(variables):
            tk.Label(self.sistema_entries_frame, text=f"x{j+1} =", bg="#2E2E2E", fg="white",
                     font=("Segoe UI", 10)).grid(row=0, column=j, sticky='e')

    def resolver_sistema(self):
        ecuaciones = self.ecuaciones_var.get()
        variables = self.variables_var.get()
        A = []
        b = []
        try:
            for i in range(ecuaciones):
                fila = []
                for j in range(variables):
                    val = self.sistema_entries[i][j].get()
                    if val == '':
                        raise ValueError("Todos los campos deben estar llenos.")
                    fila.append(float(val))
                term = self.sistema_entries[i][-1].get()
                if term == '':
                    raise ValueError("Todos los campos deben estar llenos.")
                A.append(fila)
                b.append(float(term))
            A = np.array(A)
            b = np.array(b)
            if A.shape[0] != A.shape[1]:
                raise ValueError("El sistema debe tener el mismo número de ecuaciones y variables.")
            x = np.linalg.solve(A, b)
            resultado = np.array2string(x, precision=2, separator=', ')
            # Procedimiento detallado
            procedure = f"Para resolver el sistema de ecuaciones lineales, se utiliza la función de solución de NumPy:\n\nMatriz de Coeficientes (A):\n{A}\n\nVector de Términos Independientes (b):\n{b}\n\nSolución (x):\n{x}"
            self.open_result_window("Resolución de Sistemas de Ecuaciones", procedure, resultado)
            save_to_history({
                "Operación": "Resolución de Sistema de Ecuaciones",
                "Sistema": {
                    "Coeficientes": A.tolist(),
                    "Términos Independientes": b.tolist(),
                    "Resultado": x.tolist()
                }
            })
        except ValueError as ve:
            messagebox.showerror("Error de Entrada", str(ve))
        except np.linalg.LinAlgError:
            messagebox.showerror("Error", "El sistema no tiene solución única.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al resolver el sistema:\n{e}")

    def show_autovalores_autovectores(self):
        # Crear GridEntry para Matriz Cuadrada
        matriz = GridEntry(self.content_frame, rows=3, cols=3, title="Matriz Cuadrada")

        # Botón de operación
        calc_button = ttk.Button(self.content_frame, text="Calcular Autovalores y Autovectores",
                                 command=lambda: self.calcular_eigen(matriz), width=30)
        calc_button.pack(pady=10)

    def calcular_eigen(self, matriz_entry):
        A = self.parse_matriz(matriz_entry)
        if A is None:
            return
        try:
            if A.shape[0] != A.shape[1]:
                raise ValueError("La matriz debe ser cuadrada para calcular autovalores y autovectores.")
            eigenvalues, eigenvectors = np.linalg.eig(A)
            eigenvalues_str = np.array2string(eigenvalues, precision=2, separator=', ')
            eigenvectors_str = np.array2string(eigenvectors, precision=2, separator=', ')
            # Procedimiento detallado
            procedure = f"Para calcular los autovalores y autovectores, se utiliza la función de NumPy:\n\nMatriz (A):\n{A}\n\nAutovalores:\n{eigenvalues}\n\nAutovectores:\n{eigenvectors}"
            self.open_result_window("Autovalores y Autovectores", procedure,
                                    f"Autovalores:\n{eigenvalues_str}\n\nAutovectores:\n{eigenvectors_str}")
            save_to_history({
                "Operación": "Autovalores y Autovectores",
                "Matriz": A.tolist(),
                "Autovalores": eigenvalues.tolist(),
                "Autovectores": eigenvectors.tolist()
            })
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular autovalores y autovectores:\n{e}")

    def show_descomposicion_lu(self):
        # Crear GridEntry para Matriz Cuadrada
        matriz = GridEntry(self.content_frame, rows=3, cols=3, title="Matriz Cuadrada")

        # Botón de operación
        calc_button = ttk.Button(self.content_frame, text="Calcular Descomposición LU",
                                 command=lambda: self.calcular_lu(matriz), width=25)
        calc_button.pack(pady=10)

    def calcular_lu(self, matriz_entry):
        A = self.parse_matriz(matriz_entry)
        if A is None:
            return
        try:
            if A.shape[0] != A.shape[1]:
                raise ValueError("La matriz debe ser cuadrada para la descomposición LU.")
            P, L, U = self.lu_decomposition(A.copy())
            resultado = f"P:\n{P}\n\nL:\n{L}\n\nU:\n{U}"
            # Procedimiento detallado
            procedure = f"Para realizar la descomposición LU con pivoting parcial:\n\nMatriz Original (A):\n{A}\n\nMatriz de Permutación (P):\n{P}\n\nMatriz Inferior (L):\n{L}\n\nMatriz Superior (U):\n{U}"
            self.open_result_window("Descomposición LU", procedure, resultado)
            save_to_history({
                "Operación": "Descomposición LU",
                "Matriz": A.tolist(),
                "P": P.tolist(),
                "L": L.tolist(),
                "U": U.tolist()
            })
        except Exception as e:
            messagebox.showerror("Error", f"Error en la descomposición LU:\n{e}")

    def lu_decomposition(self, A):
        n = A.shape[0]
        L = np.zeros_like(A)
        U = np.zeros_like(A)
        P = np.eye(n)
        for i in range(n):
            # Pivoting
            max_row = np.argmax(abs(A[i:, i])) + i
            if A[max_row, i] == 0:
                raise ValueError("La matriz es singular.")
            if max_row != i:
                A[[i, max_row]] = A[[max_row, i]]
                P[[i, max_row]] = P[[max_row, i]]
                L[[i, max_row], :i] = L[[max_row, i], :i]
            # LU Decomposition
            L[i, i] = 1
            for j in range(i, n):
                U[i, j] = A[i, j] - np.dot(L[i, :i], U[:i, j])
            for j in range(i+1, n):
                L[j, i] = (A[j, i] - np.dot(L[j, :i], U[:i, i])) / U[i, i]
        return P, L, U

    def show_descomposicion_qr(self):
        # Crear GridEntry para Matriz
        matriz = GridEntry(self.content_frame, title="Matriz")

        # Botón de operación
        calc_button = ttk.Button(self.content_frame, text="Calcular Descomposición QR",
                                 command=lambda: self.calcular_qr(matriz), width=25)
        calc_button.pack(pady=10)

    def calcular_qr(self, matriz_entry):
        A = self.parse_matriz(matriz_entry)
        if A is None:
            return
        try:
            Q, R = np.linalg.qr(A)
            resultado = f"Q:\n{Q}\n\nR:\n{R}"
            # Procedimiento detallado
            procedure = f"Para realizar la descomposición QR, se utiliza la función de NumPy:\n\nMatriz Original (A):\n{A}\n\nMatriz Ortogonal (Q):\n{Q}\n\nMatriz Superior (R):\n{R}"
            self.open_result_window("Descomposición QR", procedure, resultado)
            save_to_history({
                "Operación": "Descomposición QR",
                "Matriz": A.tolist(),
                "Q": Q.tolist(),
                "R": R.tolist()
            })
        except Exception as e:
            messagebox.showerror("Error", f"Error en la descomposición QR:\n{e}")

def main():
    root = tk.Tk()
    app = MatricesApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
