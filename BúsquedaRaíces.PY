import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import math
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import platform
import re  # Importamos el módulo re para expresiones regulares

def preprocess_expression(expr):
    # Reemplazar '^' por '**'
    expr = expr.replace('^', '**')
    
    # Insertar '*' entre número y letra (por ejemplo, '2x' -> '2*x')
    expr = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', expr)
    
    # Lista de nombres de funciones
    function_names = ['sin', 'cos', 'tan', 'exp', 'log', 'ln', 'sqrt', 'arcsin', 'arccos', 'arctan',
                      'sinh', 'cosh', 'tanh', 'arcsinh', 'arccosh', 'arctanh', 'sec', 'csc', 'cot', 'abs']
    func_pattern = '|'.join(function_names)
    
    # Insertar '*' entre variable y función (por ejemplo, 'xsin(x)' -> 'x*sin(x)')
    expr = re.sub(r'([a-zA-Z0-9_])(\s*)(' + func_pattern + r')\(', r'\1*\3(', expr)
    
    # Agregar paréntesis a funciones si no están presentes (por ejemplo, 'sin x' -> 'sin(x)')
    for func in function_names:
        expr = re.sub(r'\b' + func + r'\s+([^\s\(\)]+)', func + r'(\1)', expr)
    return expr

# Función para evaluar expresiones matemáticas de forma segura
def safe_eval(expr, x):
    allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
    allowed_names['x'] = x
    allowed_names['sec'] = lambda x: 1 / math.cos(x)
    allowed_names['csc'] = lambda x: 1 / math.sin(x)
    allowed_names['cot'] = lambda x: 1 / math.tan(x)
    allowed_names['ln'] = math.log  # Alias para ln
    allowed_names['log10'] = math.log10
    expr = preprocess_expression(expr)  # Preprocesar la expresión
    try:
        return eval(expr, {"__builtins__": {}}, allowed_names)
    except Exception as e:
        raise ValueError(f"Error en la expresión: {e}")

# Método de la Falsa Posición
def falsa_posicion(func, a, b, tol, max_iter):
    fa = safe_eval(func, a)
    fb = safe_eval(func, b)
    if fa * fb >= 0:
        raise ValueError("f(a) y f(b) deben tener signos opuestos.")
    
    iterations_data = []
    for i in range(max_iter):
        c = b - fb * (b - a) / (fb - fa)
        fc = safe_eval(func, c)
        iterations_data.append({
            'Iteración': i+1,
            'a': a,
            'b': b,
            'c': c,
            'f(a)': fa,
            'f(b)': fb,
            'f(c)': fc,
        })
        if abs(fc) < tol:
            return c, i+1, iterations_data
        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
    raise ValueError("Método de la Falsa Posición no converge.")

# Método de la Secante
def secante(func, x0, x1, tol, max_iter):
    f_x0 = safe_eval(func, x0)
    f_x1 = safe_eval(func, x1)
    iterations_data = []
    for i in range(max_iter):
        if f_x1 - f_x0 == 0:
            raise ValueError("División por cero en el método de la Secante.")
        x2 = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)
        f_x2 = safe_eval(func, x2)
        iterations_data.append({
            'Iteración': i+1,
            'x0': x0,
            'x1': x1,
            'x2': x2,
            'f(x0)': f_x0,
            'f(x1)': f_x1,
            'f(x2)': f_x2,
        })
        if abs(f_x2) < tol:
            return x2, i+1, iterations_data
        x0, f_x0 = x1, f_x1
        x1, f_x1 = x2, f_x2
    raise ValueError("Método de la Secante no converge.")

