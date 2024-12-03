import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser
from sympy import symbols, Eq, solve, sympify
from sympy.parsing.sympy_parser import parse_expr
from scipy.optimize import root, bisect, newton
import numpy as np
import openai
import json
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Configurar la clave API de OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Depuración: Verificar si la clave API está cargada
if openai.api_key:
    print("Clave API cargada correctamente.")
else:
    print("No se pudo cargar la clave API.")

class EjerciciosApp:
    def __init__(self, master):
        self.master = master
        master.title("Ejercicios - Algebrify")
        master.geometry("1200x800")
        master.configure(bg="#2E2E2E")  # Fondo gris oscuro
        master.attributes("-fullscreen", False)
        master.resizable(True, True)

        # Estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Usar tema 'clam' para mayor flexibilidad

        # Configuración de botones
        self.style.configure('TButton',
                             font=('Helvetica Neue', 14, 'bold'),
                             padding=10,
                             foreground='#FFFFFF',
                             background='#4A4A4A',  # Gris medio para botones
                             borderwidth=0,
                             relief='flat')
        self.style.map('TButton',
                       background=[('active', '#6A6A6A')],  # Gris más claro al activar
                       foreground=[('active', '#FFFFFF')])

        # Configuración de etiquetas
        self.style.configure('TLabel',
                             font=('Helvetica Neue', 14),
                             background='#2E2E2E',  # Fondo gris oscuro
                             foreground='#E0E0E0')  # Texto gris claro

        # Configuración de entradas
        self.style.configure('TEntry',
                             font=('Helvetica Neue', 14),
                             padding=10,
                             fieldbackground='#3E3E3E',  # Fondo entrada gris medio
                             foreground='#FFFFFF',
                             insertcolor='#FFFFFF')

        # Configuración de áreas de texto
        self.style.configure('TText',
                             font=('Helvetica Neue', 14),
                             padding=10,
                             background='#3E3E3E',
                             foreground='#FFFFFF',
                             borderwidth=1,
                             relief='solid')

        # Contenedor principal
        self.main_frame = tk.Frame(master, bg="#2E2E2E")
        self.main_frame.pack(expand=True, fill='both', padx=50, pady=50)

        # Título
        self.title_label = ttk.Label(self.main_frame, text="Resolución de Ecuaciones", font=("Helvetica Neue", 24, "bold"))
        self.title_label.pack(pady=(0, 20))

        # Campo de entrada
        self.input_frame = tk.Frame(self.main_frame, bg="#2E2E2E")
        self.input_frame.pack(pady=10, fill='x')

        self.ecuacion_label = ttk.Label(self.input_frame, text="Ingresa la Ecuación:")
        self.ecuacion_label.pack(side='left', padx=(0, 10))

        self.ecuacion_entry = ttk.Entry(self.input_frame, width=80)
        self.ecuacion_entry.pack(side='left', fill='x', expand=True)

        # Botones
        self.button_frame = tk.Frame(self.main_frame, bg="#2E2E2E")
        self.button_frame.pack(pady=20)

        self.resolver_button = ttk.Button(self.button_frame, text="Resolver", command=self.resolver_ecuacion)
        self.resolver_button.grid(row=0, column=0, padx=15, pady=10)

        self.detectar_button = ttk.Button(self.button_frame, text="Detectar", command=self.detectar_metodo)
        self.detectar_button.grid(row=0, column=1, padx=15, pady=10)

        self.guardar_button = ttk.Button(self.button_frame, text="Guardar", command=self.guardar_resultados)
        self.guardar_button.grid(row=0, column=2, padx=15, pady=10)

        # Área de resultados
        self.resultados_label = ttk.Label(self.main_frame, text="Resultados:")
        self.resultados_label.pack(pady=(20, 10))

        self.resultados_text = tk.Text(self.main_frame, height=25, wrap='word', state='disabled',
                                       bg="#3E3E3E", fg="#FFFFFF", insertbackground="#FFFFFF")
        self.resultados_text.pack(fill='both', expand=True)

        # Barra de menú
        self.menu_bar = tk.Menu(master, bg="#2E2E2E", fg="#E0E0E0", activebackground="#4A4A4A", activeforeground="#FFFFFF")
        master.config(menu=self.menu_bar)

        self.view_menu = tk.Menu(self.menu_bar, tearoff=0, bg="#2E2E2E", fg="#E0E0E0",
                                 activebackground="#4A4A4A", activeforeground="#FFFFFF")
        self.menu_bar.add_cascade(label="Vista", menu=self.view_menu)
        self.view_menu.add_command(label="Pantalla Completa", command=self.toggle_fullscreen, accelerator="F11")
        self.view_menu.add_separator()
        self.view_menu.add_command(label="Salir Pantalla Completa", command=self.toggle_fullscreen, accelerator="Esc")

        master.bind("<F11>", self.toggle_fullscreen)
        master.bind("<Escape>", self.toggle_fullscreen)

    def toggle_fullscreen(self, event=None):
        is_fullscreen = self.master.attributes("-fullscreen")
        self.master.attributes("-fullscreen", not is_fullscreen)

    def mostrar_error(self, mensaje):
        messagebox.showerror("Error", mensaje)

    def resolver_ecuacion(self):
        ecuacion_input = self.ecuacion_entry.get()
        if not ecuacion_input.strip():
            self.mostrar_error("Por favor, ingresa una ecuación.")
            return

        try:
            # Parsear la ecuación
            x = symbols('x')
            ecuacion_sympy = parse_expr(ecuacion_input, evaluate=False)
            if isinstance(ecuacion_sympy, Eq):
                ecuacion = ecuacion_sympy
            else:
                ecuacion = Eq(ecuacion_sympy, 0)
        except Exception as e:
            self.mostrar_error(f"Ecuación inválida: {e}")
            return

        # Detectar el tipo de ecuación
        tipo_ecuacion = self.detectar_tipo_ecuacion(ecuacion)

        procedimiento = f"Resolviendo la ecuación: {ecuacion}\n"
        procedimiento += f"Tipo de Ecuación: {tipo_ecuacion}\n\n"

        soluciones = []
        metodo_utilizado = ""

        try:
            if tipo_ecuacion == "Polinomial":
                metodo_utilizado = "Solución simbólica con SymPy"
                procedimiento += f"Usando SymPy para resolver la ecuación polinomial.\n"
                soluciones = solve(ecuacion, x)
                procedimiento += f"Soluciones encontradas: {soluciones}\n"
            elif tipo_ecuacion == "Trascendental":
                metodo_utilizado = "Métodos numéricos con SciPy"
                procedimiento += f"Usando métodos numéricos (Newton-Raphson) para resolver la ecuación trascendental.\n"
                # Definir la función
                f = lambda var: sympify(ecuacion.lhs - ecuacion.rhs).subs(x, var)
                # Definir la derivada
                f_prime = lambda var: sympify(ecuacion.lhs - ecuacion.rhs).diff(x).subs(x, var)

                # Elegir un punto inicial
                x0 = 1.0

                # Usar el método de Newton-Raphson
                resultado = newton(f, x0, fprime=f_prime, tol=1e-5, maxiter=100, full_output=True)

                if resultado.converged:
                    solucion = resultado.root
                    soluciones = [solucion]
                    procedimiento += f"Inicialización: x0 = {x0}\n"
                    procedimiento += f"Iteración 1: x1 = {resultado.iterations[0]}, f(x1) = {f(resultado.iterations[0])}, f'(x1) = {f_prime(resultado.iterations[0])}\n"
                    procedimiento += f"Solución encontrada: x ≈ {solucion}\n"
                else:
                    self.mostrar_error("El método numérico no convergió.")
                    return
            else:
                self.mostrar_error("Tipo de ecuación no soportado.")
                return
        except Exception as e:
            self.mostrar_error(f"Error al resolver la ecuación: {e}")
            return

        # Mostrar los resultados en el área de texto
        self.resultados_text.configure(state='normal')
        self.resultados_text.delete(1.0, tk.END)
        self.resultados_text.insert(tk.END, procedimiento)
        self.resultados_text.configure(state='disabled')

    def detectar_tipo_ecuacion(self, ecuacion):
        # Determinar si la ecuación es polinomial o trascendental
        # Verificar si la ecuación contiene funciones trascendentales comunes
        funciones_trascendentales = ['sin', 'cos', 'tan', 'exp', 'log', 'sqrt']
        ecuacion_str = str(ecuacion).lower()

        for func in funciones_trascendentales:
            if func in ecuacion_str:
                return "Trascendental"
        return "Polinomial"

    def detectar_metodo(self):
        entrada = self.ecuacion_entry.get()
        if not entrada.strip():
            self.mostrar_error("Por favor, ingresa un texto o ecuación.")
            return

        try:
            # Llamar a la API de OpenAI para analizar la entrada
            prompt = (
                f"Analiza el siguiente contenido y determina si es una ecuación matemática. "
                f"Si lo es, recomienda el mejor método para resolverla y proporciona una breve descripción del método recomendado. "
                f"Si no es una ecuación, describe brevemente el contenido.\n\nContenido: {entrada}"
            )
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=200,
                n=1,
                stop=None,
                temperature=0.5,
            )
            analisis = response.choices[0].text.strip()
        except Exception as e:
            self.mostrar_error(f"Error al comunicarse con la API de OpenAI: {e}")
            return

        # Mostrar el análisis en el área de texto
        self.resultados_text.configure(state='normal')
        self.resultados_text.delete(1.0, tk.END)
        self.resultados_text.insert(tk.END, f"Análisis del contenido:\n{analisis}\n")
        self.resultados_text.configure(state='disabled')

        # Determinar si la entrada es una ecuación
        if "ecuación" in analisis.lower():
            # Preguntar al usuario si desea resolverla
            respuesta = messagebox.askyesno("Método Encontrado",
                                           "Método encontrado. ¿Quieres resolver la ecuación?")
            if respuesta:
                self.resolver_ecuacion()
        else:
            messagebox.showinfo("Información", "El contenido ingresado no es una ecuación matemática.")

    def guardar_resultados(self):
        # Obtener el contenido del área de texto
        contenido = self.resultados_text.get(1.0, tk.END).strip()
        if not contenido:
            self.mostrar_error("No hay resultados para guardar.")
            return

        # Solicitar el nombre del archivo al usuario
        nombre_archivo = filedialog.asksaveasfilename(defaultextension=".txt",
                                                     filetypes=[("Archivos de texto", "*.txt")],
                                                     title="Guardar resultados como")
        if not nombre_archivo:
            return  # El usuario canceló la operación

        try:
            with open(nombre_archivo, 'w', encoding='utf-8') as f:
                f.write(contenido)
            messagebox.showinfo("Guardar Resultados", f"Resultados guardados exitosamente en {nombre_archivo}")
        except Exception as e:
            self.mostrar_error(f"No se pudo guardar el archivo: {e}")

def main():
    root = tk.Tk()
    app = EjerciciosApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
