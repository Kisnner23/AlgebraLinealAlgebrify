# Vectores.py

import tkinter as tk
from tkinter import ttk, messagebox
import math

class Vector:
    def __init__(self, componentes):
        """
        Inicializa el vector con una lista de componentes.
        """
        self.componentes = componentes
        self.dimension = len(componentes)
    
    def __str__(self):
        return f"Vector({self.componentes})"
    
    def __add__(self, otro):
        """
        Suma de dos vectores con pasos.
        """
        if self.dimension != otro.dimension:
            raise ValueError("Los vectores deben tener la misma dimensión para la suma.")
        pasos = []
        resultado = []
        pasos.append(f"Sumando componente a componente:")
        for a, b in zip(self.componentes, otro.componentes):
            suma = a + b
            resultado.append(suma)
            pasos.append(f"{a} + {b} = {suma}")
        pasos.append(f"Resultado: {resultado}")
        return resultado, pasos
    
    def __sub__(self, otro):
        """
        Resta de dos vectores con pasos.
        """
        if self.dimension != otro.dimension:
            raise ValueError("Los vectores deben tener la misma dimensión para la resta.")
        pasos = []
        resultado = []
        pasos.append(f"Restando componente a componente:")
        for a, b in zip(self.componentes, otro.componentes):
            resta = a - b
            resultado.append(resta)
            pasos.append(f"{a} - {b} = {resta}")
        pasos.append(f"Resultado: {resultado}")
        return resultado, pasos
    
    def scalar_multiply(self, escalar):
        """
        Multiplicación de un vector por un escalar con pasos.
        """
        pasos = []
        resultado = []
        pasos.append(f"Multiplicando cada componente por el escalar {escalar}:")
        for a in self.componentes:
            producto = a * escalar
            resultado.append(producto)
            pasos.append(f"{a} * {escalar} = {producto}")
        pasos.append(f"Resultado: {resultado}")
        return resultado, pasos
    
    def dot_product(self, otro):
        """
        Producto punto (escalar) de dos vectores con pasos.
        """
        if self.dimension != otro.dimension:
            raise ValueError("Los vectores deben tener la misma dimensión para el producto punto.")
        pasos = []
        pasos.append(f"Calculando el producto punto:")
        productos = [a * b for a, b in zip(self.componentes, otro.componentes)]
        pasos.append(f"Productos componente a componente: {productos}")
        resultado = sum(productos)
        pasos.append(f"Suma de productos: {resultado}")
        return resultado, pasos
    
    def cross_product(self, otro):
        """
        Producto cruz (vectorial) de dos vectores en 3D con pasos.
        """
        if self.dimension != 3 or otro.dimension != 3:
            raise ValueError("El producto cruz solo está definido para vectores en 3 dimensiones.")
        a1, a2, a3 = self.componentes
        b1, b2, b3 = otro.componentes
        pasos = []
        pasos.append("Calculando el producto cruz:")
        pasos.append(f"i: {a2} * {b3} - {a3} * {b2} = {a2 * b3} - {a3 * b2} = {a2 * b3 - a3 * b2}")
        pasos.append(f"j: {a3} * {b1} - {a1} * {b3} = {a3 * b1} - {a1 * b3} = {a3 * b1 - a1 * b3}")
        pasos.append(f"k: {a1} * {b2} - {a2} * {b1} = {a1 * b2} - {a2 * b1} = {a1 * b2 - a2 * b1}")
        resultado = [
            a2 * b3 - a3 * b2,
            a3 * b1 - a1 * b3,
            a1 * b2 - a2 * b1
        ]
        pasos.append(f"Resultado: {resultado}")
        return resultado, pasos
    
    def magnitude(self):
        """
        Calcula la norma (magnitud) del vector con pasos.
        """
        pasos = []
        pasos.append("Calculando la magnitud del vector:")
        cuadrados = [a**2 for a in self.componentes]
        pasos.append(f"Componentes al cuadrado: {cuadrados}")
        suma = sum(cuadrados)
        pasos.append(f"Suma de cuadrados: {suma}")
        mag = math.sqrt(suma)
        pasos.append(f"Raíz cuadrada de {suma}: {mag}")
        return mag, pasos
    
    def normalize(self):
        """
        Normaliza el vector (convierte a un vector unitario) con pasos.
        """
        pasos = []
        mag, pasos_mag = self.magnitude()
        pasos.extend(pasos_mag)
        if mag == 0:
            raise ValueError("No se puede normalizar el vector cero.")
        pasos.append(f"Dividiendo cada componente por la magnitud {mag}:")
        resultado = [a / mag for a in self.componentes]
        pasos.append(f"Vector normalizado: {resultado}")
        return resultado, pasos
    
    def projection_onto(self, otro):
        """
        Proyecta este vector sobre otro vector con pasos.
        """
        pasos = []
        pasos.append(f"Proyectando {self} sobre {otro}:")
        dot_product, pasos_dot = self.dot_product(otro)
        pasos.extend(pasos_dot)
        otro_dot, _ = otro.dot_product(otro)
        pasos.append(f"Producto punto de {otro} consigo mismo: {otro_dot}")
        if otro_dot == 0:
            raise ValueError("No se puede proyectar sobre el vector cero.")
        escalar = dot_product / otro_dot
        pasos.append(f"Escalar para la proyección: {dot_product} / {otro_dot} = {escalar}")
        proyeccion, pasos_proy = otro.scalar_multiply(escalar)
        pasos.extend(pasos_proy)
        return proyeccion, pasos
    
    def angle_with(self, otro):
        """
        Calcula el ángulo entre este vector y otro en grados con pasos.
        """
        pasos = []
        pasos.append(f"Calculando el ángulo entre {self} y {otro}:")
        dot_product, pasos_dot = self.dot_product(otro)
        pasos.extend(pasos_dot)
        mag_self, pasos_mag_self = self.magnitude()
        pasos.extend(pasos_mag_self)
        mag_otro, pasos_mag_otro = otro.magnitude()
        pasos.extend(pasos_mag_otro)
        if mag_self == 0 or mag_otro == 0:
            raise ValueError("No se puede calcular el ángulo con el vector cero.")
        pasos.append(f"Coseno del ángulo: {dot_product} / ({mag_self} * {mag_otro}) = {dot_product / (mag_self * mag_otro)}")
        cos_theta = dot_product / (mag_self * mag_otro)
        # Asegurarse de que el valor esté en el rango [-1,1]
        cos_theta = max(min(cos_theta, 1.0), -1.0)
        angle_rad = math.acos(cos_theta)
        angle_deg = math.degrees(angle_rad)
        pasos.append(f"Ángulo en radianes: {angle_rad}")
        pasos.append(f"Ángulo en grados: {angle_deg}")
        return angle_deg, pasos
    
    @staticmethod
    def are_linearly_independent(vectores):
        """
        Determina si un conjunto de vectores es linealmente independiente con pasos.
        """
        pasos = []
        if not vectores:
            pasos.append("No se proporcionaron vectores.")
            return False, pasos
        dimension = vectores[0].dimension
        if any(v.dimension != dimension for v in vectores):
            raise ValueError("Todos los vectores deben tener la misma dimensión.")
        
        pasos.append("Construyendo la matriz de vectores:")
        matriz = [v.componentes[:] for v in vectores]
        pasos.append(f"Matriz inicial: {matriz}")
        
        # Aplicar eliminación gaussiana para encontrar el rango
        rank = 0
        for col in range(dimension):
            pivot = None
            for row in range(rank, len(matriz)):
                if matriz[row][col] != 0:
                    pivot = row
                    break
            if pivot is not None:
                pasos.append(f"Seleccionando pivote en la columna {col}, fila {pivot}")
                matriz[rank], matriz[pivot] = matriz[pivot], matriz[rank]
                pivot_val = matriz[rank][col]
                pasos.append(f"Normalizando fila {rank} con el pivote {pivot_val}")
                matriz[rank] = [element / pivot_val for element in matriz[rank]]
                for r in range(len(matriz)):
                    if r != rank and matriz[r][col] != 0:
                        factor = matriz[r][col]
                        pasos.append(f"Eliminando elemento en fila {r}, columna {col} usando factor {factor}")
                        matriz[r] = [a - factor * b for a, b in zip(matriz[r], matriz[rank])]
                rank += 1
                pasos.append(f"Estado de la matriz: {matriz}")
        independientes = rank == len(vectores)
        pasos.append(f"Rango de la matriz: {rank}")
        pasos.append(f"Cantidad de vectores: {len(vectores)}")
        pasos.append(f"Los vectores {'son' if independientes else 'NO son'} linealmente independientes.")
        return independientes, pasos
    
    @staticmethod
    def linear_combination(vectores, escalares):
        """
        Construye una combinación lineal de vectores dados una lista de escalares con pasos.
        """
        pasos = []
        if len(vectores) != len(escalares):
            raise ValueError("El número de vectores y escalares debe ser el mismo.")
        dimension = vectores[0].dimension
        if any(v.dimension != dimension for v in vectores):
            raise ValueError("Todos los vectores deben tener la misma dimensión.")
        pasos.append("Construyendo la combinación lineal:")
        combinacion = [0] * dimension
        for i, (vector, escalar) in enumerate(zip(vectores, escalares)):
            pasos.append(f"Multiplicando Vector {i+1} por escalar {escalar}: {vector.componentes} * {escalar}")
            producto = [a * escalar for a in vector.componentes]
            pasos.append(f"Resultado: {producto}")
            combinacion = [a + b for a, b in zip(combinacion, producto)]
            pasos.append(f"Suma acumulada: {combinacion}")
        pasos.append(f"Combinación lineal final: {combinacion}")
        return combinacion, pasos
    
    @staticmethod
    def base_and_dimension(vectores):
        """
        Determina una base para el espacio generado por los vectores y su dimensión con pasos.
        """
        pasos = []
        if not vectores:
            pasos.append("No se proporcionaron vectores.")
            return [], 0, pasos
        dimension = vectores[0].dimension
        if any(v.dimension != dimension for v in vectores):
            raise ValueError("Todos los vectores deben tener la misma dimensión.")
        
        pasos.append("Aplicando eliminación gaussiana para encontrar vectores independientes:")
        matriz = [v.componentes[:] for v in vectores]
        pasos.append(f"Matriz inicial: {matriz}")
        base = []
        for col in range(dimension):
            pivot = None
            for row in range(len(matriz)):
                if matriz[row][col] != 0:
                    pivot = row
                    break
            if pivot is not None:
                pasos.append(f"Seleccionando pivote en columna {col}, fila {pivot}")
                base.append(Vector(matriz[pivot]))
                # Eliminar la dependencia en otras filas
                for r in range(len(matriz)):
                    if r != pivot and matriz[r][col] != 0:
                        factor = matriz[r][col] / matriz[pivot][col]
                        pasos.append(f"Eliminando dependencia en fila {r} usando factor {factor}")
                        matriz[r] = [a - factor * b for a, b in zip(matriz[r], matriz[pivot])]
                pasos.append(f"Matriz actualizada: {matriz}")
        dimension_final = len(base)
        pasos.append(f"Base encontrada: {[str(v) for v in base]}")
        pasos.append(f"Dimensión del espacio generado: {dimension_final}")
        return base, dimension_final, pasos

