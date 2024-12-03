import tkinter as tk
from tkinter import ttk, messagebox
import math
import json
import os
from datetime import datetime
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import re

def insert_implicit_multiplication(func_str):
    """
    Inserta multiplicaciones implícitas en la cadena de la función.
    Por ejemplo, convierte '3x' en '3*x' y 'x sin(x)' en 'x*sin(x)'.
    """
    # Insertar '*' entre un número y una variable o función (e.g., 3x -> 3*x)
    func_str = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', func_str)
    # Insertar '*' entre una variable o cierre de paréntesis y una variable o función (e.g., x sin(x) -> x*sin(x))
    func_str = re.sub(r'([a-zA-Z\)])([a-zA-Z\(])', r'\1*\2', func_str)
    return func_str

def translate_function(func_str):
    """
    Traduce las funciones matemáticas ingresadas por el usuario a las correspondientes
    funciones del módulo math de Python. También maneja exponentes y multiplicaciones implícitas.
    """
    func_mappings = {
        'sen': 'math.sin',
        'cos': 'math.cos',
        'tan': 'math.tan',
        'asin': 'math.asin',
        'acos': 'math.acos',
        'atan': 'math.atan',
        'exp': 'math.exp',
        'log': 'math.log',
        'raiz': 'math.sqrt',
        # Puedes agregar más funciones si es necesario
    }

    # Reemplazar las funciones usando expresiones regulares
    for func, math_func in func_mappings.items():
        # Buscar la función seguida de un paréntesis
        pattern = r'\b' + re.escape(func) + r'\s*\('
        replacement = math_func + '('
        func_str = re.sub(pattern, replacement, func_str, flags=re.IGNORECASE)

    # Reemplazar '^' por '**' para exponentes
    func_str = func_str.replace('^', '**')

    # Insertar multiplicaciones implícitas
    func_str = insert_implicit_multiplication(func_str)

    return func_str

def evaluate_function(func_str, x):
    """
    Evalúa la función proporcionada como string en el punto x después de traducirla.
    """
    try:
        # Traduce la función ingresada
        translated_func = translate_function(func_str)
        # Define un entorno seguro para la evaluación
        allowed_names = {"x": x, "math": math, "np": np}
        return eval(translated_func, {"__builtins__": None}, allowed_names)
    except Exception as e:
        raise ValueError(f"Error al evaluar la función: {e}")

def bisection_method(func_str, a, b, tol, max_iter=100):
    """
    Implementa el método de bisección para encontrar la raíz de una función.
    Retorna la raíz, el número de iteraciones y un historial de las iteraciones.
    """
    fa = evaluate_function(func_str, a)
    fb = evaluate_function(func_str, b)

    if fa * fb > 0:
        raise ValueError("La función debe tener signos opuestos en los extremos del intervalo.")

    history = []
    xr_prev = None

    for iteration in range(1, max_iter + 1):
        c = (a + b) / 2
        fc = evaluate_function(func_str, c)

        if xr_prev is not None:
            relative_error = abs((c - xr_prev) / c) * 100
        else:
            relative_error = None

        history.append({
            'iteration': iteration,
            'a': a,
            'b': b,
            'c': c,
            'f(c)': fc,
            'relative_error': relative_error
        })

        if fc == 0 or (b - a) / 2 < tol or (relative_error is not None and relative_error < tol):
            return c, iteration, history

        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc

        xr_prev = c

    raise ValueError("El método de bisección no convergió dentro del número máximo de iteraciones.")

