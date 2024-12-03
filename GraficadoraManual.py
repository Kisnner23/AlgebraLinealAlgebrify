# GraficadoraManual.py

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
import sympy as sp
import numpy as np

class GraficadoraManual:
    def __init__(self, master):
        self.master = master
        self.master.overrideredirect(True)  # Eliminar decoraciones estándar
        self.master.geometry("1200x900")
        self.master.configure(bg="#f0f0f0")  # Color de fondo típico de macOS
        self.is_maximized = False

        # Variables para arrastrar la ventana
        self.offset_x = 0
        self.offset_y = 0

        # Crear barra de título personalizada
        self.create_title_bar()

        # Crear el contenido principal
        self.frame = tk.Frame(master, bg="#f0f0f0", padx=20, pady=20)
        self.frame.pack(expand=True, fill='both')

        # Botón para alternar pantalla completa (opcional)
        self.btn_fullscreen = ttk.Button(self.frame, text="Pantalla Completa", command=self.toggle_fullscreen)
        self.btn_fullscreen.pack(pady=(0, 10))

        # Lista Ordenada de Opciones de Graficación
        plot_type_frame = tk.Frame(self.frame, bg="#f0f0f0")
        plot_type_frame.pack(pady=10, anchor='w')

        self.plot_options = [
            "1. Vectores en el plano y el espacio",
            "2. Transformaciones lineales",
            "3. Sistemas de ecuaciones lineales",
            "4. Graficacion por Newton - Raphson",
            "5. Planos y espacios en 3D"
        ]

        self.selected_plot = tk.StringVar()
        self.combo_plot = ttk.Combobox(plot_type_frame, values=self.plot_options, state="readonly", width=60)
        self.combo_plot.set("Seleccione una opción de graficación")
        self.combo_plot.pack(side='left', padx=5)
        self.combo_plot.bind("<<ComboboxSelected>>", self.update_plot_options)

        # Botón de ayuda
        self.btn_help = ttk.Button(self.frame, text="!", width=3, command=self.show_help)
        self.btn_help.pack(pady=(0, 10))

        # Frame para entradas de datos
        self.input_frame = tk.Frame(self.frame, bg="#f0f0f0")
        self.input_frame.pack(pady=10, anchor='w')

        # Campos de Entrada Iniciales
        self.labels_entries = {}

        # Botón para graficar
        self.btn_graficar = ttk.Button(self.frame, text="Graficar", command=self.graficar)
        self.btn_graficar.pack(pady=10)

        # Botón para resolver sistemas de ecuaciones (solo visible para opción 3)
        self.btn_resolver = ttk.Button(self.frame, text="Resolver Sistema de Ecuaciones", command=self.resolver_sistema)
        self.btn_resolver.pack(pady=10)
        self.btn_resolver.pack_forget()  # Oculto por defecto

        # Botón para mejorar gráficos
        self.btn_mejorar = ttk.Button(self.frame, text="Mejorar Gráficos", command=self.toggle_mejorar_graficos, state='disabled')
        self.btn_mejorar.pack(pady=10)

        # Variable para controlar el modo de gráficos mejorados
        self.mejorar_graficos = False

        # Área para el gráfico
        self.figure = plt.Figure(figsize=(10,8), dpi=100)
        self.ax = self.figure.add_subplot(111, projection='3d')  # Inicialmente en 3D para mejorar interactividad
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.frame)
        self.canvas.get_tk_widget().pack(pady=20, fill='both', expand=True)

    def create_title_bar(self):
        title_bar = tk.Frame(self.master, bg="#e0e0e0", relief='raised', bd=0, highlightthickness=0)
        title_bar.pack(fill=tk.X)

        # Botones de control
        btn_close = tk.Canvas(title_bar, width=15, height=15, bg="#e0e0e0", highlightthickness=0)
        btn_close.pack(side=tk.LEFT, padx=10, pady=5)
        btn_close.create_oval(3, 3, 12, 12, fill="#ff5f56", outline="#ff5f56")
        btn_close.bind("<Button-1>", self.close_window)

        btn_minimize = tk.Canvas(title_bar, width=15, height=15, bg="#e0e0e0", highlightthickness=0)
        btn_minimize.pack(side=tk.LEFT, padx=10, pady=5)
        btn_minimize.create_oval(3, 3, 12, 12, fill="#ffbd2e", outline="#ffbd2e")
        btn_minimize.bind("<Button-1>", self.minimize_window)

        btn_maximize = tk.Canvas(title_bar, width=15, height=15, bg="#e0e0e0", highlightthickness=0)
        btn_maximize.pack(side=tk.LEFT, padx=10, pady=5)
        btn_maximize.create_oval(3, 3, 12, 12, fill="#28c940", outline="#28c940")
        btn_maximize.bind("<Button-1>", self.maximize_restore_window)

        # Título de la aplicación
        title_label = tk.Label(title_bar, text="Graficadora Manual - Algebrify", bg="#e0e0e0", fg="#000000", font=("Helvetica", 12))
        title_label.pack(side=tk.LEFT, padx=10)

        # Permitir arrastrar la ventana
        title_bar.bind("<ButtonPress-1>", self.start_move)
        title_bar.bind("<ButtonRelease-1>", self.stop_move)
        title_bar.bind("<B1-Motion>", self.do_move)

        # Opcional: Añadir icono o logo
        # Puedes añadir un logo de Apple o personalizado aquí si lo deseas.

    def start_move(self, event):
        self.offset_x = event.x
        self.offset_y = event.y

    def stop_move(self, event):
        self.offset_x = None
        self.offset_y = None

    def do_move(self, event):
        x = event.x_root - self.offset_x
        y = event.y_root - self.offset_y
        self.master.geometry(f"+{x}+{y}")

    def close_window(self, event=None):
        self.master.destroy()

    def minimize_window(self, event=None):
        self.master.iconify()

    def maximize_restore_window(self, event=None):
        if not self.is_maximized:
            self.previous_geometry = self.master.geometry()
            self.master.geometry(f"{self.master.winfo_screenwidth()}x{self.master.winfo_screenheight()}+0+0")
            self.is_maximized = True
        else:
            self.master.geometry(self.previous_geometry)
            self.is_maximized = False

    def toggle_fullscreen(self):
        is_fullscreen = self.master.attributes('-fullscreen')
        self.master.attributes('-fullscreen', not is_fullscreen)
        if is_fullscreen:
            self.btn_fullscreen.config(text="Pantalla Completa")
        else:
            self.btn_fullscreen.config(text="Salir Pantalla Completa")

    def exit_fullscreen(self, event=None):
        self.master.attributes('-fullscreen', False)
        self.btn_fullscreen.config(text="Pantalla Completa")

    def update_plot_options(self, event=None):
        selected = self.combo_plot.get()
        # Limpiar campos de entrada anteriores
        for widget in self.input_frame.winfo_children():
            widget.destroy()
        self.labels_entries.clear()

        # Ocultar botón de resolver por defecto
        self.btn_resolver.pack_forget()

        # Definir campos de entrada según la opción seleccionada
        if selected.startswith("1. Vectores"):
            self.add_entry("X", "Ingrese los valores de X (separados por comas):")
            self.add_entry("Y", "Ingrese los valores de Y (separados por comas):")
            self.add_entry("Z", "Ingrese los valores de Z (separados por comas):", optional=True)
            self.add_entry("U", "Ingrese los valores de U (componente X de los vectores, separados por comas):")
            self.add_entry("V", "Ingrese los valores de V (componente Y de los vectores, separados por comas):")
            self.add_entry("W", "Ingrese los valores de W (componente Z de los vectores, separados por comas):", optional=True)
        
        elif selected.startswith("2. Transformaciones"):
            self.add_entry("X", "Ingrese los valores de X (separados por comas):")
            self.add_entry("Y", "Ingrese los valores de Y (separados por comas):")
            self.add_entry("Matriz", "Ingrese la matriz de transformación (filas separadas por ';', elementos por comas):")

        elif selected.startswith("3. Sistemas de ecuaciones"):
            # No requiere entradas aquí; usar botón para resolver
            self.btn_resolver.pack(pady=10)

        elif selected.startswith("4. Graficacion por Newton - Raphson"):
            self.add_entry("Funcion", "Ingrese la función f(x):")
            self.add_entry("Derivada", "Ingrese la derivada f'(x):")
            self.add_entry("Inicial", "Ingrese el valor inicial x₀:")
            self.add_entry("Tolerancia", "Ingrese la tolerancia (e.g., 1e-5):")
            self.add_entry("Max Iteraciones", "Ingrese el máximo de iteraciones:")

        elif selected.startswith("5. Planos y espacios"):
            self.add_entry("Plano 1", "Ingrese los coeficientes del primer plano (A,B,C,D separados por comas):")
            self.add_entry("Plano 2", "Ingrese los coeficientes del segundo plano (A,B,C,D separados por comas):")
            self.add_entry("Plano 3", "Ingrese los coeficientes del tercer plano (A,B,C,D separados por comas):", optional=True)

    def add_entry(self, key, label_text, optional=False):
        row = len(self.labels_entries)
        label = tk.Label(self.input_frame, text=label_text, bg="#f0f0f0")
        label.grid(row=row, column=0, sticky='e', pady=5, padx=5)
        entry = ttk.Entry(self.input_frame, width=80)
        entry.grid(row=row, column=1, pady=5, padx=5)
        self.labels_entries[key] = (label, entry)
        if optional:
            label.config(fg="grey")
            entry.config(fg="grey")

    def show_help(self):
        selected = self.combo_plot.get()
        help_message = ""
        if selected.startswith("1. Vectores"):
            help_message = (
                "Para graficar vectores en el plano y el espacio:\n"
                "- **X:** Ingrese las coordenadas X de los puntos de inicio de los vectores, separados por comas.\n"
                "- **Y:** Ingrese las coordenadas Y de los puntos de inicio de los vectores, separados por comas.\n"
                "- **Z:** (Opcional) Ingrese las coordenadas Z de los puntos de inicio de los vectores, separados por comas (para 3D).\n"
                "- **U:** Ingrese las componentes U (X) de los vectores, separados por comas.\n"
                "- **V:** Ingrese las componentes V (Y) de los vectores, separados por comas.\n"
                "- **W:** (Opcional) Ingrese las componentes W (Z) de los vectores, separados por comas (para 3D).\n\n"
                "Ejemplo para 2D:\nX: 0, 1\nY: 0, 1\nU: 1, 2\nV: 1, 2"
            )
        
        elif selected.startswith("2. Transformaciones"):
            help_message = (
                "Para graficar transformaciones lineales:\n"
                "- **X:** Ingrese las coordenadas X de los puntos a transformar, separados por comas.\n"
                "- **Y:** Ingrese las coordenadas Y de los puntos a transformar, separados por comas.\n"
                "- **Matriz:** Ingrese la matriz de transformación en el formato `a,b;c,d` para 2x2 o `a,b,c;d,e,f;g,h,i` para 3x3.\n\n"
                "Ejemplo de matriz 2x2:\n1,2;3,4"
            )
        
        elif selected.startswith("3. Sistemas de ecuaciones"):
            help_message = (
                "Para graficar sistemas de ecuaciones lineales:\n"
                "- Utiliza el botón **Resolver Sistema de Ecuaciones** para ingresar y resolver un sistema de 2 ecuaciones con 2 incógnitas.\n"
                "- La solución se mostrará en la gráfica donde se intersectan las líneas correspondientes a las ecuaciones."
            )
        
        elif selected.startswith("4. Graficacion por Newton - Raphson"):
            help_message = (
                "Para graficar el método de Newton-Raphson:\n"
                "- **Función f(x):** Ingrese la función cuya raíz desea encontrar.\n"
                "- **Derivada f'(x):** Ingrese la derivada de la función.\n"
                "- **Inicial x₀:** Ingrese el valor inicial para el método.\n"
                "- **Tolerancia:** Ingrese la tolerancia para la convergencia (por ejemplo, 1e-5).\n"
                "- **Max Iteraciones:** Ingrese el número máximo de iteraciones permitidas.\n\n"
                "Ejemplo:\n"
                "f(x) = x^2 - 2\n"
                "f'(x) = 2x\n"
                "Inicial x₀ = 1\n"
                "Tolerancia = 1e-5\n"
                "Max Iteraciones = 10"
            )
        
        elif selected.startswith("5. Planos y espacios"):
            help_message = (
                "Para graficar planos en 3D:\n"
                "- **Plano 1:** Ingrese los coeficientes A, B, C, D del primer plano en la ecuación Ax + By + Cz + D = 0, separados por comas.\n"
                "- **Plano 2:** Igual que Plano 1 para el segundo plano.\n"
                "- **Plano 3:** (Opcional) Ingrese los coeficientes para un tercer plano.\n\n"
                "Ejemplo para dos planos:\nPlano 1: 1,1,1,-6\nPlano 2: 0,1,-1,-3"
            )
        
        else:
            help_message = "Seleccione una opción de graficación para obtener ayuda."

        messagebox.showinfo("Ayuda - Cómo introducir los datos", help_message)

    def toggle_mejorar_graficos(self):
        if not hasattr(self, 'current_plot_data'):
            messagebox.showwarning("Sin Gráfica", "Por favor, genera una gráfica primero.")
            return

        selected = self.combo_plot.get()
        tipo_grafica = self.current_plot_data['tipo']

        # Solo permitir mejorar gráficas 3D
        if not tipo_grafica in ['vectores', 'transformaciones', 'planos']:
            messagebox.showwarning("No es 3D", "La mejora gráfica solo está disponible para gráficas en 3D.")
            return

        self.mejorar_graficos = not self.mejorar_graficos
        if self.mejorar_graficos:
            self.btn_mejorar.config(text="Desactivar Mejorar Gráficos")
            # Abrir una nueva ventana con la gráfica mejorada
            self.abrir_ventana_mejorada()
        else:
            self.btn_mejorar.config(text="Mejorar Gráficos")
            # Cerrar la ventana mejorada si está abierta
            if hasattr(self, 'ventana_mejorada') and self.ventana_mejorada.winfo_exists():
                self.ventana_mejorada.destroy()

    def abrir_ventana_mejorada(self):
        # Crear una nueva ventana
        self.ventana_mejorada = tk.Toplevel(self.master)
        self.ventana_mejorada.title("Gráfica Mejorada - Algebrify")
        self.ventana_mejorada.geometry("1200x900")
        self.ventana_mejorada.resizable(True, True)

        # Crear una figura de matplotlib mejorada
        figura_mejorada = plt.Figure(figsize=(12,10), dpi=100)
        if self.current_plot_data['tipo'] in ['vectores', 'transformaciones', 'planos']:
            ax_mejorada = figura_mejorada.add_subplot(111, projection='3d')
        else:
            ax_mejorada = figura_mejorada.add_subplot(111)

        # Copiar los datos de la gráfica actual según el tipo
        tipo_grafica = self.current_plot_data['tipo']
        data = self.current_plot_data['data']

        if tipo_grafica == 'vectores':
            x = data['x']
            y = data['y']
            u = data['u']
            v = data['v']
            z = data.get('z')
            w = data.get('w')

            is_3d = z is not None and w is not None

            if is_3d:
                for xi, yi, zi, ui, vi, wi in zip(x, y, z, u, v, w):
                    ax_mejorada.quiver(xi, yi, zi, ui, vi, wi, length=1, normalize=True, arrow_length_ratio=0.1)
                ax_mejorada.set_title("Vectores en 3D - Mejorado", fontsize=18)
                ax_mejorada.set_xlabel("X", fontsize=14)
                ax_mejorada.set_ylabel("Y", fontsize=14)
                ax_mejorada.set_zlabel("Z", fontsize=14)
            else:
                for xi, yi, ui, vi in zip(x, y, u, v):
                    ax_mejorada.arrow(xi, yi, ui, vi, head_width=0.2, head_length=0.2, fc='k', ec='k')
                ax_mejorada.set_title("Vectores en 2D - Mejorado", fontsize=18)
                ax_mejorada.set_xlabel("X", fontsize=14)
                ax_mejorada.set_ylabel("Y", fontsize=14)

        elif tipo_grafica == 'transformaciones':
            x = data['x']
            y = data['y']
            matriz = data['matriz']

            if matriz.shape[0] == 3:
                points = np.vstack((x, y, np.zeros_like(x)))
                transformed = matriz @ points
                ax_mejorada.scatter(transformed[0, :], transformed[1, :], transformed[2, :], c='g', marker='^', label='Transformado')
                ax_mejorada.scatter(points[0, :], points[1, :], points[2, :], c='b', marker='o', label='Original')
                ax_mejorada.set_title("Transformación Lineal 3D - Mejorado", fontsize=18)
                ax_mejorada.set_xlabel("X", fontsize=14)
                ax_mejorada.set_ylabel("Y", fontsize=14)
                ax_mejorada.set_zlabel("Z", fontsize=14)
            else:
                points = np.vstack((x, y))
                transformed = matriz @ points
                ax_mejorada.scatter(transformed[0, :], transformed[1, :], c='g', marker='^', label='Transformado')
                ax_mejorada.scatter(points[0, :], points[1, :], c='b', marker='o', label='Original')
                ax_mejorada.set_title("Transformación Lineal 2D - Mejorado", fontsize=18)
                ax_mejorada.set_xlabel("X", fontsize=14)
                ax_mejorada.set_ylabel("Y", fontsize=14)

        elif tipo_grafica == 'planos':
            coef1 = data['coef1']
            coef2 = data['coef2']
            coef3 = data.get('coef3')

            # Definir rango
            x = np.linspace(-10, 10, 20)
            y = np.linspace(-10, 10, 20)
            X, Y = np.meshgrid(x, y)

            # Calcular Z para cada plano
            try:
                Z1 = (-coef1[0] * X - coef1[1] * Y - coef1[3]) / coef1[2]
                Z2 = (-coef2[0] * X - coef2[1] * Y - coef2[3]) / coef2[2]
                if coef3:
                    Z3 = (-coef3[0] * X - coef3[1] * Y - coef3[3]) / coef3[2]
            except ZeroDivisionError:
                messagebox.showerror("Error", "El coeficiente de Z no puede ser cero en la ecuación del plano.")
                return

            # Graficar los planos
            ax_mejorada.plot_surface(X, Y, Z1, alpha=0.5, color='r')
            ax_mejorada.plot_surface(X, Y, Z2, alpha=0.5, color='g')
            if coef3:
                ax_mejorada.plot_surface(X, Y, Z3, alpha=0.5, color='b')

            ax_mejorada.set_title("Planos en 3D - Mejorado", fontsize=18)
            ax_mejorada.set_xlabel("X", fontsize=14)
            ax_mejorada.set_ylabel("Y", fontsize=14)
            ax_mejorada.set_zlabel("Z", fontsize=14)

            # Agregar leyenda manualmente
            from matplotlib.patches import Patch
            legend_elements = [
                Patch(facecolor='r', edgecolor='r', label='Plano 1'),
                Patch(facecolor='g', edgecolor='g', label='Plano 2')
            ]
            if coef3:
                legend_elements.append(Patch(facecolor='b', edgecolor='b', label='Plano 3'))
            ax_mejorada.legend(handles=legend_elements)

        # Configurar interactividad mejorada
        ax_mejorada.set_title(self.ax.get_title(), fontsize=18)
        ax_mejorada.set_xlabel(self.ax.get_xlabel(), fontsize=14)
        ax_mejorada.set_ylabel(self.ax.get_ylabel(), fontsize=14)
        if hasattr(ax_mejorada, 'set_zlabel') and self.ax.get_zlabel():
            ax_mejorada.set_zlabel(self.ax.get_zlabel(), fontsize=14)
        ax_mejorada.legend()
        ax_mejorada.grid(True)

        # Crear un canvas para la figura mejorada
        canvas_mejorado = FigureCanvasTkAgg(figura_mejorada, master=self.ventana_mejorada)
        canvas_mejorado.draw()
        canvas_mejorado.get_tk_widget().pack(pady=20, fill='both', expand=True)

        # Añadir toolbar para mayor interactividad
        toolbar_frame = tk.Frame(self.ventana_mejorada)
        toolbar_frame.pack()
        from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
        toolbar = NavigationToolbar2Tk(canvas_mejorado, toolbar_frame)
        toolbar.update()

    def graficar(self):
        selected = self.combo_plot.get()
        if selected == "Seleccione una opción de graficación":
            messagebox.showwarning("Seleccionar Opción", "Por favor, seleccione una opción de graficación.")
            return

        try:
            if selected.startswith("1. Vectores"):
                self.graficar_vectores()
            elif selected.startswith("2. Transformaciones"):
                self.graficar_transformaciones()
            elif selected.startswith("3. Sistemas de ecuaciones"):
                messagebox.showinfo("Información", "Por favor, usa el botón 'Resolver Sistema de Ecuaciones' para esta opción.")
            elif selected.startswith("4. Graficacion por Newton - Raphson"):
                self.graficar_newton_raphson()
            elif selected.startswith("5. Planos y espacios"):
                self.graficar_planos()
            else:
                messagebox.showerror("Error", "Opción de graficación no reconocida.")
        except ValueError as ve:
            messagebox.showerror("Entrada Inválida", f"Error en los datos ingresados:\n{ve}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado:\n{e}")
        else:
            # Habilitar el botón "Mejorar Gráficos" después de generar una gráfica
            self.btn_mejorar.config(state='normal')

    def graficar_vectores(self):
        x_str = self.labels_entries.get("X")[1].get()
        y_str = self.labels_entries.get("Y")[1].get()
        u_str = self.labels_entries.get("U")[1].get()
        v_str = self.labels_entries.get("V")[1].get()
        z_str = self.labels_entries.get("Z")[1].get() if "Z" in self.labels_entries else None
        w_str = self.labels_entries.get("W")[1].get() if "W" in self.labels_entries else None

        x = [float(i.strip()) for i in x_str.split(',')]
        y = [float(i.strip()) for i in y_str.split(',')]
        u = [float(i.strip()) for i in u_str.split(',')]
        v = [float(i.strip()) for i in v_str.split(',')]
        z = [float(i.strip()) for i in z_str.split(',')] if z_str else None
        w = [float(i.strip()) for i in w_str.split(',')] if w_str else None

        if z and len(x) != len(z):
            raise ValueError("Las listas de X y Z deben tener la misma cantidad de elementos.")
        if w and len(u) != len(w):
            raise ValueError("Las listas de U y W deben tener la misma cantidad de elementos.")

        # Limpiar el gráfico anterior
        self.ax.clear()

        # Determinar si es 2D o 3D
        is_3d = z is not None and w is not None

        if is_3d:
            self.ax = self.figure.add_subplot(111, projection='3d')
            for xi, yi, zi, ui, vi, wi in zip(x, y, z, u, v, w):
                self.ax.quiver(xi, yi, zi, ui, vi, wi, length=1, normalize=True)
            self.ax.set_title("Vectores en 3D", fontsize=16)
            self.ax.set_xlabel("X", fontsize=12)
            self.ax.set_ylabel("Y", fontsize=12)
            self.ax.set_zlabel("Z", fontsize=12)
        else:
            self.ax = self.figure.add_subplot(111)
            for xi, yi, ui, vi in zip(x, y, u, v):
                self.ax.arrow(xi, yi, ui, vi, head_width=0.2, head_length=0.2, fc='k', ec='k')
            self.ax.set_title("Vectores en 2D", fontsize=16)
            self.ax.set_xlabel("X", fontsize=12)
            self.ax.set_ylabel("Y", fontsize=12)

        self.ax.grid(True)
        self.canvas.draw()

        # Guardar los datos de la gráfica actual
        self.current_plot_data = {
            'tipo': 'vectores',
            'data': {
                'x': x,
                'y': y,
                'u': u,
                'v': v,
                'z': z,
                'w': w
            }
        }

    def graficar_transformaciones(self):
        x_str = self.labels_entries.get("X")[1].get()
        y_str = self.labels_entries.get("Y")[1].get()
        matriz_str = self.labels_entries.get("Matriz")[1].get()

        x = [float(i.strip()) for i in x_str.split(',')]
        y = [float(i.strip()) for i in y_str.split(',')]
        matriz = np.array([[float(num) for num in row.split(',')] for row in matriz_str.split(';')])

        if matriz.shape not in [(2, 2), (3, 3)]:
            raise ValueError("La matriz de transformación debe ser de tamaño 2x2 o 3x3.")

        if len(x) != len(y):
            raise ValueError("Las listas de X e Y deben tener la misma cantidad de elementos.")

        # Crear matriz de puntos
        points = np.vstack((x, y))
        if matriz.shape[0] == 3:
            # Extender a 3D si es necesario
            points = np.vstack((points, np.zeros((1, points.shape[1]))))

        # Aplicar transformación
        transformed = matriz @ points

        # Limpiar el gráfico anterior
        if matriz.shape[0] == 3:
            self.ax = self.figure.add_subplot(111, projection='3d')
            self.ax.scatter(transformed[0, :], transformed[1, :], transformed[2, :], c='g', marker='^', label='Transformado')
            self.ax.scatter(points[0, :], points[1, :], points[2, :], c='b', marker='o', label='Original')
            self.ax.set_zlabel("Z", fontsize=12)
        else:
            self.ax = self.figure.add_subplot(111)
            self.ax.scatter(transformed[0, :], transformed[1, :], c='g', marker='^', label='Transformado')
            self.ax.scatter(points[0, :], points[1, :], c='b', marker='o', label='Original')

        # Configurar el gráfico
        self.ax.set_title("Transformación Lineal", fontsize=16)
        self.ax.set_xlabel("X", fontsize=12)
        self.ax.set_ylabel("Y", fontsize=12)
        if matriz.shape[0] == 3:
            self.ax.set_zlabel("Z", fontsize=12)
        self.ax.legend()
        self.ax.grid(True)

        self.canvas.draw()

        # Guardar los datos de la gráfica actual
        self.current_plot_data = {
            'tipo': 'transformaciones',
            'data': {
                'x': x,
                'y': y,
                'matriz': matriz
            }
        }

    def graficar_newton_raphson(self):
        funcion_str = self.labels_entries.get("Funcion")[1].get()
        derivada_str = self.labels_entries.get("Derivada")[1].get()
        inicial_str = self.labels_entries.get("Inicial")[1].get()
        tolerancia_str = self.labels_entries.get("Tolerancia")[1].get()
        max_iter_str = self.labels_entries.get("Max Iteraciones")[1].get()

        # Convertir entradas
        try:
            x0 = float(inicial_str)
            tolerancia = float(tolerancia_str)
            max_iter = int(max_iter_str)
        except ValueError:
            raise ValueError("Inicial, Tolerancia y Max Iteraciones deben ser números.")

        # Definir variables simbólicas
        x = sp.symbols('x')

        # Convertir las cadenas a expresiones simbólicas
        try:
            funcion = sp.sympify(funcion_str)
            derivada = sp.sympify(derivada_str)
        except sp.SympifyError:
            raise ValueError("La función y su derivada deben estar correctamente definidas.")

        # Convertir a funciones lambda
        f = sp.lambdify(x, funcion, modules=['numpy'])
        f_prime = sp.lambdify(x, derivada, modules=['numpy'])

        # Inicializar variables para Newton-Raphson
        iteraciones = 0
        error = float('inf')
        x_vals = [x0]
        f_vals = [f(x0)]
        errores = [error]

        # Ejecutar el método de Newton-Raphson
        while error > tolerancia and iteraciones < max_iter:
            try:
                x1 = x0 - f(x0)/f_prime(x0)
            except ZeroDivisionError:
                messagebox.showerror("Error", "La derivada se volvió cero. Método de Newton-Raphson falla.")
                return
            error = abs(x1 - x0)
            x_vals.append(x1)
            f_vals.append(f(x1))
            errores.append(error)
            x0 = x1
            iteraciones += 1

        if error > tolerancia:
            messagebox.showwarning("Advertencia", "El método no convergió en el número máximo de iteraciones.")
        else:
            messagebox.showinfo("Convergencia", f"El método convergió a x = {x1} en {iteraciones} iteraciones.")

        # Graficar la función y las iteraciones
        self.ax.clear()
        x_plot = np.linspace(x0 - 10, x0 + 10, 400)
        y_plot = f(x_plot)

        if isinstance(self.ax, Axes3D):
            # Cambiar a 2D si es necesario
            self.ax = self.figure.add_subplot(111)

        self.ax.plot(x_plot, y_plot, label='f(x)')
        self.ax.axhline(0, color='black', linewidth=0.5)

        # Graficar las aproximaciones
        for i in range(len(x_vals)-1):
            self.ax.plot([x_vals[i], x_vals[i+1]], [f(x_vals[i]), 0], 'ro-')
            self.ax.plot([x_vals[i+1], x_vals[i+1]], [0, f(x_vals[i+1])], 'ro-')

        self.ax.set_title("Método de Newton-Raphson", fontsize=16)
        self.ax.set_xlabel("x", fontsize=12)
        self.ax.set_ylabel("f(x)", fontsize=12)
        self.ax.legend()
        self.ax.grid(True)
        self.canvas.draw()

        # Guardar los datos de la gráfica actual
        self.current_plot_data = {
            'tipo': 'newton_raphson',
            'data': {
                'funcion': funcion,
                'derivada': derivada,
                'x_vals': x_vals,
                'f_vals': f_vals,
                'errores': errores,
                'convergio': error <= tolerancia,
                'iteraciones': iteraciones
            }
        }

    def graficar_planos(self):
        plano1_str = self.labels_entries.get("Plano 1")[1].get()
        plano2_str = self.labels_entries.get("Plano 2")[1].get()
        plano3_str = self.labels_entries.get("Plano 3")[1].get() if "Plano 3" in self.labels_entries else None

        # Convertir coeficientes a A, B, C, D
        coef1 = [float(i.strip()) for i in plano1_str.split(',')]
        coef2 = [float(i.strip()) for i in plano2_str.split(',')]
        coef3 = [float(i.strip()) for i in plano3_str.split(',')] if plano3_str else None

        # Definir rango
        x = np.linspace(-10, 10, 20)
        y = np.linspace(-10, 10, 20)
        X, Y = np.meshgrid(x, y)

        # Calcular Z para cada plano
        try:
            Z1 = (-coef1[0] * X - coef1[1] * Y - coef1[3]) / coef1[2]
            Z2 = (-coef2[0] * X - coef2[1] * Y - coef2[3]) / coef2[2]
            if coef3:
                Z3 = (-coef3[0] * X - coef3[1] * Y - coef3[3]) / coef3[2]
        except ZeroDivisionError:
            raise ValueError("El coeficiente de Z no puede ser cero en la ecuación del plano.")

        # Limpiar el gráfico anterior
        self.ax.clear()

        # Configurar el gráfico en 3D
        self.ax = self.figure.add_subplot(111, projection='3d')

        # Graficar los planos
        self.ax.plot_surface(X, Y, Z1, alpha=0.5, color='r')
        self.ax.plot_surface(X, Y, Z2, alpha=0.5, color='g')
        if coef3:
            self.ax.plot_surface(X, Y, Z3, alpha=0.5, color='b')

        self.ax.set_title("Planos en 3D", fontsize=16)
        self.ax.set_xlabel("X", fontsize=12)
        self.ax.set_ylabel("Y", fontsize=12)
        self.ax.set_zlabel("Z", fontsize=12)
        self.ax.grid(True)

        # Agregar leyenda manualmente
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='r', edgecolor='r', label='Plano 1'),
            Patch(facecolor='g', edgecolor='g', label='Plano 2')
        ]
        if coef3:
            legend_elements.append(Patch(facecolor='b', edgecolor='b', label='Plano 3'))
        self.ax.legend(handles=legend_elements)

        self.canvas.draw()

        # Guardar los datos de la gráfica actual
        self.current_plot_data = {
            'tipo': 'planos',
            'data': {
                'coef1': coef1,
                'coef2': coef2,
                'coef3': coef3
            }
        }

    def resolver_sistema(self):
        # Ventana para ingresar el sistema de ecuaciones
        sistema_window = tk.Toplevel(self.master)
        sistema_window.title("Resolver Sistema de Ecuaciones")
        sistema_window.geometry("500x400")
        sistema_window.resizable(False, False)

        frame = tk.Frame(sistema_window, padx=20, pady=20, bg="#f0f0f0")
        frame.pack(expand=True, fill='both')

        # Instrucciones
        instruccion = tk.Label(frame, text="Ingrese un sistema de 2 ecuaciones lineales con 2 incógnitas (x y):", wraplength=460, justify="left", bg="#f0f0f0")
        instruccion.pack(pady=10)

        # Entrada para la primera ecuación
        eq1_frame = tk.Frame(frame, bg="#f0f0f0")
        eq1_frame.pack(pady=5)
        eq1_label = tk.Label(eq1_frame, text="Ecuación 1:", bg="#f0f0f0")
        eq1_label.pack(side='left')
        self.eq1_entry = ttk.Entry(eq1_frame, width=40)
        self.eq1_entry.pack(side='left', padx=5)

        # Entrada para la segunda ecuación
        eq2_frame = tk.Frame(frame, bg="#f0f0f0")
        eq2_frame.pack(pady=5)
        eq2_label = tk.Label(eq2_frame, text="Ecuación 2:", bg="#f0f0f0")
        eq2_label.pack(side='left')
        self.eq2_entry = ttk.Entry(eq2_frame, width=40)
        self.eq2_entry.pack(side='left', padx=5)

        # Botón para resolver
        btn_resolver = ttk.Button(frame, text="Resolver", command=lambda: self.resolver(eq1_window=sistema_window))
        btn_resolver.pack(pady=10)

        # Área para mostrar la solución
        self.solucion_text = tk.Text(frame, height=5, width=58, state='disabled')
        self.solucion_text.pack(pady=10)

    def resolver(self, eq1_window):
        eq1 = self.eq1_entry.get()
        eq2 = self.eq2_entry.get()

        try:
            # Definir las variables
            x, y = sp.symbols('x y')

            # Convertir las ecuaciones de string a sympy
            ecuacion1 = sp.sympify(eq1)
            ecuacion2 = sp.sympify(eq2)

            # Resolver el sistema
            solucion = sp.solve((ecuacion1, ecuacion2), (x, y))

            if solucion:
                solucion_str = f"Solución:\n{x} = {solucion[x]}\n{y} = {solucion[y]}"
                self.solucion_text.config(state='normal')
                self.solucion_text.delete('1.0', tk.END)
                self.solucion_text.insert(tk.END, solucion_str)
                self.solucion_text.config(state='disabled')

                # Graficar las ecuaciones y la solución
                self.graficar_sistema(ecuacion1, ecuacion2, solucion)
            else:
                self.solucion_text.config(state='normal')
                self.solucion_text.delete('1.0', tk.END)
                self.solucion_text.insert(tk.END, "El sistema no tiene solución única.")
                self.solucion_text.config(state='disabled')

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al resolver el sistema:\n{e}")

    def graficar_sistema(self, eq1, eq2, solucion):
        # Crear un rango de valores para x
        x_vals = np.linspace(-10, 10, 400)
        y_vals_eq1 = []
        y_vals_eq2 = []

        try:
            expr_eq1 = sp.solve(eq1, sp.Symbol('y'))
            expr_eq2 = sp.solve(eq2, sp.Symbol('y'))
            if expr_eq1:
                y_vals_eq1 = [float(expr_eq1[0].subs(sp.Symbol('x'), val)) for val in x_vals]
            else:
                y_vals_eq1 = [np.nan]*len(x_vals)

            if expr_eq2:
                y_vals_eq2 = [float(expr_eq2[0].subs(sp.Symbol('x'), val)) for val in x_vals]
            else:
                y_vals_eq2 = [np.nan]*len(x_vals)
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al graficar las ecuaciones:\n{e}")
            return

        # Limpiar el gráfico anterior
        self.ax.clear()

        # Determinar si el gráfico está en 3D o 2D
        is_3d = isinstance(self.ax, Axes3D)

        if is_3d:
            self.ax = self.figure.add_subplot(111, projection='3d')
            # Graficar las ecuaciones como líneas en el plano XY
            self.ax.plot(x_vals, y_vals_eq1, zs=0, zdir='z', label='Ecuación 1')
            self.ax.plot(x_vals, y_vals_eq2, zs=0, zdir='z', label='Ecuación 2')
            self.ax.scatter(solucion[sp.Symbol('x')], solucion[sp.Symbol('y')], zs=0, color='r', marker='o', label='Solución')
            self.ax.set_zlim(-1, 1)  # Limitar Z para mejor visualización
            self.ax.set_xlabel("X", fontsize=12)
            self.ax.set_ylabel("Y", fontsize=12)
            self.ax.set_zlabel("Z", fontsize=12)
        else:
            # Graficar las ecuaciones
            self.ax.plot(x_vals, y_vals_eq1, label='Ecuación 1')
            self.ax.plot(x_vals, y_vals_eq2, label='Ecuación 2')

            # Graficar la solución
            self.ax.plot(solucion[sp.Symbol('x')], solucion[sp.Symbol('y')], 'ro', label='Solución')

            # Configurar el gráfico
            self.ax.set_title("Sistema de Ecuaciones Resuelto", fontsize=16)
            self.ax.set_xlabel("X", fontsize=12)
            self.ax.set_ylabel("Y", fontsize=12)
            self.ax.legend()
            self.ax.grid(True)

        self.canvas.draw()

        # Guardar los datos de la gráfica actual
        self.current_plot_data = {
            'tipo': 'sistemas',
            'data': {
                'eq1': eq1,
                'eq2': eq2,
                'solucion': solucion
            }
        }

    def graficar_planos(self):
        plano1_str = self.labels_entries.get("Plano 1")[1].get()
        plano2_str = self.labels_entries.get("Plano 2")[1].get()
        plano3_str = self.labels_entries.get("Plano 3")[1].get() if "Plano 3" in self.labels_entries else None

        # Convertir coeficientes a A, B, C, D
        coef1 = [float(i.strip()) for i in plano1_str.split(',')]
        coef2 = [float(i.strip()) for i in plano2_str.split(',')]
        coef3 = [float(i.strip()) for i in plano3_str.split(',')] if plano3_str else None

        # Definir rango
        x = np.linspace(-10, 10, 20)
        y = np.linspace(-10, 10, 20)
        X, Y = np.meshgrid(x, y)

        # Calcular Z para cada plano
        try:
            Z1 = (-coef1[0] * X - coef1[1] * Y - coef1[3]) / coef1[2]
            Z2 = (-coef2[0] * X - coef2[1] * Y - coef2[3]) / coef2[2]
            if coef3:
                Z3 = (-coef3[0] * X - coef3[1] * Y - coef3[3]) / coef3[2]
        except ZeroDivisionError:
            raise ValueError("El coeficiente de Z no puede ser cero en la ecuación del plano.")

        # Limpiar el gráfico anterior
        self.ax.clear()

        # Configurar el gráfico en 3D
        self.ax = self.figure.add_subplot(111, projection='3d')

        # Graficar los planos
        self.ax.plot_surface(X, Y, Z1, alpha=0.5, color='r')
        self.ax.plot_surface(X, Y, Z2, alpha=0.5, color='g')
        if coef3:
            self.ax.plot_surface(X, Y, Z3, alpha=0.5, color='b')

        self.ax.set_title("Planos en 3D", fontsize=16)
        self.ax.set_xlabel("X", fontsize=12)
        self.ax.set_ylabel("Y", fontsize=12)
        self.ax.set_zlabel("Z", fontsize=12)
        self.ax.grid(True)

        # Agregar leyenda manualmente
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='r', edgecolor='r', label='Plano 1'),
            Patch(facecolor='g', edgecolor='g', label='Plano 2')
        ]
        if coef3:
            legend_elements.append(Patch(facecolor='b', edgecolor='b', label='Plano 3'))
        self.ax.legend(handles=legend_elements)

        self.canvas.draw()

        # Guardar los datos de la gráfica actual
        self.current_plot_data = {
            'tipo': 'planos',
            'data': {
                'coef1': coef1,
                'coef2': coef2,
                'coef3': coef3
            }
        }

def main():
    root = tk.Tk()
    app = GraficadoraManual(root)
    root.mainloop()

if __name__ == "__main__":
    main()
