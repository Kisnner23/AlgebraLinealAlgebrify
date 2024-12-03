import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application
)
from matplotlib.figure import Figure

# Importar proyecciones 3D para gráficos 3D
from mpl_toolkits.mplot3d import Axes3D

# Habilitar interactividad en matplotlib
matplotlib.use('TkAgg')

# Constantes de configuración
BG_COLOR = "#1e1e1e"
FG_COLOR = "#ffffff"
ENTRY_BG_COLOR = "#2e2e2e"
FONT = ("Segoe UI", 12)  # Reducir tamaño de fuente
TITLE_FONT = ("Segoe UI", 20, "bold")  # Reducir tamaño de título
OPERATIONS = [
    ('+', '+'), ('-', '-'), ('×', '*'), ('÷', '/'),
    ('^', '**'), ('(', '('), (')', ')'),
    ('sin', 'sin('), ('cos', 'cos('), ('tan', 'tan('),
    ('asin', 'asin('), ('acos', 'acos('), ('atan', 'atan('),
    ('sinh', 'sinh('), ('cosh', 'cosh('), ('tanh', 'tanh('),
    ('sec', 'sec('), ('csc', 'csc('), ('cot', 'cot('),
    ('exp', 'exp('), ('ln', 'ln('), ('log', 'log('), ('√', 'sqrt('),
    ('abs', 'Abs('),
    ('e', 'E'), ('π', 'pi'),
    ('x²', 'x**2'), ('x³', 'x**3'), ('x⁴', 'x**4'), ('x⁵', 'x**5'),
    ('y²', 'y**2'), ('y³', 'y**3'), ('y⁴', 'y**4'), ('y⁵', 'y**5')
]
NUMBERS = ['7', '8', '9', '4', '5', '6', '1', '2', '3', '0', '.']
VARIABLES = ['x', 'y']