class BiseccionApp:
    def __init__(self, master):
        self.master = master
        self.master.title("🔢 Método de Bisección - Algebrify")
        self.master.geometry("1200x800")
        self.master.state('zoomed')  # Iniciar en pantalla completa
        self.master.bind("<F11>", self.toggle_fullscreen)
        self.master.bind("<Escape>", self.exit_fullscreen)

        # Menú
        self.menu_bar = tk.Menu(self.master)
        self.master.config(menu=self.menu_bar)

        view_menu = tk.Menu(self.menu_bar, tearoff=0)
        view_menu.add_command(label="Pantalla Completa (F11)", command=self.toggle_fullscreen)
        view_menu.add_command(label="Salir Pantalla Completa", command=self.exit_fullscreen)
        self.menu_bar.add_cascade(label="Ver", menu=view_menu)

        ayuda_menu = tk.Menu(self.menu_bar, tearoff=0)
        ayuda_menu.add_command(label="Cómo Ingresar un Ejercicio", command=self.show_instructions)
        self.menu_bar.add_cascade(label="Ayuda", menu=ayuda_menu)

        # Estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Helvetica', 12, 'bold'), padding=10)
        self.style.configure('TLabel', font=('Helvetica', 12))
        self.style.configure('Header.TLabel', font=('Helvetica', 20, 'bold'))
        self.style.configure('Treeview', font=('Helvetica', 12))
        self.style.configure('Treeview.Heading', font=('Helvetica', 12, 'bold'))
        # Configurar estilo para Combobox
        self.style.configure('TCombobox', font=('Helvetica', 12))

        # Contenedor principal
        self.main_frame = tk.Frame(master, padx=20, pady=20, bg="#f0f0f0")
        self.main_frame.pack(expand=True, fill='both')

        # Título
        title_label = ttk.Label(self.main_frame, text="Método de Bisección", style='Header.TLabel', background="#f0f0f0")
        title_label.pack(pady=(0, 20))

        # Inputs
        input_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        input_frame.pack(pady=10, fill='x')

        # Función
        func_label = ttk.Label(input_frame, text="Función f(x):", background="#f0f0f0")
        func_label.grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.func_var = tk.StringVar()
        self.func_entry = ttk.Entry(input_frame, width=50, textvariable=self.func_var, font=("Helvetica", 12))
        self.func_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        self.func_var.trace("w", self.update_function_display_and_disable_plot)

        # ### Agregar Combobox para seleccionar funciones ###
        # Etiqueta para el Combobox
        select_func_label = ttk.Label(input_frame, text="Seleccionar Función:", background="#f0f0f0")
        select_func_label.grid(row=0, column=2, sticky='e', padx=5, pady=5)

        # Opciones de funciones ampliadas y traducidas
        self.function_options = [
            "x^3",
            "x^2",
            "sen(x)",
            "cos(x)",
            "tan(x)",
            "exp(x)",
            "log(x)",
            "raiz(x)",
            "asin(x)",
            "acos(x)",
            "atan(x)",
            "x^4",
            "x^5",
            "-x",
            "-x^2 + 4",
            "exp(-x)",
            "log(x) - 1",
            "raiz(x) - 2",
            "sen(x) - 0.5",
            "cos(x) - 0.5",
            "tan(x) - 1"
        ]

        # Combobox para seleccionar funciones
        self.func_combobox = ttk.Combobox(input_frame, values=self.function_options, state="readonly", width=25, font=("Helvetica", 12))
        self.func_combobox.grid(row=0, column=3, padx=5, pady=5, sticky='w')
        self.func_combobox.bind("<<ComboboxSelected>>", self.on_function_selected)
        self.func_combobox.set("Seleccionar...")  # Texto por defecto

        # ### Fin de la adición del Combobox ###

        # Botón para generar ejercicios aleatorios
        generate_button = ttk.Button(input_frame, text="Generar Ejercicio Aleatorio", command=self.generate_random_exercise)
        generate_button.grid(row=0, column=4, padx=10, pady=5)

        # Botón de Ayuda Adicional
        help_button = ttk.Button(input_frame, text="Botón de Ayuda", command=self.show_instructions)
        help_button.grid(row=0, column=5, padx=10, pady=5)

        # Display en tiempo real de la función
        self.display_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.display_frame.pack(pady=5, fill='x')
        self.display_label = ttk.Label(self.display_frame, text="f(x) =", font=("Helvetica", 14, "bold"), background="#f0f0f0")
        self.display_label.pack(side='left', padx=5)
        self.display_func = ttk.Label(self.display_frame, text="", font=("Helvetica", 14), background="#f0f0f0", foreground="#333333")
        self.display_func.pack(side='left')

        # Intervalo a
        a_label = ttk.Label(input_frame, text="a:", background="#f0f0f0")
        a_label.grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.a_entry = ttk.Entry(input_frame, width=20, font=("Helvetica", 12))
        self.a_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.a_entry.bind("<Key>", self.on_manual_entry_change)

        # Intervalo b
        b_label = ttk.Label(input_frame, text="b:", background="#f0f0f0")
        b_label.grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.b_entry = ttk.Entry(input_frame, width=20, font=("Helvetica", 12))
        self.b_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.b_entry.bind("<Key>", self.on_manual_entry_change)

        # Tolerancia
        tol_label = ttk.Label(input_frame, text="Tolerancia:", background="#f0f0f0")
        tol_label.grid(row=3, column=0, sticky='e', padx=5, pady=5)
        self.tol_entry = ttk.Entry(input_frame, width=20, font=("Helvetica", 12))
        self.tol_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.tol_entry.bind("<Key>", self.on_manual_entry_change)

        # Botones
        button_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        button_frame.pack(pady=20)

        execute_button = ttk.Button(button_frame, text="Ejecutar Método", command=self.execute_bisection)
        execute_button.grid(row=0, column=0, padx=10)

        self.details_button = ttk.Button(button_frame, text="Detalles", command=self.show_details_window)
        self.details_button.grid(row=0, column=1, padx=10)
        self.details_button.state(['disabled'])  # Inicialmente deshabilitado

        # Nuevo Botón para Mostrar la Gráfica
        self.plot_button = ttk.Button(button_frame, text="Mostrar Gráfica", command=self.show_plot, state='disabled')  # Inicialmente deshabilitado
        self.plot_button.grid(row=0, column=2, padx=10)

        # Resultados
        result_label = ttk.Label(self.main_frame, text="Resultados:", background="#f0f0f0")
        result_label.pack(anchor='nw', padx=5, pady=5)

        # Treeview para mostrar las iteraciones
        columns = ("Iteración", "a", "b", "c", "f(c)", "Error Relativo (%)")
        self.tree = ttk.Treeview(self.main_frame, columns=columns, show='headings', height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center', width=150)
        self.tree.pack(pady=10, fill='both', expand=True)

        # Scrollbar para la Treeview
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

        # Botón Cerrar
        close_button = ttk.Button(self.main_frame, text="Cerrar", command=master.destroy)
        close_button.pack(pady=10)

        # Variable para almacenar detalles actuales
        self.current_details = None

    def toggle_fullscreen(self, event=None):
        self.master.attributes("-fullscreen", not self.master.attributes("-fullscreen"))

    def exit_fullscreen(self, event=None):
        self.master.attributes("-fullscreen", False)

    def update_function_display_and_disable_plot(self, *args):
        func = self.func_var.get()
        display_text = f"f(x) = {func}" if func else "f(x) = "
        self.display_func.config(text=display_text)
        # Deshabilitar el botón de graficar ya que la función ha cambiado
        self.plot_button.state(['disabled'])

    def show_instructions(self):
        instructions = (
            "### Cómo Ingresar un Ejercicio:\n\n"
            "1. **Formato de la Función:** Escribe la función matemática utilizando notación algebraica estándar.\n"
            "   - **Exponentes:** Usa el símbolo `^` para exponentes en lugar de `**`.\n"
            "     - Ejemplo: En lugar de `x**3`, escribe `x^3`.\n"
            "   - **Multiplicación Implícita:** Puedes omitir el símbolo `*` en multiplicaciones entre un número y una variable o entre dos variables.\n"
            "     - Ejemplo: En lugar de `3*x`, escribe `3x`.\n"
            "     - En lugar de `x*sin(x)`, escribe `x sin(x)`.\n"
            "   - **Funciones Matemáticas:** Usa nombres en español para las funciones trigonométricas y otras funciones matemáticas.\n"
            "     - Ejemplos: `sen(x)`, `cos(x)`, `tan(x)`, `raiz(x)`, `log(x)`, `exp(x)`.\n\n"
            "   - **Ejemplo Completo:** \n"
            "     - En lugar de `x**3 - 3*x**2 - sen(x)`, escribe `x^3 - 3x^2 - sen(x)`.\n\n"
            "2. **Intervalo [a, b]:** Ingresa los valores de `a` y `b` donde buscas la raíz.\n"
            "   - Asegúrate de que `f(a) * f(b) < 0` para aplicar el método de bisección.\n\n"
            "3. **Tolerancia:** Ingresa el valor de la precisión deseada (por ejemplo, `0.0001`).\n\n"
            "4. **Ejecutar el Método:** Haz clic en 'Ejecutar Método' para iniciar el proceso.\n\n"
            "5. **Resultados:** Los resultados se mostrarán en la tabla, detallando cada iteración.\n\n"
            "6. **Detalles y Gráfica:** Usa los botones 'Detalles' para ver una explicación completa del proceso y 'Mostrar Gráfica' para visualizar la función en el intervalo seleccionado.\n\n"
            "7. **Funciones Predefinidas:** Puedes seleccionar una función común desde el menú desplegable 'Seleccionar Función' para insertarla automáticamente en el campo de función.\n"
            "8. **Generar Ejercicio Aleatorio:** Haz clic en 'Generar Ejercicio Aleatorio' para que la aplicación genere automáticamente una función, un intervalo y una tolerancia adecuados.\n"
        )
        messagebox.showinfo("Cómo Ingresar un Ejercicio", instructions)

    def execute_bisection(self):
        func_str = self.func_entry.get()
        a_str = self.a_entry.get()
        b_str = self.b_entry.get()
        tol_str = self.tol_entry.get()

        # Validar entradas
        if not func_str or not a_str or not b_str or not tol_str:
            messagebox.showerror("Error", "Por favor, completa todos los campos.")
            return

        try:
            a = float(a_str)
            b = float(b_str)
            tol = float(tol_str)
        except ValueError:
            messagebox.showerror("Error", "a, b y tolerancia deben ser números.")
            return

        # Validar que a < b
        if a >= b:
            messagebox.showerror("Error", "El valor de 'a' debe ser menor que 'b'.")
            return

        try:
            # Ejecutar el método de bisección para una raíz
            root, iterations, history = bisection_method(func_str, a, b, tol)
            result = f"Raíz encontrada: {root}\nNúmero de iteraciones: {iterations}"
            messagebox.showinfo("Éxito", result)
            # Mostrar resultados en la Treeview
            self.display_results(history)
            # Guardar detalles para la ventana de detalles
            self.current_details = {
                'function': func_str,
                'a': a,
                'b': b,
                'tolerance': tol,
                'root': root,
                'iterations': iterations,
                'history': history,
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            # Habilitar el botón de detalles
            self.details_button.state(['!disabled'])
            # Habilitar el botón de graficar
            self.plot_button.state(['!disabled'])
            # Opcional: Guardar en historial
            self.save_to_history('Bisección', self.current_details)

            # Preguntar si desea encontrar todas las raíces en el intervalo
            response = messagebox.askyesno("Buscar Todas las Raíces", "¿Deseas encontrar todas las raíces existentes en el intervalo seleccionado?")
            if response:
                all_roots, all_histories = self.find_all_roots(func_str, a, b, tol)
                if all_roots:
                    roots_info = "\n".join([f"Raíz {i+1}: {root}" for i, root in enumerate(all_roots)])
                    messagebox.showinfo("Todas las Raíces Encontradas", f"Se encontraron {len(all_roots)} raíz(s):\n{roots_info}")
                    # Mostrar todas las iteraciones en la Treeview
                    self.display_multiple_results(all_histories)
                    # Actualizar detalles para múltiples raíces
                    self.current_details = {
                        'function': func_str,
                        'a': a,
                        'b': b,
                        'tolerance': tol,
                        'roots': all_roots,
                        'iterations': [h[-1]['iteration'] for h in all_histories],
                        'history': all_histories,
                        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    # Habilitar el botón de graficar si aún no está habilitado
                    self.plot_button.state(['!disabled'])
                    # Guardar en historial
                    self.save_to_history('Bisección - Múltiples Raíces', self.current_details)
                else:
                    messagebox.showinfo("Resultado", "No se encontraron más raíces en el intervalo.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al ejecutar el método: {e}")

    def find_all_roots(self, func_str, a, b, tol):
        """
        Encuentra todas las raíces en el intervalo [a, b] utilizando el método de bisección.
        """
        roots = []
        histories = []
        step = 1  # Tamaño del paso para escanear el intervalo
        sub_a = a
        while sub_a < b:
            sub_b = sub_a + step
            if sub_b > b:
                sub_b = b
            try:
                fa = evaluate_function(func_str, sub_a)
                fb = evaluate_function(func_str, sub_b)
                if fa * fb < 0:
                    root, iterations, history = bisection_method(func_str, sub_a, sub_b, tol)
                    # Verificar si la raíz ya está registrada (evitar duplicados)
                    if not any(math.isclose(root, existing_root, rel_tol=1e-5) for existing_root in roots):
                        roots.append(root)
                        histories.append(history)
            except:
                pass  # Ignorar errores y continuar
            sub_a += step / 2  # Superponer pasos para detectar raíces cercanas
        return roots, histories

    def display_results(self, history):
        # Limpiar Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Insertar nuevas filas
        for record in history:
            iteracion = record['iteration']
            a = record['a']
            b = record['b']
            c = record['c']
            fc = record['f(c)']
            error = f"{record['relative_error']:.6f}" if record['relative_error'] is not None else "N/A"
            self.tree.insert("", "end", values=(iteracion, f"{a:.6f}", f"{b:.6f}", f"{c:.6f}", f"{fc:.6f}", error))

    def display_multiple_results(self, histories):
        # Limpiar Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Insertar todas las iteraciones de todas las raíces
        for idx, history in enumerate(histories):
            self.tree.insert("", "end", values=(f"--- Raíz {idx+1} ---", "", "", "", "", ""))
            for record in history:
                iteracion = record['iteration']
                a = record['a']
                b = record['b']
                c = record['c']
                fc = record['f(c)']
                error = f"{record['relative_error']:.6f}" if record['relative_error'] is not None else "N/A"
                self.tree.insert("", "end", values=(iteracion, f"{a:.6f}", f"{b:.6f}", f"{c:.6f}", f"{fc:.6f}", error))

    def show_details_window(self):
        if not self.current_details:
            messagebox.showerror("Error", "No hay detalles para mostrar.")
            return

        details = self.current_details

        # Crear la nueva ventana
        details_window = tk.Toplevel(self.master)
        details_window.title("Detalles del Ejercicio")
        details_window.geometry("800x600")

        # Título
        details_title = ttk.Label(details_window, text="Detalles del Método de Bisección", style='Header.TLabel', background="#f0f0f0")
        details_title.pack(pady=10)

        # Información general
        info_frame = tk.Frame(details_window, padx=10, pady=10, bg="#f0f0f0")
        info_frame.pack(fill='x')

        if 'roots' in details:
            roots = "\n".join([f"Raíz {i+1}: {root}" for i, root in enumerate(details.get('roots', []))])
            iterations_info = "\n".join([f"Raíz {i+1}: {iterations}" for i, iterations in enumerate(details.get('iterations', []))])
            info_text = (
                f"Fecha: {details.get('date', 'N/A')}\n"
                f"Función f(x): {details.get('function', 'N/A')}\n"
                f"Intervalo [a, b]: [{details.get('a', 'N/A')}, {details.get('b', 'N/A')}]\n"
                f"Tolerancia: {details.get('tolerance', 'N/A')}\n"
                f"Raíces Encontradas:\n{roots}\n"
                f"Número de Iteraciones por Raíz:\n{iterations_info}\n"
            )
        else:
            info_text = (
                f"Fecha: {details.get('date', 'N/A')}\n"
                f"Función f(x): {details.get('function', 'N/A')}\n"
                f"Intervalo [a, b]: [{details.get('a', 'N/A')}, {details.get('b', 'N/A')}]\n"
                f"Tolerancia: {details.get('tolerance', 'N/A')}\n"
                f"Raíz Encontrada: {details.get('root', 'N/A')}\n"
                f"Número de Iteraciones: {details.get('iterations', 'N/A')}\n"
            )

        info_label = ttk.Label(info_frame, text=info_text, font=("Helvetica", 12), justify='left', background="#f0f0f0")
        info_label.pack(anchor='w')

        # Explicación del Método de Bisección
        explanation = (
            "\nProceso del Método de Bisección:\n\n"
            "1. **Selección del Intervalo Inicial:** Se elige un intervalo [a, b] donde la función f(x) cambia de signo, es decir, f(a) * f(b) < 0.\n"
            "2. **Cálculo del Punto Medio:** Se calcula el punto medio c = (a + b) / 2 y se evalúa f(c).\n"
            "3. **Verificación de la Condición de Parada:** Si f(c) es cercano a cero, si la longitud del intervalo es menor que la tolerancia, o si el error relativo es menor que la tolerancia, se considera que c es la raíz.\n"
            "4. **Actualización del Intervalo:** Dependiendo del signo de f(c), se actualiza el intervalo a [a, c] o [c, b].\n"
            "5. **Repetición del Proceso:** Se repite el proceso hasta que se cumple una de las condiciones de parada.\n"
        )

        explanation_label = ttk.Label(details_window, text=explanation, font=("Helvetica", 12), justify='left', wraplength=750, background="#f0f0f0")
        explanation_label.pack(anchor='w', padx=10)

        # Tabla de Iteraciones
        iterations_label = ttk.Label(details_window, text="Historial de Iteraciones:", font=("Helvetica", 14, "bold"), background="#f0f0f0")
        iterations_label.pack(pady=(20, 5))

        iter_columns = ("Iteración", "a", "b", "c", "f(c)", "Error Relativo (%)")
        iter_tree = ttk.Treeview(details_window, columns=iter_columns, show='headings', height=10)
        for col in iter_columns:
            iter_tree.heading(col, text=col)
            iter_tree.column(col, anchor='center', width=100)
        iter_tree.pack(pady=5, fill='both', expand=True, padx=10)

        # Scrollbar para las iteraciones
        iter_scrollbar = ttk.Scrollbar(details_window, orient="vertical", command=iter_tree.yview)
        iter_tree.configure(yscroll=iter_scrollbar.set)
        iter_scrollbar.pack(side='right', fill='y')

        # Insertar las iteraciones en el Treeview
        if 'roots' in details:
            history_records = details.get('history', [])
            for idx, history in enumerate(history_records):
                iter_tree.insert("", "end", values=(f"--- Raíz {idx+1} ---", "", "", "", "", ""))
                for record in history:
                    iteracion = record['iteration']
                    a_val = record['a']
                    b_val = record['b']
                    c_val = record['c']
                    fc_val = record['f(c)']
                    error_val = f"{record['relative_error']:.6f}" if record['relative_error'] is not None else "N/A"
                    iter_tree.insert("", "end", values=(iteracion, f"{a_val:.6f}", f"{b_val:.6f}", f"{c_val:.6f}", f"{fc_val:.6f}", error_val))
        else:
            history_records = details.get('history', [])
            for record in history_records:
                iteracion = record['iteration']
                a_val = record['a']
                b_val = record['b']
                c_val = record['c']
                fc_val = record['f(c)']
                error_val = f"{record['relative_error']:.6f}" if record['relative_error'] is not None else "N/A"
                iter_tree.insert("", "end", values=(iteracion, f"{a_val:.6f}", f"{b_val:.6f}", f"{c_val:.6f}", f"{fc_val:.6f}", error_val))

        # Botón Cerrar
        close_btn = ttk.Button(details_window, text="Cerrar", command=details_window.destroy)
        close_btn.pack(pady=10)

    def save_to_history(self, exercise_type, details):
        """
        Guarda los detalles del ejercicio en el archivo de historial.
        """
        history_file = 'history.json'
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                history = json.load(f)
        else:
            history = []

        history.append({
            'type': exercise_type,
            'details': details
        })

        with open(history_file, 'w') as f:
            json.dump(history, f, indent=4)

    def on_function_selected(self, event):
        selected_func = self.func_combobox.get()
        if selected_func != "Seleccionar...":
            self.func_var.set(selected_func)
            # Deshabilitar el botón de graficar ya que la función ha cambiado
            self.plot_button.state(['disabled'])

    def generate_random_exercise(self):
        """
        Genera un ejercicio aleatorio seleccionando una función y un intervalo válido.
        """
        max_attempts = 100  # Número máximo de intentos para encontrar un intervalo válido
        attempt = 0
        while attempt < max_attempts:
            # Seleccionar una función aleatoria
            func_str = random.choice(self.function_options)

            # Definir un rango para a y b
            a = random.uniform(-10, 10)
            b = random.uniform(-10, 10)
            if a == b:
                continue  # a y b no deben ser iguales

            # Asegurarse de que a < b
            if a > b:
                a, b = b, a

            # Evaluar f(a) y f(b)
            try:
                fa = evaluate_function(func_str, a)
                fb = evaluate_function(func_str, b)
            except Exception:
                attempt += 1
                continue  # Si hay un error en la evaluación, intentar con otra función

            # Verificar si f(a) * f(b) < 0
            if fa * fb < 0:
                # Seleccionar una tolerancia aleatoria entre 1e-4 y 1e-2
                tol = random.choice([0.0001, 0.00001, 0.000001, 0.001, 0.01])
                # Actualizar los campos de la interfaz
                self.func_var.set(func_str)
                self.func_combobox.set("Seleccionar...")
                self.a_entry.delete(0, tk.END)
                self.a_entry.insert(0, f"{a:.6f}")
                self.b_entry.delete(0, tk.END)
                self.b_entry.insert(0, f"{b:.6f}")
                self.tol_entry.delete(0, tk.END)
                self.tol_entry.insert(0, f"{tol:.6f}")
                # Deshabilitar el botón de graficar hasta que se ejecute el método
                self.plot_button.state(['disabled'])
                # Deshabilitar el botón de detalles hasta que se ejecute el método
                self.details_button.state(['disabled'])
                # Limpiar la Treeview
                self.clear_treeview()
                messagebox.showinfo("Ejercicio Aleatorio", "Se ha generado un ejercicio aleatorio exitosamente.")
                return
            else:
                attempt += 1

        messagebox.showwarning("Advertencia", "No se pudo generar un ejercicio aleatorio válido después de varios intentos.")

    def clear_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def show_plot(self):
        """
        Muestra una gráfica de la función en el intervalo [a, b].
        """
        func_str = self.func_entry.get()
        a_str = self.a_entry.get()
        b_str = self.b_entry.get()

        # Validar entradas
        if not func_str or not a_str or not b_str:
            messagebox.showerror("Error", "Por favor, completa los campos de función, a y b para generar la gráfica.")
            return

        try:
            a = float(a_str)
            b = float(b_str)
        except ValueError:
            messagebox.showerror("Error", "a y b deben ser números.")
            return

        if a >= b:
            messagebox.showerror("Error", "El valor de 'a' debe ser menor que 'b'.")
            return

        # Generar puntos para la gráfica
        try:
            x_vals = np.linspace(a, b, 400)
            y_vals = [evaluate_function(func_str, x) for x in x_vals]
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar la gráfica:\n{e}")
            return

        # Crear una nueva ventana para la gráfica
        plot_window = tk.Toplevel(self.master)
        plot_window.title("Gráfica de la Función")
        plot_window.geometry("800x600")

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(x_vals, y_vals, label=f"f(x) = {func_str}")
        ax.axhline(0, color='black', linewidth=0.5)
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.set_title("Gráfica de la Función")
        ax.legend()
        ax.grid(True)

        # Integrar la gráfica en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

        # Botón para cerrar la ventana de la gráfica
        close_btn = ttk.Button(plot_window, text="Cerrar", command=plot_window.destroy)
        close_btn.pack(pady=10)

    def show_details_window(self):
        if not self.current_details:
            messagebox.showerror("Error", "No hay detalles para mostrar.")
            return

        details = self.current_details

        # Crear la nueva ventana
        details_window = tk.Toplevel(self.master)
        details_window.title("Detalles del Ejercicio")
        details_window.geometry("800x600")

        # Título
        details_title = ttk.Label(details_window, text="Detalles del Método de Bisección", style='Header.TLabel', background="#f0f0f0")
        details_title.pack(pady=10)

        # Información general
        info_frame = tk.Frame(details_window, padx=10, pady=10, bg="#f0f0f0")
        info_frame.pack(fill='x')

        if 'roots' in details:
            roots = "\n".join([f"Raíz {i+1}: {root}" for i, root in enumerate(details.get('roots', []))])
            iterations_info = "\n".join([f"Raíz {i+1}: {iterations}" for i, iterations in enumerate(details.get('iterations', []))])
            info_text = (
                f"Fecha: {details.get('date', 'N/A')}\n"
                f"Función f(x): {details.get('function', 'N/A')}\n"
                f"Intervalo [a, b]: [{details.get('a', 'N/A')}, {details.get('b', 'N/A')}]\n"
                f"Tolerancia: {details.get('tolerance', 'N/A')}\n"
                f"Raíces Encontradas:\n{roots}\n"
                f"Número de Iteraciones por Raíz:\n{iterations_info}\n"
            )
        else:
            info_text = (
                f"Fecha: {details.get('date', 'N/A')}\n"
                f"Función f(x): {details.get('function', 'N/A')}\n"
                f"Intervalo [a, b]: [{details.get('a', 'N/A')}, {details.get('b', 'N/A')}]\n"
                f"Tolerancia: {details.get('tolerance', 'N/A')}\n"
                f"Raíz Encontrada: {details.get('root', 'N/A')}\n"
                f"Número de Iteraciones: {details.get('iterations', 'N/A')}\n"
            )

        info_label = ttk.Label(info_frame, text=info_text, font=("Helvetica", 12), justify='left', background="#f0f0f0")
        info_label.pack(anchor='w')

        # Explicación del Método de Bisección
        explanation = (
            "\nProceso del Método de Bisección:\n\n"
            "1. **Selección del Intervalo Inicial:** Se elige un intervalo [a, b] donde la función f(x) cambia de signo, es decir, f(a) * f(b) < 0.\n"
            "2. **Cálculo del Punto Medio:** Se calcula el punto medio c = (a + b) / 2 y se evalúa f(c).\n"
            "3. **Verificación de la Condición de Parada:** Si f(c) es cercano a cero, si la longitud del intervalo es menor que la tolerancia, o si el error relativo es menor que la tolerancia, se considera que c es la raíz.\n"
            "4. **Actualización del Intervalo:** Dependiendo del signo de f(c), se actualiza el intervalo a [a, c] o [c, b].\n"
            "5. **Repetición del Proceso:** Se repite el proceso hasta que se cumple una de las condiciones de parada.\n"
        )

        explanation_label = ttk.Label(details_window, text=explanation, font=("Helvetica", 12), justify='left', wraplength=750, background="#f0f0f0")
        explanation_label.pack(anchor='w', padx=10)

        # Tabla de Iteraciones
        iterations_label = ttk.Label(details_window, text="Historial de Iteraciones:", font=("Helvetica", 14, "bold"), background="#f0f0f0")
        iterations_label.pack(pady=(20, 5))

        iter_columns = ("Iteración", "a", "b", "c", "f(c)", "Error Relativo (%)")
        iter_tree = ttk.Treeview(details_window, columns=iter_columns, show='headings', height=10)
        for col in iter_columns:
            iter_tree.heading(col, text=col)
            iter_tree.column(col, anchor='center', width=100)
        iter_tree.pack(pady=5, fill='both', expand=True, padx=10)

        # Scrollbar para las iteraciones
        iter_scrollbar = ttk.Scrollbar(details_window, orient="vertical", command=iter_tree.yview)
        iter_tree.configure(yscroll=iter_scrollbar.set)
        iter_scrollbar.pack(side='right', fill='y')

        # Insertar las iteraciones en el Treeview
        if 'roots' in details:
            history_records = details.get('history', [])
            for idx, history in enumerate(history_records):
                iter_tree.insert("", "end", values=(f"--- Raíz {idx+1} ---", "", "", "", "", ""))
                for record in history:
                    iteracion = record['iteration']
                    a_val = record['a']
                    b_val = record['b']
                    c_val = record['c']
                    fc_val = record['f(c)']
                    error_val = f"{record['relative_error']:.6f}" if record['relative_error'] is not None else "N/A"
                    iter_tree.insert("", "end", values=(iteracion, f"{a_val:.6f}", f"{b_val:.6f}", f"{c_val:.6f}", f"{fc_val:.6f}", error_val))
        else:
            history_records = details.get('history', [])
            for record in history_records:
                iteracion = record['iteration']
                a_val = record['a']
                b_val = record['b']
                c_val = record['c']
                fc_val = record['f(c)']
                error_val = f"{record['relative_error']:.6f}" if record['relative_error'] is not None else "N/A"
                iter_tree.insert("", "end", values=(iteracion, f"{a_val:.6f}", f"{b_val:.6f}", f"{c_val:.6f}", f"{fc_val:.6f}", error_val))

        # Botón Cerrar
        close_btn = ttk.Button(details_window, text="Cerrar", command=details_window.destroy)
        close_btn.pack(pady=10)

    def save_to_history(self, exercise_type, details):
        """
        Guarda los detalles del ejercicio en el archivo de historial.
        """
        history_file = 'history.json'
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                history = json.load(f)
        else:
            history = []

        history.append({
            'type': exercise_type,
            'details': details
        })

        with open(history_file, 'w') as f:
            json.dump(history, f, indent=4)

    def on_function_selected(self, event):
        selected_func = self.func_combobox.get()
        if selected_func != "Seleccionar...":
            self.func_var.set(selected_func)
            # Deshabilitar el botón de graficar ya que la función ha cambiado
            self.plot_button.state(['disabled'])

    def generate_random_exercise(self):
        """
        Genera un ejercicio aleatorio seleccionando una función y un intervalo válido.
        """
        max_attempts = 100  # Número máximo de intentos para encontrar un intervalo válido
        attempt = 0
        while attempt < max_attempts:
            # Seleccionar una función aleatoria
            func_str = random.choice(self.function_options)

            # Definir un rango para a y b
            a = random.uniform(-10, 10)
            b = random.uniform(-10, 10)
            if a == b:
                continue  # a y b no deben ser iguales

            # Asegurarse de que a < b
            if a > b:
                a, b = b, a

            # Evaluar f(a) y f(b)
            try:
                fa = evaluate_function(func_str, a)
                fb = evaluate_function(func_str, b)
            except Exception:
                attempt += 1
                continue  # Si hay un error en la evaluación, intentar con otra función

            # Verificar si f(a) * f(b) < 0
            if fa * fb < 0:
                # Seleccionar una tolerancia aleatoria entre 1e-4 y 1e-2
                tol = random.choice([0.0001, 0.00001, 0.000001, 0.001, 0.01])
                # Actualizar los campos de la interfaz
                self.func_var.set(func_str)
                self.func_combobox.set("Seleccionar...")
                self.a_entry.delete(0, tk.END)
                self.a_entry.insert(0, f"{a:.6f}")
                self.b_entry.delete(0, tk.END)
                self.b_entry.insert(0, f"{b:.6f}")
                self.tol_entry.delete(0, tk.END)
                self.tol_entry.insert(0, f"{tol:.6f}")
                # Deshabilitar el botón de graficar hasta que se ejecute el método
                self.plot_button.state(['disabled'])
                # Deshabilitar el botón de detalles hasta que se ejecute el método
                self.details_button.state(['disabled'])
                # Limpiar la Treeview
                self.clear_treeview()
                messagebox.showinfo("Ejercicio Aleatorio", "Se ha generado un ejercicio aleatorio exitosamente.")
                return
            else:
                attempt += 1

        messagebox.showwarning("Advertencia", "No se pudo generar un ejercicio aleatorio válido después de varios intentos.")

    def clear_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def show_plot(self):
        """
        Muestra una gráfica de la función en el intervalo [a, b].
        """
        func_str = self.func_entry.get()
        a_str = self.a_entry.get()
        b_str = self.b_entry.get()

        # Validar entradas
        if not func_str or not a_str or not b_str:
            messagebox.showerror("Error", "Por favor, completa los campos de función, a y b para generar la gráfica.")
            return

        try:
            a = float(a_str)
            b = float(b_str)
        except ValueError:
            messagebox.showerror("Error", "a y b deben ser números.")
            return

        if a >= b:
            messagebox.showerror("Error", "El valor de 'a' debe ser menor que 'b'.")
            return

        # Generar puntos para la gráfica
        try:
            x_vals = np.linspace(a, b, 400)
            y_vals = [evaluate_function(func_str, x) for x in x_vals]
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar la gráfica:\n{e}")
            return

        # Crear una nueva ventana para la gráfica
        plot_window = tk.Toplevel(self.master)
        plot_window.title("Gráfica de la Función")
        plot_window.geometry("800x600")

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(x_vals, y_vals, label=f"f(x) = {func_str}")
        ax.axhline(0, color='black', linewidth=0.5)
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.set_title("Gráfica de la Función")
        ax.legend()
        ax.grid(True)

        # Integrar la gráfica en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

        # Botón para cerrar la ventana de la gráfica
        close_btn = ttk.Button(plot_window, text="Cerrar", command=plot_window.destroy)
        close_btn.pack(pady=10)

    def show_details_window(self):
        if not self.current_details:
            messagebox.showerror("Error", "No hay detalles para mostrar.")
            return

        details = self.current_details

        # Crear la nueva ventana
        details_window = tk.Toplevel(self.master)
        details_window.title("Detalles del Ejercicio")
        details_window.geometry("800x600")

        # Título
        details_title = ttk.Label(details_window, text="Detalles del Método de Bisección", style='Header.TLabel', background="#f0f0f0")
        details_title.pack(pady=10)

        # Información general
        info_frame = tk.Frame(details_window, padx=10, pady=10, bg="#f0f0f0")
        info_frame.pack(fill='x')

        if 'roots' in details:
            roots = "\n".join([f"Raíz {i+1}: {root}" for i, root in enumerate(details.get('roots', []))])
            iterations_info = "\n".join([f"Raíz {i+1}: {iterations}" for i, iterations in enumerate(details.get('iterations', []))])
            info_text = (
                f"Fecha: {details.get('date', 'N/A')}\n"
                f"Función f(x): {details.get('function', 'N/A')}\n"
                f"Intervalo [a, b]: [{details.get('a', 'N/A')}, {details.get('b', 'N/A')}]\n"
                f"Tolerancia: {details.get('tolerance', 'N/A')}\n"
                f"Raíces Encontradas:\n{roots}\n"
                f"Número de Iteraciones por Raíz:\n{iterations_info}\n"
            )
        else:
            info_text = (
                f"Fecha: {details.get('date', 'N/A')}\n"
                f"Función f(x): {details.get('function', 'N/A')}\n"
                f"Intervalo [a, b]: [{details.get('a', 'N/A')}, {details.get('b', 'N/A')}]\n"
                f"Tolerancia: {details.get('tolerance', 'N/A')}\n"
                f"Raíz Encontrada: {details.get('root', 'N/A')}\n"
                f"Número de Iteraciones: {details.get('iterations', 'N/A')}\n"
            )

        info_label = ttk.Label(info_frame, text=info_text, font=("Helvetica", 12), justify='left', background="#f0f0f0")
        info_label.pack(anchor='w')

        # Explicación del Método de Bisección
        explanation = (
            "\nProceso del Método de Bisección:\n\n"
            "1. **Selección del Intervalo Inicial:** Se elige un intervalo [a, b] donde la función f(x) cambia de signo, es decir, f(a) * f(b) < 0.\n"
            "2. **Cálculo del Punto Medio:** Se calcula el punto medio c = (a + b) / 2 y se evalúa f(c).\n"
            "3. **Verificación de la Condición de Parada:** Si f(c) es cercano a cero, si la longitud del intervalo es menor que la tolerancia, o si el error relativo es menor que la tolerancia, se considera que c es la raíz.\n"
            "4. **Actualización del Intervalo:** Dependiendo del signo de f(c), se actualiza el intervalo a [a, c] o [c, b].\n"
            "5. **Repetición del Proceso:** Se repite el proceso hasta que se cumple una de las condiciones de parada.\n"
        )

        explanation_label = ttk.Label(details_window, text=explanation, font=("Helvetica", 12), justify='left', wraplength=750, background="#f0f0f0")
        explanation_label.pack(anchor='w', padx=10)

        # Tabla de Iteraciones
        iterations_label = ttk.Label(details_window, text="Historial de Iteraciones:", font=("Helvetica", 14, "bold"), background="#f0f0f0")
        iterations_label.pack(pady=(20, 5))

        iter_columns = ("Iteración", "a", "b", "c", "f(c)", "Error Relativo (%)")
        iter_tree = ttk.Treeview(details_window, columns=iter_columns, show='headings', height=10)
        for col in iter_columns:
            iter_tree.heading(col, text=col)
            iter_tree.column(col, anchor='center', width=100)
        iter_tree.pack(pady=5, fill='both', expand=True, padx=10)

        # Scrollbar para las iteraciones
        iter_scrollbar = ttk.Scrollbar(details_window, orient="vertical", command=iter_tree.yview)
        iter_tree.configure(yscroll=iter_scrollbar.set)
        iter_scrollbar.pack(side='right', fill='y')

        # Insertar las iteraciones en el Treeview
        if 'roots' in details:
            history_records = details.get('history', [])
            for idx, history in enumerate(history_records):
                iter_tree.insert("", "end", values=(f"--- Raíz {idx+1} ---", "", "", "", "", ""))
                for record in history:
                    iteracion = record['iteration']
                    a_val = record['a']
                    b_val = record['b']
                    c_val = record['c']
                    fc_val = record['f(c)']
                    error_val = f"{record['relative_error']:.6f}" if record['relative_error'] is not None else "N/A"
                    iter_tree.insert("", "end", values=(iteracion, f"{a_val:.6f}", f"{b_val:.6f}", f"{c_val:.6f}", f"{fc_val:.6f}", error_val))
        else:
            history_records = details.get('history', [])
            for record in history_records:
                iteracion = record['iteration']
                a_val = record['a']
                b_val = record['b']
                c_val = record['c']
                fc_val = record['f(c)']
                error_val = f"{record['relative_error']:.6f}" if record['relative_error'] is not None else "N/A"
                iter_tree.insert("", "end", values=(iteracion, f"{a_val:.6f}", f"{b_val:.6f}", f"{c_val:.6f}", f"{fc_val:.6f}", error_val))

        # Botón Cerrar
        close_btn = ttk.Button(details_window, text="Cerrar", command=details_window.destroy)
        close_btn.pack(pady=10)

    def on_manual_entry_change(self, event):
        """
        Evento llamado cuando el usuario cambia manualmente las entradas a, b o tolerancia.
        """
        # Deshabilitar el botón de graficar ya que los parámetros han cambiado
        self.plot_button.state(['disabled'])
        # Deshabilitar el botón de detalles ya que los resultados anteriores ya no son válidos
        self.details_button.state(['disabled'])
        # Limpiar la Treeview
        self.clear_treeview()

def main():
    root = tk.Tk()
    app = BiseccionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