class VirtualKeyboard:
    def __init__(self, app):
        self.app = app
        self.window = tk.Toplevel()
        self.window.title("Teclado de Símbolos")
        self.window.geometry("700x500")  # Tamaño ajustado para scroll
        self.window.resizable(False, False)
        self.window.attributes("-topmost", True)

        # Hacer la ventana draggable
        self.window.bind('<ButtonPress-1>', self.start_move)
        self.window.bind('<ButtonRelease-1>', self.stop_move)
        self.window.bind('<B1-Motion>', self.do_move)
        self.offset_x = 0
        self.offset_y = 0

        # Crear un Canvas con Scrollbar
        self.canvas = tk.Canvas(self.window, bg="#2E2E2E")
        self.scrollbar = ttk.Scrollbar(self.window, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Crear un frame dentro del canvas
        self.inner_frame = tk.Frame(self.canvas, bg="#2E2E2E")
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor='nw')

        self.inner_frame.bind("<Configure>", self.on_frame_configure)

        # Definir las secciones y sus botones
        sections = {
            "Trigonométricas básicas": [
                ("sin\n(seno)", "sin("),
                ("cos\n(coseno)", "cos("),
                ("tan\n(tangente)", "tan(")
            ],
            "Trigonométricas inversas": [
                ("arcsin\narcsin o sin⁻¹", "arcsin("),
                ("arccos\narccos o cos⁻¹", "arccos("),
                ("arctan\narctan o tan⁻¹", "arctan(")
            ],
            "Hiperbólicas": [
                ("sinh\nsinh (seno hiperbólico)", "sinh("),
                ("cosh\ncosh (coseno hiperbólico)", "cosh("),
                ("tanh\ntanh (tangente hiperbólica)", "tanh(")
            ],
            "Hiperbólicas inversas": [
                ("arcsinh\narcsinh o sinh⁻¹", "arcsinh("),
                ("arccosh\narccosh o cosh⁻¹", "arccosh("),
                ("arctanh\narctanh o tanh⁻¹", "arctanh(")
            ],
            "Funciones adicionales": [
                ("sec\nsec (secante)", "sec("),
                ("csc\ncsc (cosecante)", "csc("),
                ("cot\ncot (cotangente)", "cot("),
                ("exp\nexp (exponencial)", "exp("),
                ("ln\nln (logaritmo natural)", "ln("),
                ("log\nlog (logaritmo base 10)", "log10("),
                ("|x|\n|x| (valor absoluto)", "abs(")
            ],
            "Potencias y raíces": [
                ("x²\nx^2", "x^2"),
                ("xʸ\nx^y", "x^"),
                ("√x\nsqrt(x)", "sqrt("),
                ("√ʸx\nx^(1/y)", "x^(1/")
            ],
            "Números": [
                ("1", "1"),
                ("2", "2"),
                ("3", "3"),
                ("4", "4"),
                ("5", "5"),
                ("6", "6"),
                ("7", "7"),
                ("8", "8"),
                ("9", "9"),
                ("0", "0")
            ],
            "Variables": [
                ("x", "x"),
                ("y", "y")
            ]
        }

        # Crear secciones y botones de manera organizada
        for section, buttons in sections.items():
            # Sección
            section_frame = tk.LabelFrame(self.inner_frame, text=section, bg="#2E2E2E", fg="white", font=("Segoe UI", 12, "bold"), bd=2, relief=tk.GROOVE)
            section_frame.pack(padx=10, pady=5, fill=tk.X)

            # Determinar el número de columnas
            columns = 4
            for i, (btn_text, insert_text) in enumerate(buttons):
                row = i // columns
                col = i % columns
                btn = ttk.Button(section_frame, text=btn_text, command=lambda txt=insert_text: self.insert_text(txt), width=15)
                btn.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')

            # Configurar el grid para expandirse
            for i in range(columns):
                section_frame.columnconfigure(i, weight=1)

        # Botón para "Importar más operaciones"
        import_btn = ttk.Button(self.inner_frame, text="Importar más operaciones", command=self.import_operations)
        import_btn.pack(pady=10, padx=20, fill=tk.X)

        # Bind para el scroll con el mouse wheel
        self.bind_mouse_wheel()

    def on_frame_configure(self, event):
        # Ajustar el scrollregion del canvas
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def bind_mouse_wheel(self):
        system = platform.system()
        if system == 'Windows':
            self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        elif system == 'Darwin':  # macOS
            self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
            self.canvas.bind_all("<Button-4>", self.on_mousewheel)
            self.canvas.bind_all("<Button-5>", self.on_mousewheel)
        else:  # Linux or other
            self.canvas.bind_all("<Button-4>", self.on_mousewheel)
            self.canvas.bind_all("<Button-5>", self.on_mousewheel)

    def on_mousewheel(self, event):
        system = platform.system()
        if system == 'Windows':
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        elif system == 'Darwin':  # macOS
            if event.delta:
                self.canvas.yview_scroll(int(-1*(event.delta)), "units")
            elif event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")
        else:  # Linux or other
            if event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")

    def start_move(self, event):
        self.offset_x = event.x
        self.offset_y = event.y

    def stop_move(self, event):
        self.offset_x = 0
        self.offset_y = 0

    def do_move(self, event):
        x = self.window.winfo_pointerx() - self.offset_x
        y = self.window.winfo_pointery() - self.offset_y
        self.window.geometry(f'+{x}+{y}')

    def insert_text(self, text):
        if self.app.current_entry:
            current_text = self.app.current_entry.get()
            cursor_position = self.app.current_entry.index(tk.INSERT)
            new_text = current_text[:cursor_position] + text + current_text[cursor_position:]
            self.app.current_entry.delete(0, tk.END)
            self.app.current_entry.insert(0, new_text)
            self.app.current_entry.icursor(cursor_position + len(text))

    def import_operations(self):
        # Placeholder para la funcionalidad de importar más operaciones
        messagebox.showinfo("Importar", "Funcionalidad de importar más operaciones aún no implementada.")

class RootFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Root Finder - Windows 11 Inspired")
        self.root.geometry("1300x800")
        self.root.configure(bg="#2E2E2E")
        
        # Contadores para numerar las pestañas
        self.method_counters = {"Falsa Posición": 0, "Secante": 0}
        
        # Diccionario para almacenar pestañas fijadas
        self.pinned_tabs = {}
        
        # Variable para rastrear la entrada actualmente enfocada
        self.current_entry = None
        
        # Estilos
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TButton",
                             background="#3C3C3C",
                             foreground="white",
                             font=("Segoe UI", 12))  # Aumentar el tamaño de fuente
        self.style.map("TButton",
                       background=[('active', '#505050')])
        self.style.configure("Custom.TNotebook.Tab",
                             background="#3C3C3C",
                             foreground="white",
                             font=("Segoe UI", 10),
                             padding=[10, 5])
        self.style.map("Custom.TNotebook.Tab",
                       background=[('selected', '#505050')],
                       foreground=[('selected', 'white')])
        
        # Panel izquierdo
        self.side_panel = tk.Frame(self.root, bg="#1E1E1E", width=250)
        self.side_panel.pack(side=tk.LEFT, fill=tk.Y)
        
        # Marco para Operaciones y Funciones
        self.operations_functions_frame = tk.Frame(self.side_panel, bg="#1E1E1E")
        self.operations_functions_frame.pack(fill=tk.BOTH, expand=True)
        
        # Botón para mostrar/ocultar Operaciones
        self.op_button = ttk.Button(self.operations_functions_frame, text="Operaciones ▼", command=self.toggle_operations)
        self.op_button.pack(pady=(10, 0), padx=15, fill=tk.X)
        
        self.operations_frame = tk.Frame(self.operations_functions_frame, bg="#1E1E1E")
        self.operations = ["Falsa Posición", "Secante"]
        for op in self.operations:
            btn = ttk.Button(self.operations_frame, text=op, command=lambda op=op: self.add_tab(op))
            btn.pack(pady=5, padx=20, fill=tk.X)
        
        # Separador entre Operaciones y Funciones
        self.separator = ttk.Separator(self.operations_functions_frame, orient='horizontal')
        
        # Botón para mostrar/ocultar Funciones
        self.show_funciones_btn = ttk.Button(self.operations_functions_frame, text="Funciones ▼", command=self.toggle_funciones)
        
        self.funciones_frame = tk.Frame(self.operations_functions_frame, bg="#1E1E1E")
        self.aleatorio_btn = ttk.Button(
            self.funciones_frame,
            text="Ejercicio Aleatorio",
            command=self.generate_random_exercise,
            width=25
        )
        self.aleatorio_btn.pack(pady=5, padx=20, fill=tk.X)
        
        # Botón "Símbolos"
        self.simbolos_btn = ttk.Button(
            self.funciones_frame,
            text="Símbolos",
            command=self.open_virtual_keyboard,
            width=25
        )
        self.simbolos_btn.pack(pady=5, padx=20, fill=tk.X)
        
        # Iniciar sin mostrar los frames
        self.operations_frame.pack_forget()
        self.separator.pack_forget()
        self.show_funciones_btn.pack_forget()
        self.funciones_frame.pack_forget()
        
        # Área principal con Notebook
        self.notebook = ttk.Notebook(self.root, style="Custom.TNotebook")
        self.notebook.pack(expand=True, fill='both')
        
        # Añadir pestaña de '+' para añadir nuevas pestañas
        self.add_plus_tab()
        
        # Bind para manejar clicks en las pestañas
        self.notebook.bind('<Button-1>', self.on_tab_click)
        self.notebook.bind('<Button-3>', self.on_tab_right_click)  # Clic derecho

    def toggle_operations(self):
        if self.operations_frame.winfo_ismapped():
            self.operations_frame.pack_forget()
            self.separator.pack_forget()
            self.show_funciones_btn.pack_forget()
            self.funciones_frame.pack_forget()
            self.op_button.config(text="Operaciones ▼")
        else:
            self.operations_frame.pack(pady=5, padx=10, fill=tk.X)
            self.separator.pack(fill=tk.X, pady=5)
            self.show_funciones_btn.pack(pady=5, padx=15, fill=tk.X)
            self.op_button.config(text="Operaciones ▲")
            self.show_funciones_btn.config(text="Funciones ▼")

    def toggle_funciones(self):
        if self.funciones_frame.winfo_ismapped():
            self.funciones_frame.pack_forget()
            self.show_funciones_btn.config(text="Funciones ▼")
        else:
            self.funciones_frame.pack(pady=5, padx=10, fill=tk.X)
            self.show_funciones_btn.config(text="Funciones ▲")

    def add_plus_tab(self):
        # Crear una pestaña vacía con el símbolo '+'
        self.notebook.add(tk.Frame(self.notebook), text='+')
        self.notebook.select(len(self.notebook.tabs()) -1)

    def add_tab(self, method):
        # Incrementar contador del método
        self.method_counters[method] += 1
        count = self.method_counters[method]
        tab_title = f"{method} {count}"
        
        # Crear nuevo frame para la pestaña
        frame = ttk.Frame(self.notebook)
        self.notebook.insert(len(self.notebook.tabs()) -1, frame, text=tab_title)
        self.notebook.select(len(self.notebook.tabs()) -2)
        
        # Añadir contenido a la pestaña
        OperationTab(frame, method, self)

    def on_tab_click(self, event):
        # Identificar qué pestaña fue clickeada
        x, y = event.x, event.y
        elem = self.notebook.identify(x, y)
        if "label" in elem:
            index = self.notebook.index("@%d,%d" % (x, y))
            tab_text = self.notebook.tab(index, "text")
            if tab_text == '+':
                # Abrir menú para seleccionar método
                self.open_method_menu(event)
            else:
                pass  # Para otros casos, no hacer nada en este momento

    def on_tab_right_click(self, event):
        # Identificar qué pestaña fue clickeada con el botón derecho
        x, y = event.x, event.y
        elem = self.notebook.identify(x, y)
        if "label" in elem:
            index = self.notebook.index("@%d,%d" % (x, y))
            tab_text = self.notebook.tab(index, "text")
            if tab_text != '+':
                # Mostrar menú contextual
                self.show_tab_menu(event, index, tab_text)

    def show_tab_menu(self, event, index, tab_text):
        # Crear un menú contextual para la pestaña
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Cerrar", command=lambda idx=index: self.close_tab(idx))
        menu.add_command(label="Cambiar Nombre", command=lambda idx=index: self.rename_tab(idx))
        if f"{tab_text} 📌" in self.pinned_tabs:
            menu.add_command(label="Desfijar", command=lambda idx=index: self.unpin_tab(idx))
        else:
            menu.add_command(label="Fijar", command=lambda idx=index: self.pin_tab(idx))
        menu.post(event.x_root, event.y_root)

    def close_tab(self, index):
        tab_text = self.notebook.tab(index, "text")
        if f"{tab_text} 📌" in self.pinned_tabs:
            messagebox.showinfo("Información", "Esta pestaña está fijada y no puede ser cerrada.")
            return
        self.notebook.forget(index)

    def rename_tab(self, index):
        current_title = self.notebook.tab(index, "text")
        if current_title.endswith(" 📌"):
            current_title = current_title[:-2]
        new_title = simpledialog.askstring("Cambiar Nombre", "Ingrese el nuevo nombre para la pestaña:", initialvalue=current_title)
        if new_title:
            if current_title in self.pinned_tabs:
                del self.pinned_tabs[current_title]
                self.pinned_tabs[new_title] = True
                new_title += " 📌"
            self.notebook.tab(index, text=new_title)

    def pin_tab(self, index):
        tab_text = self.notebook.tab(index, "text")
        new_title = f"{tab_text} 📌"
        self.notebook.tab(index, text=new_title)
        self.pinned_tabs[new_title] = True

    def unpin_tab(self, index):
        tab_text = self.notebook.tab(index, "text")
        if tab_text in self.pinned_tabs:
            new_title = tab_text.replace(" 📌", "")
            self.notebook.tab(index, text=new_title)
            del self.pinned_tabs[tab_text]

    def open_method_menu(self, event):
        # Crear un menú contextual para seleccionar el método
        menu = tk.Menu(self.root, tearoff=0)
        for method in self.operations:
            menu.add_command(label=method, command=lambda m=method: self.add_tab(m))
        menu.post(event.x_root, event.y_root)

    def generate_random_exercise(self):
        # Generar una función aleatoria
        functions = [
            "x^3 - 4x + 1",
            "sin x - x/2",
            "exp x - 3x",
            "x^2 - 5",
            "cos x - x",
            "x^4 - 2x^2 + 1",
            "x^5 - x - 1"
        ]
        func = random.choice(functions)
        
        # Crear una ventana para seleccionar el método de manera más compacta
        select_window = tk.Toplevel(self.root)
        select_window.title("Ejercicio Aleatorio")
        select_window.geometry("350x200")  # Aumentar ligeramente el tamaño para mejor legibilidad
        select_window.resizable(False, False)
        select_window.grab_set()
        
        # Centrar la ventana sobre la ventana principal
        self.center_window(select_window, 350, 200)
        
        # Información de la función seleccionada
        func_label = tk.Label(select_window, text="Función seleccionada:", font=("Segoe UI", 12, "bold"))
        func_label.pack(pady=(15, 5))
        
        func_display = tk.Label(select_window, text=func, font=("Segoe UI", 12), wraplength=320, justify='center')
        func_display.pack(pady=(0, 15))
        
        # Selección del método
        method_frame = tk.Frame(select_window)
        method_frame.pack(pady=5)
        
        selected_method = tk.StringVar(value="Falsa Posición")
        
        rb1 = ttk.Radiobutton(method_frame, text="Falsa Posición", variable=selected_method, value="Falsa Posición")
        rb1.pack(side=tk.LEFT, padx=10)
        rb2 = ttk.Radiobutton(method_frame, text="Secante", variable=selected_method, value="Secante")
        rb2.pack(side=tk.LEFT, padx=10)
        
        # Botón de confirmación
        confirm_button = ttk.Button(select_window, text="Aceptar", command=lambda: self.confirm_random_selection(select_window, func, selected_method.get()))
        confirm_button.pack(pady=20)

    def confirm_random_selection(self, window, func, method):
        if method == "Falsa Posición":
            # Intentar encontrar un intervalo adecuado múltiples veces
            a, b = self.find_bracket(func, attempts=50)  # Aumentar los intentos
            if a is None:
                messagebox.showerror("Error", "No se pudo encontrar un intervalo adecuado para Falsa Posición.")
                window.destroy()
                return
            tol = 1e-5
            max_iter = 100
            self.add_tab_with_params(method, func, a, b, tol, max_iter)
        else:
            # Intentar encontrar puntos iniciales adecuados múltiples veces
            x0, x1 = self.find_initial_points(func, attempts=50)  # Aumentar los intentos
            if x0 is None or x1 is None:
                messagebox.showerror("Error", "No se pudo encontrar puntos iniciales adecuados para Secante.")
                window.destroy()
                return
            tol = 1e-5
            max_iter = 100
            self.add_tab_with_params(method, func, x0, x1, tol, max_iter)
        window.destroy()

    def center_window(self, window, width, height):
        # Obtener las dimensiones de la pantalla
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        # Calcular la posición para centrar la ventana
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        window.geometry(f'{width}x{height}+{x}+{y}')

    def find_bracket(self, func, attempts=50):
        # Buscar un intervalo [a, b] donde f(a)*f(b) < 0
        for _ in range(attempts):
            a = random.uniform(-10, 10)
            b = random.uniform(-10, 10)
            if a == b:
                continue
            try:
                fa = safe_eval(func, a)
                fb = safe_eval(func, b)
                if fa * fb < 0:
                    return a, b
            except:
                continue
        return None, None

    def find_initial_points(self, func, attempts=50):
        # Buscar dos puntos donde f(x0) y f(x1) no sean iguales
        for _ in range(attempts):
            x0 = random.uniform(-10, 10)
            x1 = random.uniform(-10, 10)
            if x0 == x1:
                continue
            try:
                f0 = safe_eval(func, x0)
                f1 = safe_eval(func, x1)
                if f0 != f1:
                    return x0, x1
            except:
                continue
        return None, None

    def add_tab_with_params(self, method, func, param1, param2, tol, max_iter):
        # Incrementar contador del método
        self.method_counters[method] += 1
        count = self.method_counters[method]
        tab_title = f"{method} {count}"
        
        # Crear nuevo frame para la pestaña
        frame = ttk.Frame(self.notebook)
        self.notebook.insert(len(self.notebook.tabs()) -1, frame, text=tab_title)
        self.notebook.select(len(self.notebook.tabs()) -2)
        
        # Añadir contenido a la pestaña
        operation_tab = OperationTab(frame, method, self)
        operation_tab.set_parameters(func, param1, param2, tol, max_iter)

    def open_virtual_keyboard(self):
        if hasattr(self, 'virtual_keyboard') and self.virtual_keyboard.window.winfo_exists():
            # Si ya está abierta, simplemente enfocarla
            self.virtual_keyboard.window.lift()
        else:
            self.virtual_keyboard = VirtualKeyboard(self)

