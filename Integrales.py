# Integrales.py
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from sympy import symbols, sympify, integrate, Matrix, lambdify
from sympy.vector import CoordSys3D
import numpy as np

class IntegralesApp:
    def __init__(self, master):
        self.master = master
        self.master.title("∫ Integrales - Algebrify")
        self.master.geometry("900x700")
        self.master.resizable(False, False)
        
        # Estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Segoe UI', 12), padding=10)
        self.style.configure('TLabel', font=('Segoe UI', 14))
        self.style.configure('TEntry', font=('Segoe UI', 12))
        self.style.configure('TNotebook.Tab', font=('Segoe UI', 12, 'bold'))
        
        # Título
        title_label = ttk.Label(master, text="∫ Integrales en Álgebra Lineal", font=("Segoe UI", 20, "bold"))
        title_label.pack(pady=20)
        
        # Notebook (pestañas)
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Crear pestañas para cada tema
        self.create_vector_functions_tab()
        self.create_projections_tab()
        self.create_matrix_integrals_tab()
        self.create_line_integral_tab()
        self.create_surface_volume_integral_tab()
        self.create_determinant_integral_tab()
        self.create_eigen_integral_tab()
        
        # Botón para cerrar
        close_button = ttk.Button(master, text="🔙 Volver", command=self.master.destroy)
        close_button.pack(pady=10)
    
    def create_vector_functions_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Funciones Vectoriales")
        
        # Instrucciones
        instructions = (
            "Ingresa una función vectorial f(t) en términos de t.\n"
            "Ejemplo: [t, t**2, sin(t)]"
        )
        instr_label = ttk.Label(tab, text=instructions, wraplength=800, justify='left')
        instr_label.pack(pady=10)
        
        # Entrada de función vectorial
        func_label = ttk.Label(tab, text="f(t) = ")
        func_label.pack(anchor='w', padx=10)
        self.vector_func_entry = ttk.Entry(tab, width=100)
        self.vector_func_entry.pack(padx=10, pady=5)
        
        # Intervalo de integración
        interval_frame = ttk.Frame(tab)
        interval_frame.pack(pady=10, anchor='w', padx=10)
        ttk.Label(interval_frame, text="Intervalo de Integración: ").pack(side='left')
        ttk.Label(interval_frame, text="a=").pack(side='left')
        self.vector_a_entry = ttk.Entry(interval_frame, width=10)
        self.vector_a_entry.pack(side='left', padx=5)
        ttk.Label(interval_frame, text="b=").pack(side='left')
        self.vector_b_entry = ttk.Entry(interval_frame, width=10)
        self.vector_b_entry.pack(side='left', padx=5)
        
        # Botón para calcular
        calc_button = ttk.Button(tab, text="Calcular Integral", command=self.calculate_vector_integral)
        calc_button.pack(pady=10)
        
        # Área de resultados
        result_label = ttk.Label(tab, text="Resultado:")
        result_label.pack(anchor='w', padx=10)
        self.vector_result = scrolledtext.ScrolledText(tab, height=10, width=100, state='disabled', font=("Segoe UI", 12))
        self.vector_result.pack(padx=10, pady=5)
    
    def calculate_vector_integral(self):
        func_str = self.vector_func_entry.get()
        a_str = self.vector_a_entry.get()
        b_str = self.vector_b_entry.get()
        
        if not func_str or not a_str or not b_str:
            messagebox.showerror("Error", "Por favor, completa todos los campos.")
            return
        
        try:
            a = float(a_str)
            b = float(b_str)
        except ValueError:
            messagebox.showerror("Error", "Los límites de integración deben ser números.")
            return
        
        try:
            # Parsear la función vectorial
            func_list = sympify(func_str)
            if not isinstance(func_list, (list, tuple, Matrix)):
                raise ValueError("La función vectorial debe ser una lista, tupla o matriz.")
            if len(func_list) == 0:
                raise ValueError("La función vectorial no puede estar vacía.")
            
            t = symbols('t')
            integral_components = []
            for component in func_list:
                integral = integrate(component, (t, a, b))
                integral_components.append(integral)
            
            # Mostrar el resultado
            result_str = f"∫ₐᵇ f(t) dt = [{', '.join([str(comp) for comp in integral_components])}]"
            self.vector_result.configure(state='normal')
            self.vector_result.delete('1.0', tk.END)
            self.vector_result.insert(tk.END, result_str)
            self.vector_result.configure(state='disabled')
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular la integral: {e}")
    
    def create_projections_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Proyecciones Ortogonales")
        
        # Instrucciones
        instructions = (
            "Calcula el producto interno y la proyección ortogonal de dos funciones f(t) y g(t) en el intervalo [a, b].\n"
            "Ejemplo de f(t): t\n"
            "Ejemplo de g(t): t**2"
        )
        instr_label = ttk.Label(tab, text=instructions, wraplength=800, justify='left')
        instr_label.pack(pady=10)
        
        # Función f(t)
        f_label = ttk.Label(tab, text="f(t) = ")
        f_label.pack(anchor='w', padx=10)
        self.proj_f_entry = ttk.Entry(tab, width=100)
        self.proj_f_entry.pack(padx=10, pady=5)
        
        # Función g(t)
        g_label = ttk.Label(tab, text="g(t) = ")
        g_label.pack(anchor='w', padx=10)
        self.proj_g_entry = ttk.Entry(tab, width=100)
        self.proj_g_entry.pack(padx=10, pady=5)
        
        # Intervalo de integración
        interval_frame = ttk.Frame(tab)
        interval_frame.pack(pady=10, anchor='w', padx=10)
        ttk.Label(interval_frame, text="Intervalo de Integración: ").pack(side='left')
        ttk.Label(interval_frame, text="a=").pack(side='left')
        self.proj_a_entry = ttk.Entry(interval_frame, width=10)
        self.proj_a_entry.pack(side='left', padx=5)
        ttk.Label(interval_frame, text="b=").pack(side='left')
        self.proj_b_entry = ttk.Entry(interval_frame, width=10)
        self.proj_b_entry.pack(side='left', padx=5)
        
        # Botón para calcular
        calc_button = ttk.Button(tab, text="Calcular Proyección", command=self.calculate_projections)
        calc_button.pack(pady=10)
        
        # Área de resultados
        result_label = ttk.Label(tab, text="Resultado:")
        result_label.pack(anchor='w', padx=10)
        self.proj_result = scrolledtext.ScrolledText(tab, height=15, width=100, state='disabled', font=("Segoe UI", 12))
        self.proj_result.pack(padx=10, pady=5)
    
    def calculate_projections(self):
        f_str = self.proj_f_entry.get()
        g_str = self.proj_g_entry.get()
        a_str = self.proj_a_entry.get()
        b_str = self.proj_b_entry.get()
        
        if not f_str or not g_str or not a_str or not b_str:
            messagebox.showerror("Error", "Por favor, completa todos los campos.")
            return
        
        try:
            a = float(a_str)
            b = float(b_str)
        except ValueError:
            messagebox.showerror("Error", "Los límites de integración deben ser números.")
            return
        
        try:
            t = symbols('t')
            f = sympify(f_str)
            g = sympify(g_str)
            
            # Producto interno ⟨f, g⟩ = ∫ₐᵇ f(t)*g(t) dt
            inner_product = integrate(f * g, (t, a, b))
            
            # Norma de f: ⟨f, f⟩ = ∫ₐᵇ f(t)**2 dt
            norm_f = integrate(f**2, (t, a, b))
            if norm_f == 0:
                raise ValueError("La norma de f(t) es cero, no se puede proyectar.")
            
            # Proyección de g sobre f: (⟨g, f⟩ / ⟨f, f⟩) * f(t)
            projection_coeff = inner_product / norm_f
            projection = projection_coeff * f
            
            # Mostrar resultados
            result_str = (
                f"⟨f, g⟩ = ∫ₐᵇ f(t)*g(t) dt = {inner_product}\n"
                f"⟨f, f⟩ = ∫ₐᵇ f(t)**2 dt = {norm_f}\n"
                f"Proyección de g sobre f: (⟨g, f⟩ / ⟨f, f⟩) * f(t) = {projection}"
            )
            self.proj_result.configure(state='normal')
            self.proj_result.delete('1.0', tk.END)
            self.proj_result.insert(tk.END, result_str)
            self.proj_result.configure(state='disabled')
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular las proyecciones: {e}")
    
    def create_matrix_integrals_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Integrales de Matrices")
        
        # Instrucciones
        instructions = (
            "Ingresa una función matricial A(t) donde cada elemento es una función de t.\n"
            "Ejemplo para una matriz 2x2:\n"
            "[[t, 0], [0, t**2]]"
        )
        instr_label = ttk.Label(tab, text=instructions, wraplength=800, justify='left')
        instr_label.pack(pady=10)
        
        # Entrada de matriz
        matrix_label = ttk.Label(tab, text="A(t) = ")
        matrix_label.pack(anchor='w', padx=10)
        self.matrix_entry = ttk.Entry(tab, width=100)
        self.matrix_entry.pack(padx=10, pady=5)
        
        # Intervalo de integración
        interval_frame = ttk.Frame(tab)
        interval_frame.pack(pady=10, anchor='w', padx=10)
        ttk.Label(interval_frame, text="Intervalo de Integración: ").pack(side='left')
        ttk.Label(interval_frame, text="a=").pack(side='left')
        self.matrix_a_entry = ttk.Entry(interval_frame, width=10)
        self.matrix_a_entry.pack(side='left', padx=5)
        ttk.Label(interval_frame, text="b=").pack(side='left')
        self.matrix_b_entry = ttk.Entry(interval_frame, width=10)
        self.matrix_b_entry.pack(side='left', padx=5)
        
        # Botón para calcular
        calc_button = ttk.Button(tab, text="Calcular Integral de la Matriz", command=self.calculate_matrix_integral)
        calc_button.pack(pady=10)
        
        # Área de resultados
        result_label = ttk.Label(tab, text="Resultado:")
        result_label.pack(anchor='w', padx=10)
        self.matrix_result = scrolledtext.ScrolledText(tab, height=15, width=100, state='disabled', font=("Segoe UI", 12))
        self.matrix_result.pack(padx=10, pady=5)
    
    def calculate_matrix_integral(self):
        matrix_str = self.matrix_entry.get()
        a_str = self.matrix_a_entry.get()
        b_str = self.matrix_b_entry.get()
        
        if not matrix_str or not a_str or not b_str:
            messagebox.showerror("Error", "Por favor, completa todos los campos.")
            return
        
        try:
            a = float(a_str)
            b = float(b_str)
        except ValueError:
            messagebox.showerror("Error", "Los límites de integración deben ser números.")
            return
        
        try:
            # Parsear la matriz
            matrix_list = sympify(matrix_str)
            if not isinstance(matrix_list, (list, tuple, Matrix)):
                raise ValueError("La matriz debe ser una lista, tupla o matriz de SymPy.")
            matrix = Matrix(matrix_list)
            rows, cols = matrix.shape
            
            # Integrar cada elemento
            integral_matrix = Matrix(rows, cols, lambda i, j: integrate(matrix[i, j], (symbols('t'), a, b)))
            
            # Mostrar el resultado
            result_str = f"∫ₐᵇ A(t) dt =\n{integral_matrix}"
            self.matrix_result.configure(state='normal')
            self.matrix_result.delete('1.0', tk.END)
            self.matrix_result.insert(tk.END, result_str)
            self.matrix_result.configure(state='disabled')
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular la integral de la matriz: {e}")
    
    def create_line_integral_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Integral de Línea")
        
        # Instrucciones
        instructions = (
            "Calcula la integral de línea ∫ F · dr sobre una curva parametrizada r(t).\n"
            "Ingresa:\n"
            "- Vector de campo F(x, y, z)\n"
            "- Parametrización de la curva r(t) en términos de t\n"
            "- Intervalo de t [a, b]"
        )
        instr_label = ttk.Label(tab, text=instructions, wraplength=800, justify='left')
        instr_label.pack(pady=10)
        
        # Campo vectorial F
        F_label = ttk.Label(tab, text="F(x, y, z) = ")
        F_label.pack(anchor='w', padx=10)
        self.F_entry = ttk.Entry(tab, width=100)
        self.F_entry.pack(padx=10, pady=5)
        
        # Parametrización r(t)
        r_label = ttk.Label(tab, text="r(t) = ")
        r_label.pack(anchor='w', padx=10)
        self.r_entry = ttk.Entry(tab, width=100)
        self.r_entry.pack(padx=10, pady=5)
        
        # Intervalo de t
        interval_frame = ttk.Frame(tab)
        interval_frame.pack(pady=10, anchor='w', padx=10)
        ttk.Label(interval_frame, text="Intervalo de t: ").pack(side='left')
        ttk.Label(interval_frame, text="a=").pack(side='left')
        self.line_a_entry = ttk.Entry(interval_frame, width=10)
        self.line_a_entry.pack(side='left', padx=5)
        ttk.Label(interval_frame, text="b=").pack(side='left')
        self.line_b_entry = ttk.Entry(interval_frame, width=10)
        self.line_b_entry.pack(side='left', padx=5)
        
        # Botón para calcular
        calc_button = ttk.Button(tab, text="Calcular Integral de Línea", command=self.calculate_line_integral)
        calc_button.pack(pady=10)
        
        # Área de resultados
        result_label = ttk.Label(tab, text="Resultado:")
        result_label.pack(anchor='w', padx=10)
        self.line_result = scrolledtext.ScrolledText(tab, height=15, width=100, state='disabled', font=("Segoe UI", 12))
        self.line_result.pack(padx=10, pady=5)
    
    def calculate_line_integral(self):
        F_str = self.F_entry.get()
        r_str = self.r_entry.get()
        a_str = self.line_a_entry.get()
        b_str = self.line_b_entry.get()
        
        if not F_str or not r_str or not a_str or not b_str:
            messagebox.showerror("Error", "Por favor, completa todos los campos.")
            return
        
        try:
            a = float(a_str)
            b = float(b_str)
        except ValueError:
            messagebox.showerror("Error", "Los límites de integración deben ser números.")
            return
        
        try:
            t = symbols('t')
            # Definir el sistema de coordenadas
            N = CoordSys3D('N')
            
            # Parsear el campo vectorial F
            F_components = sympify(F_str)
            if not isinstance(F_components, (list, tuple, Matrix)):
                raise ValueError("El campo vectorial debe ser una lista, tupla o matriz de SymPy.")
            F = Matrix(F_components)
            if F.shape[0] not in [2,3]:
                raise ValueError("El campo vectorial debe tener 2 o 3 componentes.")
            
            # Parsear la parametrización r(t)
            r_components = sympify(r_str)
            if not isinstance(r_components, (list, tuple, Matrix)):
                raise ValueError("La parametrización r(t) debe ser una lista, tupla o matriz de SymPy.")
            r = Matrix(r_components)
            if r.shape[0] not in [2,3]:
                raise ValueError("La parametrización r(t) debe tener 2 o 3 componentes.")
            
            # Calcular dr/dt
            dr_dt = r.diff(t)
            
            # Sustituir x, y, z en F con r(t)
            if r.shape[0] == 2:
                F_sub = Matrix([F[0].subs({'x': r[0], 'y': r[1]}),
                                F[1].subs({'x': r[0], 'y': r[1]})])
            else:
                F_sub = Matrix([F[0].subs({'x': r[0], 'y': r[1], 'z': r[2]}),
                                F[1].subs({'x': r[0], 'y': r[1], 'z': r[2]}),
                                F[2].subs({'x': r[0], 'y': r[1], 'z': r[2]})])
            
            # Producto punto F(r(t)) · dr/dt
            dot_product = sum([F_sub[i] * dr_dt[i] for i in range(r.shape[0])])
            
            # Integrar el producto punto
            integral = integrate(dot_product, (t, a, b))
            
            # Mostrar el resultado
            result_str = f"Integral de Línea ∫ F · dr = {integral}"
            self.line_result.configure(state='normal')
            self.line_result.delete('1.0', tk.END)
            self.line_result.insert(tk.END, result_str)
            self.line_result.configure(state='disabled')
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular la integral de línea: {e}")
    
    def create_surface_volume_integral_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Superficie y Volumen")
        
        # Instrucciones
        instructions = (
            "Calcula integrales de superficie o volumen.\n"
            "Para integrales de superficie:\n"
            "- Ingresa un campo vectorial F(x, y, z).\n"
            "- Ingresa una parametrización de la superficie r(u, v).\n"
            "- Intervalos de u y v.\n\n"
            "Para integrales de volumen:\n"
            "- Ingresa una función escalar f(x, y, z).\n"
            "- Define los límites de integración."
        )
        instr_label = ttk.Label(tab, text=instructions, wraplength=800, justify='left')
        instr_label.pack(pady=10)
        
        # Selección de tipo de integral
        integral_type = tk.StringVar(value="Superficie")
        type_frame = ttk.Frame(tab)
        type_frame.pack(pady=5, anchor='w', padx=10)
        ttk.Radiobutton(type_frame, text="Integral de Superficie", variable=integral_type, value="Superficie").pack(side='left', padx=5)
        ttk.Radiobutton(type_frame, text="Integral de Volumen", variable=integral_type, value="Volumen").pack(side='left', padx=5)
        
        # Frame para inputs de superficie
        self.surface_frame = ttk.Frame(tab)
        self.surface_frame.pack(pady=10, fill='x', padx=10)
        
        # Campos para integral de superficie
        self.F_surface_label = ttk.Label(self.surface_frame, text="F(x, y, z) = ")
        self.F_surface_label.grid(row=0, column=0, sticky='w', pady=2)
        self.F_surface_entry = ttk.Entry(self.surface_frame, width=80)
        self.F_surface_entry.grid(row=0, column=1, pady=2)
        
        self.r_surface_label = ttk.Label(self.surface_frame, text="r(u, v) = ")
        self.r_surface_label.grid(row=1, column=0, sticky='w', pady=2)
        self.r_surface_entry = ttk.Entry(self.surface_frame, width=80)
        self.r_surface_entry.grid(row=1, column=1, pady=2)
        
        self.u_limits_label = ttk.Label(self.surface_frame, text="Intervalo de u: a, b")
        self.u_limits_label.grid(row=2, column=0, sticky='w', pady=2)
        self.u_a_entry = ttk.Entry(self.surface_frame, width=10)
        self.u_a_entry.grid(row=2, column=1, sticky='w', pady=2)
        self.u_b_entry = ttk.Entry(self.surface_frame, width=10)
        self.u_b_entry.grid(row=2, column=1, sticky='e', pady=2)
        
        self.v_limits_label = ttk.Label(self.surface_frame, text="Intervalo de v: c, d")
        self.v_limits_label.grid(row=3, column=0, sticky='w', pady=2)
        self.v_c_entry = ttk.Entry(self.surface_frame, width=10)
        self.v_c_entry.grid(row=3, column=1, sticky='w', pady=2)
        self.v_d_entry = ttk.Entry(self.surface_frame, width=10)
        self.v_d_entry.grid(row=3, column=1, sticky='e', pady=2)
        
        # Frame para inputs de volumen
        self.volume_frame = ttk.Frame(tab)
        # No se empaqueta inicialmente
        
        self.F_volume_label = ttk.Label(self.volume_frame, text="f(x, y, z) = ")
        self.F_volume_label.grid(row=0, column=0, sticky='w', pady=2)
        self.F_volume_entry = ttk.Entry(self.volume_frame, width=80)
        self.F_volume_entry.grid(row=0, column=1, pady=2)
        
        self.x_limits_label = ttk.Label(self.volume_frame, text="x: a, b")
        self.x_limits_label.grid(row=1, column=0, sticky='w', pady=2)
        self.x_a_entry = ttk.Entry(self.volume_frame, width=10)
        self.x_a_entry.grid(row=1, column=1, sticky='w', pady=2)
        self.x_b_entry = ttk.Entry(self.volume_frame, width=10)
        self.x_b_entry.grid(row=1, column=1, sticky='e', pady=2)
        
        self.y_limits_label = ttk.Label(self.volume_frame, text="y: c, d")
        self.y_limits_label.grid(row=2, column=0, sticky='w', pady=2)
        self.y_c_entry = ttk.Entry(self.volume_frame, width=10)
        self.y_c_entry.grid(row=2, column=1, sticky='w', pady=2)
        self.y_d_entry = ttk.Entry(self.volume_frame, width=10)
        self.y_d_entry.grid(row=2, column=1, sticky='e', pady=2)
        
        self.z_limits_label = ttk.Label(self.volume_frame, text="z: e, f")
        self.z_limits_label.grid(row=3, column=0, sticky='w', pady=2)
        self.z_e_entry = ttk.Entry(self.volume_frame, width=10)
        self.z_e_entry.grid(row=3, column=1, sticky='w', pady=2)
        self.z_f_entry = ttk.Entry(self.volume_frame, width=10)
        self.z_f_entry.grid(row=3, column=1, sticky='e', pady=2)
        
        # Botón para calcular
        calc_button = ttk.Button(tab, text="Calcular Integral", command=lambda: self.calculate_surface_volume_integral(integral_type.get()))
        calc_button.pack(pady=10)
        
        # Área de resultados
        result_label = ttk.Label(tab, text="Resultado:")
        result_label.pack(anchor='w', padx=10)
        self.surface_volume_result = scrolledtext.ScrolledText(tab, height=15, width=100, state='disabled', font=("Segoe UI", 12))
        self.surface_volume_result.pack(padx=10, pady=5)
        
        # Cambiar la interfaz según el tipo de integral seleccionada
        def toggle_integral_type():
            if integral_type.get() == "Superficie":
                self.volume_frame.pack_forget()
                self.surface_frame.pack(pady=10, fill='x', padx=10)
            else:
                self.surface_frame.pack_forget()
                self.volume_frame.pack(pady=10, fill='x', padx=10)
        
        integral_type.trace('w', lambda *args: toggle_integral_type())
        toggle_integral_type()  # Inicializar
        
    def calculate_surface_volume_integral(self, integral_type):
        try:
            if integral_type == "Superficie":
                F_str = self.F_surface_entry.get()
                r_str = self.r_surface_entry.get()
                a_str = self.u_a_entry.get()
                b_str = self.u_b_entry.get()
                c_str = self.v_c_entry.get()
                d_str = self.v_d_entry.get()
                
                if not F_str or not r_str or not a_str or not b_str or not c_str or not d_str:
                    messagebox.showerror("Error", "Por favor, completa todos los campos para la integral de superficie.")
                    return
                
                a = float(a_str)
                b = float(b_str)
                c = float(c_str)
                d = float(d_str)
                
                # Parsear F(x, y, z)
                F_components = sympify(F_str)
                if not isinstance(F_components, (list, tuple, Matrix)):
                    raise ValueError("El campo vectorial F debe ser una lista, tupla o matriz de SymPy.")
                F = Matrix(F_components)
                if F.shape[0] not in [2,3]:
                    raise ValueError("El campo vectorial F debe tener 2 o 3 componentes.")
                
                # Parsear r(u, v)
                r_components = sympify(r_str)
                if not isinstance(r_components, (list, tuple, Matrix)):
                    raise ValueError("La parametrización r(u, v) debe ser una lista, tupla o matriz de SymPy.")
                r = Matrix(r_components)
                if r.shape[0] != 3:
                    raise ValueError("La parametrización r(u, v) debe tener 3 componentes (x, y, z).")
                
                u, v = symbols('u v')
                dr_du = r.diff(u)
                dr_dv = r.diff(v)
                
                # Calcular el producto vectorial dr_du x dr_dv
                cross_product = dr_du.cross(dr_dv)
                
                # Sustituir x, y, z en F con r(u, v)
                F_sub = F.subs({'x': r[0], 'y': r[1], 'z': r[2]})
                
                # Producto punto F · (dr_du x dr_dv)
                dot_product = sum([F_sub[i] * cross_product[i] for i in range(3)])
                
                # Integrar sobre u y v
                integral = integrate(integrate(dot_product, (v, c, d)), (u, a, b))
                
                # Mostrar el resultado
                result_str = f"Integral de Superficie ∫∫ F · (dr/du × dr/dv) du dv = {integral}"
                self.surface_volume_result.configure(state='normal')
                self.surface_volume_result.delete('1.0', tk.END)
                self.surface_volume_result.insert(tk.END, result_str)
                self.surface_volume_result.configure(state='disabled')
            
            elif integral_type == "Volumen":
                f_str = self.F_volume_entry.get()
                x_a_str = self.x_a_entry.get()
                x_b_str = self.x_b_entry.get()
                y_c_str = self.y_c_entry.get()
                y_d_str = self.y_d_entry.get()
                z_e_str = self.z_e_entry.get()
                z_f_str = self.z_f_entry.get()
                
                if not f_str or not x_a_str or not x_b_str or not y_c_str or not y_d_str or not z_e_str or not z_f_str:
                    messagebox.showerror("Error", "Por favor, completa todos los campos para la integral de volumen.")
                    return
                
                x_a = float(x_a_str)
                x_b = float(x_b_str)
                y_c = float(y_c_str)
                y_d = float(y_d_str)
                z_e = float(z_e_str)
                z_f = float(z_f_str)
                
                t = symbols('t')  # No se utiliza en este contexto
                
                # Parsear f(x, y, z)
                f = sympify(f_str)
                
                # Integrar sobre x, y, z
                integral = integrate(f, (symbols('x'), x_a, x_b), (symbols('y'), y_c, y_d), (symbols('z'), z_e, z_f))
                
                # Mostrar el resultado
                result_str = f"Integral de Volumen ∫∫∫ f(x, y, z) dx dy dz = {integral}"
                self.surface_volume_result.configure(state='normal')
                self.surface_volume_result.delete('1.0', tk.END)
                self.surface_volume_result.insert(tk.END, result_str)
                self.surface_volume_result.configure(state='disabled')
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular la integral: {e}")
    
    def create_determinant_integral_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Determinante de Integrales")
        
        # Instrucciones
        instructions = (
            "Calcula el determinante de la integral de una matriz A(t) sobre [a, b].\n"
            "Ejemplo para una matriz 2x2:\n"
            "[[t, 0], [0, t**2]]"
        )
        instr_label = ttk.Label(tab, text=instructions, wraplength=800, justify='left')
        instr_label.pack(pady=10)
        
        # Entrada de matriz
        matrix_label = ttk.Label(tab, text="A(t) = ")
        matrix_label.pack(anchor='w', padx=10)
        self.det_matrix_entry = ttk.Entry(tab, width=100)
        self.det_matrix_entry.pack(padx=10, pady=5)
        
        # Intervalo de integración
        interval_frame = ttk.Frame(tab)
        interval_frame.pack(pady=10, anchor='w', padx=10)
        ttk.Label(interval_frame, text="Intervalo de Integración: ").pack(side='left')
        ttk.Label(interval_frame, text="a=").pack(side='left')
        self.det_a_entry = ttk.Entry(interval_frame, width=10)
        self.det_a_entry.pack(side='left', padx=5)
        ttk.Label(interval_frame, text="b=").pack(side='left')
        self.det_b_entry = ttk.Entry(interval_frame, width=10)
        self.det_b_entry.pack(side='left', padx=5)
        
        # Botón para calcular
        calc_button = ttk.Button(tab, text="Calcular Determinante de la Integral", command=self.calculate_determinant_integral)
        calc_button.pack(pady=10)
        
        # Área de resultados
        result_label = ttk.Label(tab, text="Resultado:")
        result_label.pack(anchor='w', padx=10)
        self.det_result = scrolledtext.ScrolledText(tab, height=15, width=100, state='disabled', font=("Segoe UI", 12))
        self.det_result.pack(padx=10, pady=5)
    
    def calculate_determinant_integral(self):
        matrix_str = self.det_matrix_entry.get()
        a_str = self.det_a_entry.get()
        b_str = self.det_b_entry.get()
        
        if not matrix_str or not a_str or not b_str:
            messagebox.showerror("Error", "Por favor, completa todos los campos.")
            return
        
        try:
            a = float(a_str)
            b = float(b_str)
        except ValueError:
            messagebox.showerror("Error", "Los límites de integración deben ser números.")
            return
        
        try:
            # Parsear la matriz
            matrix_list = sympify(matrix_str)
            if not isinstance(matrix_list, (list, tuple, Matrix)):
                raise ValueError("La matriz debe ser una lista, tupla o matriz de SymPy.")
            matrix = Matrix(matrix_list)
            rows, cols = matrix.shape
            
            # Integrar cada elemento
            integral_matrix = Matrix(rows, cols, lambda i, j: integrate(matrix[i, j], (symbols('t'), a, b)))
            
            # Calcular el determinante
            det_integral = integral_matrix.det()
            
            # Mostrar el resultado
            result_str = (
                f"∫ₐᵇ A(t) dt =\n{integral_matrix}\n\n"
                f"Determinante de ∫ₐᵇ A(t) dt = {det_integral}"
            )
            self.det_result.configure(state='normal')
            self.det_result.delete('1.0', tk.END)
            self.det_result.insert(tk.END, result_str)
            self.det_result.configure(state='disabled')
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular el determinante de la integral: {e}")
    
    def create_eigen_integral_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Valores y Vectores Propios")
        
        # Instrucciones
        instructions = (
            "Calcula los valores y vectores propios de la integral de una matriz A(t) sobre [a, b].\n"
            "Ejemplo para una matriz 2x2:\n"
            "[[t, 1], [0, t**2]]"
        )
        instr_label = ttk.Label(tab, text=instructions, wraplength=800, justify='left')
        instr_label.pack(pady=10)
        
        # Entrada de matriz
        matrix_label = ttk.Label(tab, text="A(t) = ")
        matrix_label.pack(anchor='w', padx=10)
        self.eigen_matrix_entry = ttk.Entry(tab, width=100)
        self.eigen_matrix_entry.pack(padx=10, pady=5)
        
        # Intervalo de integración
        interval_frame = ttk.Frame(tab)
        interval_frame.pack(pady=10, anchor='w', padx=10)
        ttk.Label(interval_frame, text="Intervalo de Integración: ").pack(side='left')
        ttk.Label(interval_frame, text="a=").pack(side='left')
        self.eigen_a_entry = ttk.Entry(interval_frame, width=10)
        self.eigen_a_entry.pack(side='left', padx=5)
        ttk.Label(interval_frame, text="b=").pack(side='left')
        self.eigen_b_entry = ttk.Entry(interval_frame, width=10)
        self.eigen_b_entry.pack(side='left', padx=5)
        
        # Botón para calcular
        calc_button = ttk.Button(tab, text="Calcular Valores y Vectores Propios", command=self.calculate_eigen_integral)
        calc_button.pack(pady=10)
        
        # Área de resultados
        result_label = ttk.Label(tab, text="Resultado:")
        result_label.pack(anchor='w', padx=10)
        self.eigen_result = scrolledtext.ScrolledText(tab, height=15, width=100, state='disabled', font=("Segoe UI", 12))
        self.eigen_result.pack(padx=10, pady=5)
    
    def calculate_eigen_integral(self):
        matrix_str = self.eigen_matrix_entry.get()
        a_str = self.eigen_a_entry.get()
        b_str = self.eigen_b_entry.get()
        
        if not matrix_str or not a_str or not b_str:
            messagebox.showerror("Error", "Por favor, completa todos los campos.")
            return
        
        try:
            a = float(a_str)
            b = float(b_str)
        except ValueError:
            messagebox.showerror("Error", "Los límites de integración deben ser números.")
            return
        
        try:
            # Parsear la matriz
            matrix_list = sympify(matrix_str)
            if not isinstance(matrix_list, (list, tuple, Matrix)):
                raise ValueError("La matriz debe ser una lista, tupla o matriz de SymPy.")
            matrix = Matrix(matrix_list)
            rows, cols = matrix.shape
            if rows != cols:
                raise ValueError("La matriz debe ser cuadrada para calcular valores y vectores propios.")
            
            # Integrar cada elemento
            integral_matrix = Matrix(rows, cols, lambda i, j: integrate(matrix[i, j], (symbols('t'), a, b)))
            
            # Calcular valores y vectores propios
            eigenvals = integral_matrix.eigenvals()
            eigenvects = integral_matrix.eigenvects()
            
            # Preparar resultados
            eigenvals_str = "Valores Propios:\n"
            for val, mult in eigenvals.items():
                eigenvals_str += f"λ = {val}, Multiplicidad = {mult}\n"
            
            eigenvects_str = "\nVectores Propios:\n"
            for vect_info in eigenvects:
                val = vect_info[0]
                multiplicity = vect_info[1]
                vectors = vect_info[2]
                eigenvects_str += f"Para λ = {val}:\n"
                for vect in vectors:
                    eigenvects_str += f"Vector propio: {vect}\n"
            
            # Mostrar resultados
            result_str = (
                f"∫ₐᵇ A(t) dt =\n{integral_matrix}\n\n"
                f"{eigenvals_str}\n"
                f"{eigenvects_str}"
            )
            self.eigen_result.configure(state='normal')
            self.eigen_result.delete('1.0', tk.END)
            self.eigen_result.insert(tk.END, result_str)
            self.eigen_result.configure(state='disabled')
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular valores y vectores propios: {e}")
    
def main():
    root = tk.Tk()
    app = IntegralesApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