class NewtonRaphsonApp:
    def __init__(self, master):
        self.master = master
        self.setup_window()
        self.setup_style()
        self.setup_main_frame()
        self.op_buttons = []
        self.button_positions = {}
        self.drag_data = {"x": 0, "y": 0, "item": None}
        self.transformations = (
            standard_transformations + (implicit_multiplication_application,)
        )
        self.graph_button = None
        self.tol_value = 0.0001  # Cambiar a valor de tolerancia directo
        self.create_widgets()

    def setup_window(self):
        """Configura la ventana principal."""
        self.master.title("🔍 Método de Newton-Raphson - Algebrify")
        # self.master.state('zoomed')  # Comentado para evitar pantalla completa
        self.master.geometry("1024x768")  # Tamaño de ventana ajustado
        self.master.resizable(True, True)  # Habilitar redimensionamiento
        self.master.configure(bg=BG_COLOR)

    def setup_style(self):
        """Configura el estilo de la aplicación."""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton',
                             background=ENTRY_BG_COLOR,
                             foreground=FG_COLOR,
                             font=FONT)

    def setup_main_frame(self):
        """Crea y empaca el frame principal."""
        self.frame = tk.Frame(self.master, bg=BG_COLOR)
        self.frame.pack(expand=True, fill='both', padx=20, pady=20)

    def create_widgets(self):
        """Crea todos los widgets de la interfaz."""
        self.create_title()
        self.create_action_buttons()  # Mover los botones de acción más arriba
        self.create_function_entries()
        self.create_parameters()
        self.create_buttons_section()
        self.create_result_display()

    def create_title(self):
        """Crea el título de la aplicación."""
        title_label = tk.Label(
            self.frame,
            text="🔍 Método de Newton-Raphson",
            font=TITLE_FONT,
            fg=FG_COLOR,
            bg=BG_COLOR
        )
        title_label.pack(pady=(0, 10))

    def create_function_entries(self):
        """Crea las entradas para la función y su derivada."""
        constructor_frame = tk.Frame(self.frame, bg=BG_COLOR)
        constructor_frame.pack(pady=5, fill='x')

        # Función f(x)
        self.create_label_entry(
            parent=constructor_frame,
            row=0,
            label_text="Función f(x):",
            display_text="f(x) = ",
            entry_variable='func_entry'
        )

        # Derivada f'(x)
        self.create_label_entry(
            parent=constructor_frame,
            row=1,
            label_text="Derivada f'(x):",
            display_text="f'(x) = ",
            entry_variable='deriv_entry'
        )

    def create_label_entry(self, parent, row, label_text, display_text, entry_variable):
        """Crea un par de etiqueta y entrada en el grid."""
        label = tk.Label(
            parent,
            text=label_text,
            font=FONT,
            fg=FG_COLOR,
            bg=BG_COLOR
        )
        label.grid(row=row, column=0, sticky='e', padx=5, pady=2)

        display = tk.Label(
            parent,
            text=display_text,
            font=FONT,
            fg=FG_COLOR,
            bg=BG_COLOR
        )
        display.grid(row=row, column=1, sticky='w', padx=5, pady=2)

        entry = tk.Entry(
            parent,
            width=35,
            font=FONT,
            bd=0,
            bg=ENTRY_BG_COLOR,
            fg=FG_COLOR
        )
        entry.grid(row=row, column=2, padx=5, pady=2)
        entry.insert(0, "")  # Inicialmente vacío

        setattr(self, entry_variable, entry)

    def create_buttons_section(self):
        """Crea la sección de botones organizados por categoría."""
        buttons_frame = tk.Frame(self.frame, bg=BG_COLOR)
        buttons_frame.pack(pady=5)

        # Frame para operaciones
        operations_frame = tk.LabelFrame(buttons_frame, text="Operaciones", bg=BG_COLOR, fg=FG_COLOR, font=FONT)
        operations_frame.grid(row=0, column=0, padx=5, pady=5, sticky='n')

        # Frame para contener los botones de operaciones
        self.operations_buttons_frame = tk.Frame(operations_frame, bg=BG_COLOR)
        self.operations_buttons_frame.pack()

        self.operations_buttons = []
        self.operations_frame = operations_frame

        for i, (op, symbol) in enumerate(OPERATIONS):
            btn = ttk.Button(self.operations_buttons_frame, text=op, width=4)  # Reducir ancho
            btn.grid(row=i//8, column=i%8, padx=1, pady=1)  # Más columnas, menos filas
            btn.bind("<ButtonPress-1>", self.on_button_press)
            btn.bind("<B1-Motion>", self.on_button_move)
            btn.bind("<ButtonRelease-1>", self.on_button_release)
            self.op_buttons.append((btn, symbol))
            self.button_positions[btn] = (i//8, i%8)
            self.operations_buttons.append(btn)

        # Botón para importar más operaciones
        self.import_button = ttk.Button(operations_frame, text='Importar Más Operaciones', command=self.import_operations)
        self.import_button.pack(pady=5)

        # Frame para números
        numbers_frame = tk.LabelFrame(buttons_frame, text="Números", bg=BG_COLOR, fg=FG_COLOR, font=FONT)
        numbers_frame.grid(row=0, column=1, padx=5, pady=5, sticky='n')

        for i, num in enumerate(NUMBERS):
            btn = ttk.Button(numbers_frame, text=num, width=4)  # Reducir ancho
            btn.grid(row=i//4, column=i%4, padx=1, pady=1)  # Más columnas
            btn.bind("<ButtonPress-1>", self.on_button_press)
            btn.bind("<B1-Motion>", self.on_button_move)
            btn.bind("<ButtonRelease-1>", self.on_button_release)
            self.op_buttons.append((btn, num))
            self.button_positions[btn] = (i//4, i%4)

        # Frame para variables
        variables_frame = tk.LabelFrame(buttons_frame, text="Variables", bg=BG_COLOR, fg=FG_COLOR, font=FONT)
        variables_frame.grid(row=0, column=2, padx=5, pady=5, sticky='n')

        for i, var in enumerate(VARIABLES):
            btn = ttk.Button(variables_frame, text=var, width=4)  # Reducir ancho
            btn.grid(row=0, column=i, padx=1, pady=1)
            btn.bind("<ButtonPress-1>", self.on_button_press)
            btn.bind("<B1-Motion>", self.on_button_move)
            btn.bind("<ButtonRelease-1>", self.on_button_release)
            self.op_buttons.append((btn, var))
            self.button_positions[btn] = (0, i)

    def create_parameters(self):
        """Crea las entradas para parámetros iniciales y de control."""
        params_frame = tk.Frame(self.frame, bg=BG_COLOR)
        params_frame.pack(pady=5, fill='x')

        # Valor inicial x0
        self.create_parameter_entry(
            parent=params_frame,
            row=0,
            label_text="Valor inicial x₀:",
            entry_variable='x0_entry',
            default="1.5",
            column=0
        )

        # Tolerancia
        self.create_parameter_entry(
            parent=params_frame,
            row=0,
            label_text="Tolerancia:",
            entry_variable='tol_entry',
            default="0.0001",
            column=2
        )

        # Máximo de Iteraciones
        self.create_parameter_entry(
            parent=params_frame,
            row=1,
            label_text="Máximo de Iteraciones:",
            entry_variable='max_iter_entry',
            default="100",
            column=0
        )

    def create_parameter_entry(self, parent, row, label_text, entry_variable, default="", column=0):
        """Crea una etiqueta y entrada para un parámetro."""
        label = tk.Label(
            parent,
            text=label_text,
            font=FONT,
            fg=FG_COLOR,
            bg=BG_COLOR
        )
        label.grid(row=row, column=column, sticky='e', padx=5, pady=2)

        entry = ttk.Entry(
            parent,
            width=15,
            font=FONT
        )
        entry.grid(row=row, column=column+1, padx=5, pady=2)
        entry.insert(0, default)

        setattr(self, entry_variable, entry)

    def create_action_buttons(self):
        """Crea los botones de acción: Calcular, Graficar, Limpiar, Generar y Cerrar."""
        actions_frame = tk.Frame(self.frame, bg=BG_COLOR)
        actions_frame.pack(pady=5)

        compute_button = ttk.Button(
            actions_frame,
            text="🔍 Calcular Raíz",
            command=self.compute_root,
            width=20
        )
        compute_button.grid(row=0, column=0, padx=5, pady=2)

        graph_button = ttk.Button(
            actions_frame,
            text="📈 Mostrar Gráfica",
            command=self.show_graph,
            width=20,
            state='disabled'  # Botón deshabilitado inicialmente
        )
        graph_button.grid(row=0, column=1, padx=5, pady=2)
        self.graph_button = graph_button  # Guardar referencia al botón

        generate_button = ttk.Button(
            actions_frame,
            text="🎲 Generar Ejercicio",
            command=self.generate_random_exercise,
            width=20
        )
        generate_button.grid(row=1, column=0, padx=5, pady=2)

        clear_button = ttk.Button(
            actions_frame,
            text="🧹 Limpiar",
            command=self.clear_all,
            width=20
        )
        clear_button.grid(row=1, column=1, padx=5, pady=2)

        close_button = ttk.Button(
            actions_frame,
            text="🔙 Volver",
            command=self.master.destroy,
            width=42
        )
        close_button.grid(row=2, column=0, columnspan=2, padx=5, pady=2)

    def create_result_display(self):
        """Crea el área para mostrar los resultados."""
        result_frame = tk.Frame(self.frame, bg=BG_COLOR)
        result_frame.pack(pady=5, fill='x')

        self.result_label = tk.Label(
            result_frame,
            text="",
            font=FONT,
            fg=FG_COLOR,
            bg=BG_COLOR,
            justify='left'
        )
        self.result_label.pack()

    def on_button_press(self, event):
        """Inicia el arrastre del botón."""
        widget = event.widget
        self.drag_data["item"] = widget
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def on_button_move(self, event):
        """Mueve el botón durante el arrastre."""
        widget = self.drag_data["item"]
        if widget:
            x = widget.winfo_x() - self.drag_data["x"] + event.x
            y = widget.winfo_y() - self.drag_data["y"] + event.y
            widget.place(x=x, y=y)

    def on_button_release(self, event):
        """Finaliza el arrastre e inserta el símbolo en la entrada correspondiente."""
        widget = self.drag_data["item"]
        if widget:
            x_root = self.master.winfo_pointerx() - self.master.winfo_rootx()
            y_root = self.master.winfo_pointery() - self.master.winfo_rooty()

            target = self.master.winfo_containing(
                self.master.winfo_rootx() + x_root,
                self.master.winfo_rooty() + y_root
            )

            if target in [self.func_entry, self.deriv_entry]:
                symbol = next((sym for btn, sym in self.op_buttons if btn == widget), None)
                if symbol:
                    current_text = target.get()
                    target.delete(0, tk.END)
                    target.insert(tk.END, current_text + symbol)

            widget.place_forget()
            original_pos = self.button_positions.get(widget, (0, 0))
            widget.grid(row=original_pos[0], column=original_pos[1], padx=1, pady=1)

            self.reset_drag_data()

    def compute_root(self):
        """Calcula la raíz utilizando el método de Newton-Raphson."""
        # Obtener y validar entradas
        try:
            func_str, deriv_str = self.get_function_inputs()
            x0, tol, max_iter = self.get_parameters()
        except ValueError as e:
            messagebox.showerror("Error de Entrada", str(e))
            return

        # Parsear funciones
        try:
            f_sympy, f_prime_sympy = self.parse_functions(func_str, deriv_str)
        except Exception as e:
            messagebox.showerror("Error en la Función", f"Error al interpretar las funciones:\n{e}")
            return

        # Convertir a funciones lambdify
        try:
            f = sp.lambdify(sp.symbols('x'), f_sympy, modules=['numpy', 'sympy'])
            f_prime = sp.lambdify(sp.symbols('x'), f_prime_sympy, modules=['numpy', 'sympy'])
        except Exception as e:
            messagebox.showerror("Error en la Función", f"Error al convertir funciones para evaluación numérica:\n{e}")
            return

        # Inicializar variables para la gráfica
        self.x_values = []
        self.f_values = []
        self.roots = []

        # Método de Newton-Raphson
        xi = x0
        for i in range(1, max_iter + 1):
            try:
                f_xi = f(xi)
                f_prime_xi = f_prime(xi)
            except Exception as e:
                messagebox.showerror("Error en la Evaluación", f"Error al evaluar las funciones en x = {xi}:\n{e}")
                return

            if f_prime_xi == 0:
                messagebox.showerror(
                    "Derivada Cero",
                    f"La derivada de f(x) en x = {xi} es cero. El método no puede continuar."
                )
                return

            xi_next = xi - f_xi / f_prime_xi

            # Guardar valores para la gráfica
            self.x_values.append(xi)
            self.f_values.append(f_xi)
            self.roots.append(xi_next)

            # Verificar convergencia
            if abs(xi_next - xi) < tol:
                xi = xi_next
                break

            xi = xi_next
        else:
            messagebox.showwarning(
                "No Convergencia",
                f"El método no convergió después de {max_iter} iteraciones."
            )
            return

        # Verificación final
        try:
            final_f = f(xi)
        except Exception as e:
            messagebox.showerror(
                "Error en la Evaluación Final",
                f"Error al evaluar f(x) en x = {xi}:\n{e}"
            )
            return

        # Mostrar resultados en ventana emergente
        result_message = f"Raíz encontrada: {xi}\nNúmero de iteraciones: {i}\nf(x) = {final_f}"
        messagebox.showinfo("Resultados", result_message)

        # Mostrar resultados en la interfaz
        self.result_label.config(text=result_message)

        # Guardar resultados para usarlos en la gráfica
        self.final_result = result_message

        # Habilitar el botón de mostrar gráfica
        self.graph_button['state'] = 'normal'

        # Guardar las funciones para usarlas en la gráfica interactiva
        self.f_sympy = f_sympy
        self.f_prime_sympy = f_prime_sympy

    def get_function_inputs(self):
        """Obtiene y valida las entradas de las funciones."""
        func_str = self.func_entry.get().strip()
        deriv_str = self.deriv_entry.get().strip()

        if not all([func_str, deriv_str]):
            raise ValueError("Por favor, completa las entradas de las funciones.")

        # Reemplazar ^ por ** para manejar exponentes
        func_str = func_str.replace('^', '**')
        deriv_str = deriv_str.replace('^', '**')

        return func_str, deriv_str

    def get_parameters(self):
        """Obtiene y valida los parámetros de entrada."""
        x0_str = self.x0_entry.get().strip()
        max_iter_str = self.max_iter_entry.get().strip()
        tol_str = self.tol_entry.get().strip()

        if not all([x0_str, max_iter_str, tol_str]):
            raise ValueError("Por favor, completa todos los parámetros de entrada.")

        try:
            x0 = float(x0_str)
            max_iter = int(max_iter_str)
            tol = float(tol_str)
            if tol <= 0:
                raise ValueError
        except ValueError:
            raise ValueError(
                "Asegúrate de que x₀ y tolerancia sean números válidos y el máximo de iteraciones sea un entero."
            )

        return x0, tol, max_iter

    def parse_functions(self, func_str, deriv_str):
        """Parsea las funciones usando SymPy."""
        x, y = sp.symbols('x y')
        f_sympy = parse_expr(func_str, transformations=self.transformations)
        f_prime_sympy = parse_expr(deriv_str, transformations=self.transformations)
        return f_sympy, f_prime_sympy

    def show_graph(self):
        """Muestra la gráfica de la función y permite interacción en tiempo real."""
        if not hasattr(self, 'x_values') or not self.x_values:
            messagebox.showwarning("Sin Datos", "Por favor, calcula una raíz primero.")
            return

        try:
            # Crear una nueva ventana
            graph_window = tk.Toplevel(self.master)
            graph_window.title("Gráfica Interactiva - Método de Newton-Raphson")
            graph_window.geometry("900x700")
            graph_window.configure(bg=BG_COLOR)

            # Crear una figura y un canvas en la nueva ventana
            figure = Figure(figsize=(8, 6), dpi=100)
            self.ax = figure.add_subplot(111)
            self.canvas = FigureCanvasTkAgg(figure, master=graph_window)
            self.canvas_widget = self.canvas.get_tk_widget()
            self.canvas_widget.pack(fill='both', expand=True)

            # Opciones de tipo de gráfica
            options_frame = tk.Frame(graph_window, bg=BG_COLOR)
            options_frame.pack(fill='x')

            graph_type_label = tk.Label(
                options_frame,
                text="Tipo de Gráfica:",
                font=FONT,
                fg=FG_COLOR,
                bg=BG_COLOR
            )
            graph_type_label.pack(side='left', padx=10, pady=5)

            graph_types = ["2D", "3D"]
            self.graph_type_var = tk.StringVar(value="2D")
            graph_type_menu = ttk.OptionMenu(
                options_frame,
                self.graph_type_var,
                "2D",
                *graph_types,
                command=self.update_graph
            )
            graph_type_menu.pack(side='left', padx=10, pady=5)

            # Mostrar resultados en la ventana de la gráfica
            result_label = tk.Label(
                options_frame,
                text=self.final_result,
                font=FONT,
                fg=FG_COLOR,
                bg=BG_COLOR,
                justify='left'
            )
            result_label.pack(side='left', padx=10, pady=5)

            # Graficar inicialmente
            self.plot_graph()

        except Exception as e:
            messagebox.showerror("Error en la Graficación", f"Hubo un error al graficar:\n{e}")

    def plot_graph(self):
        """Realiza la gráfica según el tipo seleccionado."""
        self.ax.clear()
        graph_type = self.graph_type_var.get()

        if graph_type == "2D":
            self.plot_2d_graph()
        elif graph_type == "3D":
            self.plot_3d_graph()

        self.canvas.draw()

    def plot_2d_graph(self):
        """Realiza la gráfica 2D interactiva."""
        x_min, x_max = self.get_x_range()
        x_plot = np.linspace(x_min, x_max, 400)
        y_plot = self.f(x_plot)

        # Graficar f(x)
        self.ax.plot(x_plot, y_plot, label='f(x)', color='blue')

        # Graficar las iteraciones de Newton-Raphson
        self.ax.plot(self.x_values, self.f_values, 'ro-', label='Iteraciones')

        # Graficar la raíz encontrada
        self.ax.axhline(0, color='black', linewidth=0.5)
        self.ax.plot(self.roots[-1], 0, 'go', label='Raíz')

        # Configurar la gráfica
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('f(x)')
        self.ax.set_title('Método de Newton-Raphson (2D)')
        self.ax.legend()
        self.ax.grid(True)

    def plot_3d_graph(self):
        """Realiza la gráfica 3D interactiva."""
        self.ax = self.ax.figure.add_subplot(111, projection='3d')
        x_min, x_max = self.get_x_range()
        y_min, y_max = x_min, x_max
        x_plot = np.linspace(x_min, x_max, 100)
        y_plot = np.linspace(y_min, y_max, 100)
        X, Y = np.meshgrid(x_plot, y_plot)
        Z = self.f_3d(X, Y)

        # Graficar la superficie
        self.ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)

        # Configurar la gráfica
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.set_zlabel('f(x, y)')
        self.ax.set_title('Método de Newton-Raphson (3D)')

    def f(self, x_val):
        """Evalúa f(x) usando SymPy."""
        try:
            func_str = self.func_entry.get().replace('^', '**')
            f_sympy = parse_expr(func_str, transformations=self.transformations)
            f_lambdified = sp.lambdify(sp.symbols('x'), f_sympy, modules=['numpy', 'sympy'])
            return f_lambdified(x_val)
        except Exception as e:
            messagebox.showerror("Error en la Evaluación de f(x)", f"Hubo un error al evaluar f(x):\n{e}")
            return None

    def f_3d(self, x_val, y_val):
        """Evalúa f(x, y) para gráficas 3D usando SymPy."""
        try:
            func_str = self.func_entry.get().replace('^', '**')
            f_sympy = parse_expr(func_str, transformations=self.transformations)
            f_lambdified = sp.lambdify((sp.symbols('x'), sp.symbols('y')), f_sympy, modules=['numpy', 'sympy'])
            return f_lambdified(x_val, y_val)
        except Exception as e:
            messagebox.showerror("Error en la Evaluación de f(x, y)", f"Hubo un error al evaluar f(x, y):\n{e}")
            return None

    def get_x_range(self):
        """Obtiene el rango de x para la gráfica."""
        all_x = self.x_values + self.roots
        x_min = min(all_x) - 1
        x_max = max(all_x) + 1
        return x_min, x_max

    def update_graph(self, event=None):
        """Actualiza la gráfica al cambiar las opciones."""
        self.plot_graph()

    def clear_all(self):
        """Limpia todas las entradas, resultados y la gráfica."""
        # Limpiar las entradas de funciones
        self.func_entry.delete(0, tk.END)
        self.deriv_entry.delete(0, tk.END)

        # Resetear parámetros a valores predeterminados
        self.reset_parameters()

        # Limpiar resultados
        self.result_label.config(text="")

        # Deshabilitar el botón de mostrar gráfica
        self.graph_button['state'] = 'disabled'

    def reset_parameters(self):
        """Resetea los parámetros a sus valores predeterminados."""
        defaults = {
            'x0_entry': "1.5",
            'max_iter_entry': "100",
            'tol_entry': "0.0001"
        }
        for var, default in defaults.items():
            entry = getattr(self, var, None)
            if entry:
                entry.delete(0, tk.END)
                entry.insert(0, default)

    def reset_drag_data(self):
        """Resetea los datos de arrastre."""
        self.drag_data = {"x": 0, "y": 0, "item": None}

    def generate_random_exercise(self):
        """Genera una función y derivada aleatorias y las inserta en las entradas."""
        functions = [
            ('x**2 - 2', '2*x'),
            ('x**3 - x - 2', '3*x**2 - 1'),
            ('sin(x) - x/2', 'cos(x) - 0.5'),
            ('exp(-x) - x', '-exp(-x) - 1'),
            ('x**5 - 5', '5*x**4'),
            ('ln(x) - 1', '1/x'),
            ('x**3 - 3*x + 2', '3*x**2 - 3'),
            ('x - cos(x)', '1 + sin(x)'),
            ('x**2 - sin(x)', '2*x - cos(x)'),
            ('tan(x) - x', 'sec(x)**2 - 1'),
            ('log(x) - 2', '1/(x*ln(10))'),
            ('sec(x) - 2', 'sec(x)*tan(x)')
        ]
        func, deriv = random.choice(functions)
        self.func_entry.delete(0, tk.END)
        self.func_entry.insert(0, func)
        self.deriv_entry.delete(0, tk.END)
        self.deriv_entry.insert(0, deriv)

    def import_operations(self):
        """Abre un diálogo para agregar más operaciones."""
        symbol = simpledialog.askstring("Agregar Operación", "Ingrese el símbolo de la operación:")
        if symbol is None:
            return
        expression = simpledialog.askstring("Agregar Operación", f"Ingrese la expresión para '{symbol}':")
        if expression is None:
            return
        if symbol and expression:
            # Agregar la nueva operación
            self.add_operation(symbol, expression)

    def add_operation(self, symbol, expression):
        """Agrega una nueva operación y su botón correspondiente."""
        num_existing_buttons = len(self.operations_buttons)
        row = num_existing_buttons // 8
        col = num_existing_buttons % 8
        btn = ttk.Button(self.operations_buttons_frame, text=symbol, width=4)
        btn.grid(row=row, column=col, padx=1, pady=1)
        btn.bind("<ButtonPress-1>", self.on_button_press)
        btn.bind("<B1-Motion>", self.on_button_move)
        btn.bind("<ButtonRelease-1>", self.on_button_release)
        self.op_buttons.append((btn, expression))
        self.button_positions[btn] = (row, col)
        self.operations_buttons.append(btn)

def main():
    root = tk.Tk()
    app = NewtonRaphsonApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