class OperationTab:
    def __init__(self, parent, method, app):
        self.parent = parent
        self.method = method
        self.app = app
        
        # Encabezado
        header = tk.Frame(self.parent, bg="#3C3C3C")
        header.pack(fill=tk.X, pady=10, padx=10)
        
        title = tk.Label(header, text=method, bg="#3C3C3C", fg="white", font=("Segoe UI", 14, "bold"))
        title.pack(side=tk.LEFT, padx=5)
        
        add_btn = ttk.Button(header, text="+", width=3, command=self.add_new_tab)
        add_btn.pack(side=tk.RIGHT, padx=2)
        
        close_btn = ttk.Button(header, text="x", width=3, command=self.close_tab)
        close_btn.pack(side=tk.RIGHT, padx=2)
        
        # Contenedor de entradas
        container = tk.Frame(self.parent, bg="#2E2E2E")
        container.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Función
        tk.Label(container, text="f(x) =", bg="#2E2E2E", fg="white", font=("Segoe UI", 10)).grid(row=0, column=0, sticky='e', pady=5)
        self.func_entry = ttk.Entry(container, width=40)
        self.func_entry.grid(row=0, column=1, pady=5, sticky='w')
        self.func_entry.bind("<FocusIn>", self.on_focus_in)
        
        if method == "Falsa Posición":
            # a
            tk.Label(container, text="a =", bg="#2E2E2E", fg="white", font=("Segoe UI", 10)).grid(row=1, column=0, sticky='e', pady=5)
            self.a_entry = ttk.Entry(container, width=40)
            self.a_entry.grid(row=1, column=1, pady=5, sticky='w')
            self.a_entry.bind("<FocusIn>", self.on_focus_in)
            # b
            tk.Label(container, text="b =", bg="#2E2E2E", fg="white", font=("Segoe UI", 10)).grid(row=2, column=0, sticky='e', pady=5)
            self.b_entry = ttk.Entry(container, width=40)
            self.b_entry.grid(row=2, column=1, pady=5, sticky='w')
            self.b_entry.bind("<FocusIn>", self.on_focus_in)
        elif method == "Secante":
            # x0
            tk.Label(container, text="x₀ =", bg="#2E2E2E", fg="white", font=("Segoe UI", 10)).grid(row=1, column=0, sticky='e', pady=5)
            self.x0_entry = ttk.Entry(container, width=40)
            self.x0_entry.grid(row=1, column=1, pady=5, sticky='w')
            self.x0_entry.bind("<FocusIn>", self.on_focus_in)
            # x1
            tk.Label(container, text="x₁ =", bg="#2E2E2E", fg="white", font=("Segoe UI", 10)).grid(row=2, column=0, sticky='e', pady=5)
            self.x1_entry = ttk.Entry(container, width=40)
            self.x1_entry.grid(row=2, column=1, pady=5, sticky='w')
            self.x1_entry.bind("<FocusIn>", self.on_focus_in)
        
        # Tolerancia
        tk.Label(container, text="Tolerancia =", bg="#2E2E2E", fg="white", font=("Segoe UI", 10)).grid(row=3, column=0, sticky='e', pady=5)
        self.tol_entry = ttk.Entry(container, width=40)
        self.tol_entry.grid(row=3, column=1, pady=5, sticky='w')
        self.tol_entry.bind("<FocusIn>", self.on_focus_in)
        
        # Iteraciones
        tk.Label(container, text="Máx. Iteraciones =", bg="#2E2E2E", fg="white", font=("Segoe UI", 10)).grid(row=4, column=0, sticky='e', pady=5)
        self.iter_entry = ttk.Entry(container, width=40)
        self.iter_entry.grid(row=4, column=1, pady=5, sticky='w')
        self.iter_entry.bind("<FocusIn>", self.on_focus_in)
        
        # Botón de cálculo
        calc_button = ttk.Button(container, text="Calcular", command=self.calculate)
        calc_button.grid(row=5, column=0, columnspan=2, pady=15)
        
        # Ajustar las columnas para que se expandan
        container.columnconfigure(1, weight=1)

    def on_focus_in(self, event):
        self.app.current_entry = event.widget

    def set_parameters(self, func, param1, param2, tol, max_iter):
        self.func_entry.insert(0, func)
        if self.method == "Falsa Posición":
            self.a_entry.insert(0, str(param1))
            self.b_entry.insert(0, str(param2))
        elif self.method == "Secante":
            self.x0_entry.insert(0, str(param1))
            self.x1_entry.insert(0, str(param2))
        self.tol_entry.insert(0, str(tol))
        self.iter_entry.insert(0, str(max_iter))

    def calculate(self):
        try:
            func = self.func_entry.get()
            tol = float(self.tol_entry.get())
            max_iter = int(self.iter_entry.get())

            if self.method == "Falsa Posición":
                a = float(self.a_entry.get())
                b = float(self.b_entry.get())
                root, iterations, iterations_data = falsa_posicion(func, a, b, tol, max_iter)
                self.open_result_tab(f"Raíz: {root:.6f} en {iterations} iteraciones.", func, root, iterations_data)
            elif self.method == "Secante":
                x0 = float(self.x0_entry.get())
                x1 = float(self.x1_entry.get())
                root, iterations, iterations_data = secante(func, x0, x1, tol, max_iter)
                self.open_result_tab(f"Raíz: {root:.6f} en {iterations} iteraciones.", func, root, iterations_data)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def open_result_tab(self, result_text, func, root, iterations_data):
        result_tab_title = f"Resultado {self.app.method_counters[self.method]}"
        frame = ttk.Frame(self.app.notebook)
        self.app.notebook.add(frame, text=result_tab_title)
        self.app.notebook.select(len(self.app.notebook.tabs()) -1)
        
        # Crear un frame para el texto y la gráfica
        result_container = tk.Frame(frame, bg="#2E2E2E")
        result_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Texto del resultado
        result_label = tk.Label(result_container, text=result_text, bg="#2E2E2E", fg="lightgreen", font=("Segoe UI", 12))
        result_label.pack(pady=10)
        
        # Generar la gráfica
        try:
            # Definir el rango para la gráfica
            self.x_min, self.x_max = -10, 10  # Valores iniciales
            self.func = func
            self.root_value = root
            self.plot_graph(result_container)
        except Exception as e:
            tk.Label(result_container, text=f"Error al generar la gráfica: {e}", bg="#2E2E2E", fg="red", font=("Segoe UI", 10)).pack()

        # Frame para los botones debajo de la gráfica
        buttons_frame = tk.Frame(result_container, bg="#2E2E2E")
        buttons_frame.pack(pady=10)

        # Botón de iteraciones
        iterations_button = ttk.Button(buttons_frame, text="Iteraciones", command=self.toggle_iterations)
        iterations_button.pack(side=tk.LEFT, padx=5)

        # Botón de parámetros
        parameters_button = ttk.Button(buttons_frame, text="Parámetros", command=self.edit_parameters)
        parameters_button.pack(side=tk.LEFT, padx=5)

        # Frame para las iteraciones (inicialmente oculto)
        self.iterations_frame = tk.Frame(result_container, bg="#2E2E2E")
        self.iterations_data = iterations_data

    def plot_graph(self, parent_frame):
        # Si ya existe una gráfica, destruirla
        if hasattr(self, 'canvas'):
            self.canvas.get_tk_widget().destroy()

        x = [self.x_min + i*(self.x_max - self.x_min)/(400 - 1) for i in range(400)]
        y = []
        for val in x:
            try:
                y_val = safe_eval(self.func, val)
                y.append(y_val)
            except:
                y.append(float('nan'))  # Para evitar errores en la gráfica

        fig, ax = plt.subplots(figsize=(5,4), dpi=100)
        ax.plot(x, y, label='f(x)')
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(self.root_value, color='red', linestyle='--', label=f'Raíz ≈ {self.root_value:.4f}')
        ax.scatter(self.root_value, 0, color='red')
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.set_title('Gráfica de la Función y la Raíz Encontrada')
        ax.legend()
        ax.grid(True)

        # Embeber la gráfica en Tkinter
        self.canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=10)

    def toggle_iterations(self):
        if self.iterations_frame.winfo_ismapped():
            self.iterations_frame.pack_forget()
        else:
            self.show_iterations()

    def show_iterations(self):
        # Limpiar el frame
        for widget in self.iterations_frame.winfo_children():
            widget.destroy()

        # Crear un Treeview para mostrar los datos
        tree = ttk.Treeview(self.iterations_frame, show='headings')

        # Definir columnas basadas en el método
        if self.method == "Falsa Posición":
            columns = ('Iteración', 'a', 'b', 'c', 'f(a)', 'f(b)', 'f(c)')
        elif self.method == "Secante":
            columns = ('Iteración', 'x0', 'x1', 'x2', 'f(x0)', 'f(x1)', 'f(x2)')

        tree['columns'] = columns

        # Definir encabezados
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor='center', width=100)

        # Insertar datos
        for data in self.iterations_data:
            values = tuple(round(data[col], 6) if isinstance(data[col], float) else data[col] for col in columns)
            tree.insert('', 'end', values=values)

        # Agregar scrollbar
        scrollbar = ttk.Scrollbar(self.iterations_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)

        self.iterations_frame.pack(fill=tk.BOTH, expand=True)

    def edit_parameters(self):
        # Ventana para editar parámetros de la gráfica
        param_window = tk.Toplevel(self.parent)
        param_window.title("Editar Parámetros de la Gráfica")
        param_window.geometry("300x200")
        param_window.resizable(False, False)
        param_window.grab_set()

        tk.Label(param_window, text="Rango de x mínimo:").pack(pady=5)
        x_min_entry = ttk.Entry(param_window)
        x_min_entry.pack(pady=5)
        x_min_entry.insert(0, str(self.x_min))

        tk.Label(param_window, text="Rango de x máximo:").pack(pady=5)
        x_max_entry = ttk.Entry(param_window)
        x_max_entry.pack(pady=5)
        x_max_entry.insert(0, str(self.x_max))

        def update_graph():
            try:
                self.x_min = float(x_min_entry.get())
                self.x_max = float(x_max_entry.get())
                if self.x_min >= self.x_max:
                    raise ValueError("x mínimo debe ser menor que x máximo.")
                self.plot_graph(self.canvas.get_tk_widget().master)
                param_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(param_window, text="Actualizar", command=update_graph).pack(pady=10)

    def add_new_tab(self):
        # Añadir una nueva pestaña del mismo método
        self.app.add_tab(self.method)

    def close_tab(self):
        # Cerrar la pestaña actual
        notebook = self.parent.master
        current_tab = notebook.select()
        tab_text = notebook.tab(current_tab, "text")
        if f"{tab_text} 📌" in self.app.pinned_tabs:
            messagebox.showinfo("Información", "Esta pestaña está fijada y no puede ser cerrada.")
            return
        notebook.forget(current_tab)

def main():
    root = tk.Tk()
    app = RootFinderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