class VectoresApp:
    def __init__(self, master):
        self.master = master
        self.master.title("📈 Vectores - Algebrify")
        self.master.state('zoomed')  # Iniciar en pantalla completa
        self.master.resizable(False, False)
        
        # Frame principal
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(fill='both', expand=True)
        
        # Panel izquierdo para operaciones
        self.left_panel = tk.Frame(self.main_frame, width=200, bg="#f0f0f0")
        self.left_panel.pack(side='left', fill='y')
        
        # Botón para desplegar/ocultar operaciones
        self.is_expanded = True
        self.toggle_button = tk.Button(self.left_panel, text="⬆", command=self.toggle_operations, width=2)
        self.toggle_button.pack(pady=5)
        
        # Lista de operaciones
        self.operations_frame = tk.Frame(self.left_panel, bg="#f0f0f0")
        self.operations_frame.pack(fill='x')
        
        # Botones de operaciones
        self.operation_buttons = []
        self.create_operation_buttons()
        
        # Panel derecho para pestañas
        self.right_panel = tk.Frame(self.main_frame)
        self.right_panel.pack(side='left', fill='both', expand=True)
        
        # Configurar el Notebook (pestañas)
        self.notebook = ttk.Notebook(self.right_panel)
        self.notebook.pack(expand=True, fill='both')
        
        # Inicialmente abrir la pestaña de Suma/Resta
        self.open_operation_tab("Suma/Resta")
        
        # Botón para salir
        self.create_exit_button()
    
    def toggle_operations(self):
        if self.is_expanded:
            for btn in self.operation_buttons[1:]:
                btn.pack_forget()
            self.toggle_button.config(text="▼")
            self.is_expanded = False
        else:
            for btn in self.operation_buttons:
                btn.pack(fill='x', pady=2)
            self.toggle_button.config(text="⬆")
            self.is_expanded = True
    
    def create_operation_buttons(self):
        operations = [
            "Suma/Resta",
            "Escalar",
            "Producto Punto",
            "Producto Cruz",
            "Norma",
            "Normalizar",
            "Proyección",
            "Ángulo",
            "Independencia Lineal",
            "Combinación Lineal",
            "Base y Dimensión"
        ]
        for op in operations:
            btn = tk.Button(self.operations_frame, text=op, width=20, command=lambda o=op: self.open_operation_tab(o))
            self.operation_buttons.append(btn)
        # Pack inicialmente todos los botones
        for btn in self.operation_buttons:
            btn.pack(fill='x', pady=2)
    
    def open_operation_tab(self, operation_name):
        # Crear una nueva pestaña
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=operation_name)
        
        # Botones de duplicar y cerrar
        control_frame = tk.Frame(tab)
        control_frame.pack(anchor='ne', pady=5)
        duplicate_btn = tk.Button(control_frame, text="+", command=lambda: self.open_operation_tab(operation_name))
        duplicate_btn.pack(side='left', padx=5)
        close_btn = tk.Button(control_frame, text="-", command=lambda: self.close_tab(tab))
        close_btn.pack(side='left')
        
        # Crear contenido según la operación
        if operation_name == "Suma/Resta":
            self.create_add_sub_tab(tab)
        elif operation_name == "Escalar":
            self.create_scalar_multiply_tab(tab)
        elif operation_name == "Producto Punto":
            self.create_dot_product_tab(tab)
        elif operation_name == "Producto Cruz":
            self.create_cross_product_tab(tab)
        elif operation_name == "Norma":
            self.create_magnitude_tab(tab)
        elif operation_name == "Normalizar":
            self.create_normalize_tab(tab)
        elif operation_name == "Proyección":
            self.create_projection_tab(tab)
        elif operation_name == "Ángulo":
            self.create_angle_tab(tab)
        elif operation_name == "Independencia Lineal":
            self.create_linear_independence_tab(tab)
        elif operation_name == "Combinación Lineal":
            self.create_linear_combination_tab(tab)
        elif operation_name == "Base y Dimensión":
            self.create_base_dimension_tab(tab)
        else:
            tk.Label(tab, text="Operación no definida.").pack()
        
        self.notebook.select(tab)
    
    def close_tab(self, tab):
        self.notebook.forget(tab)
    
    def create_exit_button(self):
        # Botón para salir de la aplicación
        exit_button = ttk.Button(self.master, text="🚪 Salir", command=self.master.quit, width=10)
        exit_button.pack(pady=10, side='bottom')
    
    # Métodos para crear contenido de las pestañas
    def create_add_sub_tab(self, tab):
        instructions = tk.Label(tab, text="Ingresa dos vectores para sumar o restar:", font=("Segoe UI", 14))
        instructions.pack(pady=10)
        
        # Frame para Vector 1
        v1_frame = tk.Frame(tab)
        v1_frame.pack(pady=5)
        tk.Label(v1_frame, text="Vector 1: ", font=("Segoe UI", 12)).pack(side='left', padx=5)
        v1_entry = tk.Entry(v1_frame, width=40, font=("Segoe UI", 12))
        v1_entry.pack(side='left')
        tk.Label(v1_frame, text="(ejemplo: 1,2,3)", font=("Segoe UI", 10)).pack(side='left', padx=5)
        
        # Frame para Vector 2
        v2_frame = tk.Frame(tab)
        v2_frame.pack(pady=5)
        tk.Label(v2_frame, text="Vector 2: ", font=("Segoe UI", 12)).pack(side='left', padx=5)
        v2_entry = tk.Entry(v2_frame, width=40, font=("Segoe UI", 12))
        v2_entry.pack(side='left')
        tk.Label(v2_frame, text="(ejemplo: 4,5,6)", font=("Segoe UI", 10)).pack(side='left', padx=5)
        
        # Botones de Suma y Resta
        button_frame = tk.Frame(tab)
        button_frame.pack(pady=10)
        sum_button = ttk.Button(button_frame, text="Sumar", command=lambda: self.sum_vectors(v1_entry, v2_entry, result_text))
        sum_button.pack(side='left', padx=10)
        sub_button = ttk.Button(button_frame, text="Restar", command=lambda: self.subtract_vectors(v1_entry, v2_entry, result_text))
        sub_button.pack(side='left', padx=10)
        
        # Resultado
        result_text = tk.Text(tab, height=10, width=80, state='disabled', font=("Segoe UI", 12))
        result_text.pack(pady=10)
    
    def create_scalar_multiply_tab(self, tab):
        instructions = tk.Label(tab, text="Multiplica un vector por un escalar:", font=("Segoe UI", 14))
        instructions.pack(pady=10)
        
        # Frame para Vector
        v_frame = tk.Frame(tab)
        v_frame.pack(pady=5)
        tk.Label(v_frame, text="Vector: ", font=("Segoe UI", 12)).pack(side='left', padx=5)
        v_entry = tk.Entry(v_frame, width=40, font=("Segoe UI", 12))
        v_entry.pack(side='left')
        tk.Label(v_frame, text="(ejemplo: 1,2,3)", font=("Segoe UI", 10)).pack(side='left', padx=5)
        
        # Frame para Escalar
        s_frame = tk.Frame(tab)
        s_frame.pack(pady=5)
        tk.Label(s_frame, text="Escalar: ", font=("Segoe UI", 12)).pack(side='left', padx=5)
        s_entry = tk.Entry(s_frame, width=20, font=("Segoe UI", 12))
        s_entry.pack(side='left')
        
        # Botón
        button = ttk.Button(tab, text="Multiplicar", command=lambda: self.scalar_multiply(v_entry, s_entry, result_text))
        button.pack(pady=10)
        
        # Resultado
        result_text = tk.Text(tab, height=10, width=80, state='disabled', font=("Segoe UI", 12))
        result_text.pack(pady=10)
    
    def create_dot_product_tab(self, tab):
        instructions = tk.Label(tab, text="Calcula el producto punto de dos vectores:", font=("Segoe UI", 14))
        instructions.pack(pady=10)
        
        # Frame para Vector 1
        v1_frame = tk.Frame(tab)
        v1_frame.pack(pady=5)
        tk.Label(v1_frame, text="Vector 1: ", font=("Segoe UI", 12)).pack(side='left', padx=5)
        v1_entry = tk.Entry(v1_frame, width=40, font=("Segoe UI", 12))
        v1_entry.pack(side='left')
        tk.Label(v1_frame, text="(ejemplo: 1,2,3)", font=("Segoe UI", 10)).pack(side='left', padx=5)
        
        # Frame para Vector 2
        v2_frame = tk.Frame(tab)
        v2_frame.pack(pady=5)
        tk.Label(v2_frame, text="Vector 2: ", font=("Segoe UI", 12)).pack(side='left', padx=5)
        v2_entry = tk.Entry(v2_frame, width=40, font=("Segoe UI", 12))
        v2_entry.pack(side='left')
        tk.Label(v2_frame, text="(ejemplo: 4,5,6)", font=("Segoe UI", 10)).pack(side='left', padx=5)
        
        # Botón
        button = ttk.Button(tab, text="Calcular Producto Punto", command=lambda: self.calculate_dot_product(v1_entry, v2_entry, result_text))
        button.pack(pady=10)
        
        # Resultado
        result_text = tk.Text(tab, height=15, width=80, state='disabled', font=("Segoe UI", 12))
        result_text.pack(pady=10)
    
    def create_cross_product_tab(self, tab):
        instructions = tk.Label(tab, text="Calcula el producto cruz de dos vectores (3D):", font=("Segoe UI", 14))
        instructions.pack(pady=10)
        
        # Frame para Vector 1
        v1_frame = tk.Frame(tab)
        v1_frame.pack(pady=5)
        tk.Label(v1_frame, text="Vector 1: ", font=("Segoe UI", 12)).pack(side='left', padx=5)
        v1_entry = tk.Entry(v1_frame, width=40, font=("Segoe UI", 12))
        v1_entry.pack(side='left')
        tk.Label(v1_frame, text="(ejemplo: 1,2,3)", font=("Segoe UI", 10)).pack(side='left', padx=5)
        
        # Frame para Vector 2
        v2_frame = tk.Frame(tab)
        v2_frame.pack(pady=5)
        tk.Label(v2_frame, text="Vector 2: ", font=("Segoe UI", 12)).pack(side='left', padx=5)
        v2_entry = tk.Entry(v2_frame, width=40, font=("Segoe UI", 12))
        v2_entry.pack(side='left')
        tk.Label(v2_frame, text="(ejemplo: 4,5,6)", font=("Segoe UI", 10)).pack(side='left', padx=5)
        
        # Botón
        button = ttk.Button(tab, text="Calcular Producto Cruz", command=lambda: self.calculate_cross_product(v1_entry, v2_entry, result_text))
        button.pack(pady=10)
        
        # Resultado
        result_text = tk.Text(tab, height=20, width=80, state='disabled', font=("Segoe UI", 12))
        result_text.pack(pady=10)
    
    def create_magnitude_tab(self, tab):
        instructions = tk.Label(tab, text="Calcula la norma (magnitud) de un vector:", font=("Segoe UI", 14))
        instructions.pack(pady=10)
        
        # Frame para Vector
        v_frame = tk.Frame(tab)
        v_frame.pack(pady=5)
        tk.Label(v_frame, text="Vector: ", font=("Segoe UI", 12)).pack(side='left', padx=5)
        v_entry = tk.Entry(v_frame, width=40, font=("Segoe UI", 12))
        v_entry.pack(side='left')
        tk.Label(v_frame, text="(ejemplo: 1,2,3)", font=("Segoe UI", 10)).pack(side='left', padx=5)
        
        # Botón
        button = ttk.Button(tab, text="Calcular Norma", command=lambda: self.calculate_magnitude(v_entry, result_text))
        button.pack(pady=10)
        
        # Resultado
        result_text = tk.Text(tab, height=15, width=80, state='disabled', font=("Segoe UI", 12))
        result_text.pack(pady=10)
    
    def create_normalize_tab(self, tab):
        instructions = tk.Label(tab, text="Normaliza un vector (convierte a un vector unitario):", font=("Segoe UI", 14))
        instructions.pack(pady=10)
        
        # Frame para Vector
        v_frame = tk.Frame(tab)
        v_frame.pack(pady=5)
        tk.Label(v_frame, text="Vector: ", font=("Segoe UI", 12)).pack(side='left', padx=5)
        v_entry = tk.Entry(v_frame, width=40, font=("Segoe UI", 12))
        v_entry.pack(side='left')
        tk.Label(v_frame, text="(ejemplo: 1,2,3)", font=("Segoe UI", 10)).pack(side='left', padx=5)
        
        # Botón
        button = ttk.Button(tab, text="Normalizar", command=lambda: self.normalize_vector(v_entry, result_text))
        button.pack(pady=10)
        
        # Resultado
        result_text = tk.Text(tab, height=20, width=80, state='disabled', font=("Segoe UI", 12))
        result_text.pack(pady=10)
    
    def create_projection_tab(self, tab):
        instructions = tk.Label(tab, text="Proyecta un vector sobre otro:", font=("Segoe UI", 14))
        instructions.pack(pady=10)
        
        # Frame para Vector 1
        v1_frame = tk.Frame(tab)
        v1_frame.pack(pady=5)
        tk.Label(v1_frame, text="Vector a Proyectar: ", font=("Segoe UI", 12)).pack(side='left', padx=5)
        v1_entry = tk.Entry(v1_frame, width=40, font=("Segoe UI", 12))
        v1_entry.pack(side='left')
        tk.Label(v1_frame, text="(ejemplo: 1,2,3)", font=("Segoe UI", 10)).pack(side='left', padx=5)
        
        # Frame para Vector 2
        v2_frame = tk.Frame(tab)
        v2_frame.pack(pady=5)
        tk.Label(v2_frame, text="Vector Base: ", font=("Segoe UI", 12)).pack(side='left', padx=5)
        v2_entry = tk.Entry(v2_frame, width=40, font=("Segoe UI", 12))
        v2_entry.pack(side='left')
        tk.Label(v2_frame, text="(ejemplo: 4,5,6)", font=("Segoe UI", 10)).pack(side='left', padx=5)
        
        # Botón
        button = ttk.Button(tab, text="Calcular Proyección", command=lambda: self.calculate_projection(v1_entry, v2_entry, result_text))
        button.pack(pady=10)
        
        # Resultado
        result_text = tk.Text(tab, height=20, width=80, state='disabled', font=("Segoe UI", 12))
        result_text.pack(pady=10)
    
    def create_angle_tab(self, tab):
        instructions = tk.Label(tab, text="Calcula el ángulo entre dos vectores:", font=("Segoe UI", 14))
        instructions.pack(pady=10)
        
        # Frame para Vector 1
        v1_frame = tk.Frame(tab)
        v1_frame.pack(pady=5)
        tk.Label(v1_frame, text="Vector 1: ", font=("Segoe UI", 12)).pack(side='left', padx=5)
        v1_entry = tk.Entry(v1_frame, width=40, font=("Segoe UI", 12))
        v1_entry.pack(side='left')
        tk.Label(v1_frame, text="(ejemplo: 1,2,3)", font=("Segoe UI", 10)).pack(side='left', padx=5)
        
        # Frame para Vector 2
        v2_frame = tk.Frame(tab)
        v2_frame.pack(pady=5)
        tk.Label(v2_frame, text="Vector 2: ", font=("Segoe UI", 12)).pack(side='left', padx=5)
        v2_entry = tk.Entry(v2_frame, width=40, font=("Segoe UI", 12))
        v2_entry.pack(side='left')
        tk.Label(v2_frame, text="(ejemplo: 4,5,6)", font=("Segoe UI", 10)).pack(side='left', padx=5)
        
        # Botón
        button = ttk.Button(tab, text="Calcular Ángulo", command=lambda: self.calculate_angle(v1_entry, v2_entry, result_text))
        button.pack(pady=10)
        
        # Resultado
        result_text = tk.Text(tab, height=20, width=80, state='disabled', font=("Segoe UI", 12))
        result_text.pack(pady=10)
    
    def create_linear_independence_tab(self, tab):
        instructions = tk.Label(tab, text="Determina si un conjunto de vectores es linealmente independiente:", font=("Segoe UI", 14))
        instructions.pack(pady=10)
        
        # Frame para Vectores
        vectors_frame = tk.Frame(tab)
        vectors_frame.pack(pady=5)
        tk.Label(vectors_frame, text="Vectores (separados por ';'): ", font=("Segoe UI", 12)).pack(side='left', padx=5)
        vectors_entry = tk.Entry(vectors_frame, width=50, font=("Segoe UI", 12))
        vectors_entry.pack(side='left')
        tk.Label(vectors_frame, text="(ejemplo: 1,2,3;4,5,6;7,8,9)", font=("Segoe UI", 10)).pack(side='left', padx=5)
        
        # Botón
        button = ttk.Button(tab, text="Verificar Independencia", command=lambda: self.check_linear_independence(vectors_entry, result_text))
        button.pack(pady=10)
        
        # Resultado
        result_text = tk.Text(tab, height=25, width=80, state='disabled', font=("Segoe UI", 12))
        result_text.pack(pady=10)
    
    def create_linear_combination_tab(self, tab):
        instructions = tk.Label(tab, text="Construye una combinación lineal de vectores:", font=("Segoe UI", 14))
        instructions.pack(pady=10)
        
        # Frame para Vectores
        vectors_frame = tk.Frame(tab)
        vectors_frame.pack(pady=5)
        tk.Label(vectors_frame, text="Vectores (separados por ';'): ", font=("Segoe UI", 12)).pack(side='left', padx=5)
        vectors_entry = tk.Entry(vectors_frame, width=50, font=("Segoe UI", 12))
        vectors_entry.pack(side='left')
        tk.Label(vectors_frame, text="(ejemplo: 1,2,3;4,5,6)", font=("Segoe UI", 10)).pack(side='left', padx=5)
        
        # Frame para Escalares
        scalars_frame = tk.Frame(tab)
        scalars_frame.pack(pady=5)
        tk.Label(scalars_frame, text="Escalares (separados por ','): ", font=("Segoe UI", 12)).pack(side='left', padx=5)
        scalars_entry = tk.Entry(scalars_frame, width=50, font=("Segoe UI", 12))
        scalars_entry.pack(side='left')
        tk.Label(scalars_frame, text="(ejemplo: 2,3)", font=("Segoe UI", 10)).pack(side='left', padx=5)
        
        # Botón
        button = ttk.Button(tab, text="Construir Combinación", command=lambda: self.construct_linear_combination(vectors_entry, scalars_entry, result_text))
        button.pack(pady=10)
        
        # Resultado
        result_text = tk.Text(tab, height=25, width=80, state='disabled', font=("Segoe UI", 12))
        result_text.pack(pady=10)
    
    def create_base_dimension_tab(self, tab):
        instructions = tk.Label(tab, text="Determina una base y la dimensión del espacio generado por vectores:", font=("Segoe UI", 14))
        instructions.pack(pady=10)
        
        # Frame para Vectores
        vectors_frame = tk.Frame(tab)
        vectors_frame.pack(pady=5)
        tk.Label(vectors_frame, text="Vectores (separados por ';'): ", font=("Segoe UI", 12)).pack(side='left', padx=5)
        vectors_entry = tk.Entry(vectors_frame, width=50, font=("Segoe UI", 12))
        vectors_entry.pack(side='left')
        tk.Label(vectors_frame, text="(ejemplo: 1,2,3;4,5,6;7,8,9)", font=("Segoe UI", 10)).pack(side='left', padx=5)
        
        # Botón
        button = ttk.Button(tab, text="Determinar Base y Dimensión", command=lambda: self.determine_base_dimension(vectors_entry, result_text))
        button.pack(pady=10)
        
        # Resultado
        result_text = tk.Text(tab, height=30, width=80, state='disabled', font=("Segoe UI", 12))
        result_text.pack(pady=10)
    
    # Métodos para operaciones
    def parse_vector(self, entry):
        """
        Parsea una cadena de texto en una lista de componentes del vector.
        """
        try:
            componentes = [float(x.strip()) for x in entry.split(",")]
            return componentes
        except ValueError:
            raise ValueError("Los componentes del vector deben ser números separados por comas.")
    
    def sum_vectors(self, v1_entry, v2_entry, result_text):
        try:
            v1 = Vector(self.parse_vector(v1_entry.get()))
            v2 = Vector(self.parse_vector(v2_entry.get()))
            resultado, pasos = v1 + v2
            result_text.config(state='normal')
            result_text.delete("1.0", tk.END)
            for paso in pasos:
                result_text.insert(tk.END, paso + "\n")
            result_text.insert(tk.END, f"Vector Resultante: {resultado}\n")
            result_text.config(state='disabled')
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def subtract_vectors(self, v1_entry, v2_entry, result_text):
        try:
            v1 = Vector(self.parse_vector(v1_entry.get()))
            v2 = Vector(self.parse_vector(v2_entry.get()))
            resultado, pasos = v1 - v2
            result_text.config(state='normal')
            result_text.delete("1.0", tk.END)
            for paso in pasos:
                result_text.insert(tk.END, paso + "\n")
            result_text.insert(tk.END, f"Vector Resultante: {resultado}\n")
            result_text.config(state='disabled')
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def scalar_multiply(self, v_entry, s_entry, result_text):
        try:
            v = Vector(self.parse_vector(v_entry.get()))
            escalar = float(s_entry.get())
            resultado, pasos = v.scalar_multiply(escalar)
            result_text.config(state='normal')
            result_text.delete("1.0", tk.END)
            for paso in pasos:
                result_text.insert(tk.END, paso + "\n")
            result_text.insert(tk.END, f"Vector Resultante: {resultado}\n")
            result_text.config(state='disabled')
        except ValueError:
            messagebox.showerror("Error", "El escalar debe ser un número.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def calculate_dot_product(self, v1_entry, v2_entry, result_text):
        try:
            v1 = Vector(self.parse_vector(v1_entry.get()))
            v2 = Vector(self.parse_vector(v2_entry.get()))
            resultado, pasos = v1.dot_product(v2)
            result_text.config(state='normal')
            result_text.delete("1.0", tk.END)
            for paso in pasos:
                result_text.insert(tk.END, paso + "\n")
            result_text.insert(tk.END, f"Producto Punto: {resultado}\n")
            result_text.config(state='disabled')
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def calculate_cross_product(self, v1_entry, v2_entry, result_text):
        try:
            v1 = Vector(self.parse_vector(v1_entry.get()))
            v2 = Vector(self.parse_vector(v2_entry.get()))
            resultado, pasos = v1.cross_product(v2)
            result_text.config(state='normal')
            result_text.delete("1.0", tk.END)
            for paso in pasos:
                result_text.insert(tk.END, paso + "\n")
            result_text.insert(tk.END, f"Producto Cruz: {resultado}\n")
            result_text.config(state='disabled')
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def calculate_magnitude(self, v_entry, result_text):
        try:
            v = Vector(self.parse_vector(v_entry.get()))
            resultado, pasos = v.magnitude()
            result_text.config(state='normal')
            result_text.delete("1.0", tk.END)
            for paso in pasos:
                result_text.insert(tk.END, paso + "\n")
            result_text.insert(tk.END, f"Norma: {resultado}\n")
            result_text.config(state='disabled')
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def normalize_vector(self, v_entry, result_text):
        try:
            v = Vector(self.parse_vector(v_entry.get()))
            resultado, pasos = v.normalize()
            result_text.config(state='normal')
            result_text.delete("1.0", tk.END)
            for paso in pasos:
                result_text.insert(tk.END, paso + "\n")
            result_text.insert(tk.END, f"Vector Normalizado: {resultado}\n")
            result_text.config(state='disabled')
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def calculate_projection(self, v1_entry, v2_entry, result_text):
        try:
            v1 = Vector(self.parse_vector(v1_entry.get()))
            v2 = Vector(self.parse_vector(v2_entry.get()))
            resultado, pasos = v1.projection_onto(v2)
            result_text.config(state='normal')
            result_text.delete("1.0", tk.END)
            for paso in pasos:
                result_text.insert(tk.END, paso + "\n")
            result_text.insert(tk.END, f"Proyección de {v1} sobre {v2}: {resultado}\n")
            result_text.config(state='disabled')
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def calculate_angle(self, v1_entry, v2_entry, result_text):
        try:
            v1 = Vector(self.parse_vector(v1_entry.get()))
            v2 = Vector(self.parse_vector(v2_entry.get()))
            angle, pasos = v1.angle_with(v2)
            result_text.config(state='normal')
            result_text.delete("1.0", tk.END)
            for paso in pasos:
                result_text.insert(tk.END, paso + "\n")
            result_text.insert(tk.END, f"Ángulo entre {v1} y {v2}: {angle:.2f} grados\n")
            result_text.config(state='disabled')
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def check_linear_independence(self, vectors_entry, result_text):
        try:
            vectores_str = vectors_entry.get()
            vectores = [Vector(self.parse_vector(v.strip())) for v in vectores_str.split(";")]
            independientes, pasos = Vector.are_linearly_independent(vectores)
            result_text.config(state='normal')
            result_text.delete("1.0", tk.END)
            for paso in pasos:
                result_text.insert(tk.END, paso + "\n")
            if independientes:
                result_text.insert(tk.END, "Los vectores son linealmente independientes.\n")
            else:
                result_text.insert(tk.END, "Los vectores NO son linealmente independientes.\n")
            result_text.config(state='disabled')
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def construct_linear_combination(self, vectors_entry, scalars_entry, result_text):
        try:
            vectores_str = vectors_entry.get()
            escalares_str = scalars_entry.get()
            vectores = [Vector(self.parse_vector(v.strip())) for v in vectores_str.split(";")]
            escalares = [float(s.strip()) for s in escalares_str.split(",")]
            resultado, pasos = Vector.linear_combination(vectores, escalares)
            result_text.config(state='normal')
            result_text.delete("1.0", tk.END)
            for paso in pasos:
                result_text.insert(tk.END, paso + "\n")
            result_text.insert(tk.END, f"Combinación Lineal: {resultado}\n")
            result_text.config(state='disabled')
        except ValueError:
            messagebox.showerror("Error", "Los escalares deben ser números separados por comas.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def determine_base_dimension(self, vectors_entry, result_text):
        try:
            vectores_str = vectors_entry.get()
            vectores = [Vector(self.parse_vector(v.strip())) for v in vectores_str.split(";")]
            base, dimension, pasos = Vector.base_and_dimension(vectores)
            result_text.config(state='normal')
            result_text.delete("1.0", tk.END)
            for paso in pasos:
                result_text.insert(tk.END, paso + "\n")
            base_str = ', '.join(str(v) for v in base)
            result_text.insert(tk.END, f"Base: {base_str}\nDimensión: {dimension}\n")
            result_text.config(state='disabled')
        except Exception as e:
            messagebox.showerror("Error", str(e))

def main():
    root = tk.Tk()
    app = VectoresApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
