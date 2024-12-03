# SpeechCalculator.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import speech_recognition as sr
import threading
import sys
import ast
import operator
import re

class SpeechWindow:
    def __init__(self, master, parent):
        self.master = master
        self.parent = parent
        self.master.title("🎤 Entrada por Voz - Algebrify")
        self.master.geometry("600x500")
        self.master.configure(bg="#3b3b3b")  # Fondo grisáceo
        self.master.resizable(True, True)

        # Variable para controlar el modo de pantalla completa
        self.fullscreen = False

        # Estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton',
                             font=('Helvetica', 14),
                             padding=10,
                             foreground="#ffffff",
                             background='#6c6c6c')  # Botones grisáceos
        self.style.map('TButton',
                       background=[('active', '#5a5a5a')])

        # Configurar la interfaz de usuario
        self.setup_ui()

        # Inicializar el reconocedor
        self.recognizer = sr.Recognizer()

    def setup_ui(self):
        # Título
        title_label = tk.Label(self.master, text="🎤 Entrada por Voz", font=("Helvetica", 20, "bold"), fg="#ffffff",
                               bg="#3b3b3b")
        title_label.pack(pady=10)

        # Frame para selección de dispositivos
        devices_frame = tk.Frame(self.master, bg="#3b3b3b")
        devices_frame.pack(pady=10)

        # Selección de micrófono
        mic_label = tk.Label(devices_frame, text="Selecciona el Micrófono:", font=("Helvetica", 12), fg="#ffffff",
                             bg="#3b3b3b")
        mic_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')

        self.mic_var = tk.StringVar()
        self.mic_dropdown = ttk.Combobox(devices_frame, textvariable=self.mic_var, state="readonly", width=40)
        self.mic_dropdown.grid(row=0, column=1, padx=5, pady=5)
        self.populate_microphones()

        # Botón para alternar pantalla completa
        fullscreen_button = ttk.Button(self.master, text="🔲 Pantalla Completa", command=self.toggle_fullscreen)
        fullscreen_button.pack(pady=10)

        # Botón para iniciar el reconocimiento
        self.record_button = ttk.Button(self.master, text="🎙️ Grabar", command=self.start_recording_thread)
        self.record_button.pack(pady=10)

        # Área para mostrar y editar el texto reconocido
        self.result_text = tk.Text(self.master, height=8, width=60, font=("Helvetica", 12), bg="#e0e0e0", fg="#000000")
        self.result_text.pack(pady=10)
        self.result_text.configure(state='normal')

        # Frame para botones adicionales
        action_frame = tk.Frame(self.master, bg="#3b3b3b")
        action_frame.pack(pady=10)

        # Botón para procesar la ecuación
        self.process_button = ttk.Button(action_frame, text="🔄 Resolver Operación", command=self.process_equation_thread)
        self.process_button.grid(row=0, column=0, padx=5, pady=5)

        # Botón para guardar el texto
        save_button = ttk.Button(action_frame, text="💾 Guardar Texto", command=self.save_text)
        save_button.grid(row=0, column=1, padx=5, pady=5)

        # Botón para limpiar el texto
        clear_button = ttk.Button(action_frame, text="🗑️ Limpiar Texto", command=self.clear_text)
        clear_button.grid(row=0, column=2, padx=5, pady=5)

        # Botón para cerrar
        close_button = ttk.Button(self.master, text="🔙 Volver", command=self.master.destroy)
        close_button.pack(pady=10)

    def populate_microphones(self):
        """
        Lista todos los micrófonos disponibles y los añade al combobox.
        """
        mic_list = sr.Microphone.list_microphone_names()
        if not mic_list:
            messagebox.showerror("Error", "No se encontraron micrófonos en el sistema.")
            self.record_button.config(state='disabled')
            return
        self.mic_dropdown['values'] = mic_list
        # Seleccionar el micrófono predeterminado
        default_mic = sr.Microphone.list_microphone_names()[0]
        self.mic_var.set(default_mic)

    def toggle_fullscreen(self):
        """
        Alterna el modo de pantalla completa.
        """
        self.fullscreen = not self.fullscreen
        self.master.attributes("-fullscreen", self.fullscreen)
        if self.fullscreen:
            self.master.geometry("")
        else:
            self.master.geometry("600x500")

    def start_recording_thread(self):
        """
        Inicia un hilo para la grabación de audio y el reconocimiento de voz.
        """
        threading.Thread(target=self.start_recording, daemon=True).start()

    def start_recording(self):
        """
        Inicia la grabación de audio y el reconocimiento de voz.
        """
        selected_mic = self.mic_var.get()
        if not selected_mic:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un micrófono.")
            return

        mic_index = sr.Microphone.list_microphone_names().index(selected_mic)
        self.record_button.config(state='disabled')
        self.process_button.config(state='disabled')
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Escuchando...")
        try:
            with sr.Microphone(device_index=mic_index) as source:
                self.recognizer.adjust_for_ambient_noise(source)
                # Notificar al usuario que hable
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, "Por favor, habla ahora...")
                audio = self.recognizer.listen(source, timeout=5)
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, "Procesando tu voz...")
            text = self.recognizer.recognize_google(audio, language='es-ES')
            self.display_result(text)
        except sr.WaitTimeoutError:
            messagebox.showerror("Error", "No se detectó voz. Intenta nuevamente.")
            self.result_text.delete(1.0, tk.END)
        except sr.UnknownValueError:
            messagebox.showerror("Error", "No se pudo entender el audio. Intenta nuevamente.")
            self.result_text.delete(1.0, tk.END)
        except sr.RequestError as e:
            messagebox.showerror("Error", f"Error con el servicio de reconocimiento de voz: {e}")
            self.result_text.delete(1.0, tk.END)
        finally:
            self.record_button.config(state='normal')
            self.process_button.config(state='normal')

    def display_result(self, text):
        """
        Muestra el texto reconocido en el área de texto.
        """
        self.result_text.configure(state='normal')
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, text)

    def process_equation_thread(self):
        """
        Inicia un hilo para procesar la ecuación.
        """
        threading.Thread(target=self.process_equation, daemon=True).start()

    def process_equation(self):
        """
        Procesa la ecuación reconocida y muestra el resultado.
        """
        equation = self.result_text.get(1.0, tk.END).strip()
        if not equation:
            messagebox.showwarning("Advertencia", "No hay una operación para procesar.")
            return

        try:
            # Convertir palabras a operadores matemáticos
            parsed_equation = self.parse_equation(equation)
            # Mostrar la ecuación parseada para depuración
            print(f"Ecuación parseada: {parsed_equation}")
            result = self.safe_eval(parsed_equation)
            messagebox.showinfo("Resultado", f"El resultado es: {result}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo procesar la operación.\n{e}")

    def parse_equation(self, equation):
        """
        Convierte las palabras comunes en operadores matemáticos.
        """
        replacements = {
            # Operadores
            'más': '+',
            'mas': '+',
            'menos': '-',
            'por': '*',
            'multiplicado por': '*',
            'entre': '/',
            'dividido por': '/',
            'dividido entre': '/',
            'suma': '+',
            'resta': '-',
            'multiplicación': '*',
            'división': '/',
            'al cuadrado': '**2',
            'al cubo': '**3',
            'elevado a la': '**',
            'elevado a': '**',
            # Números
            'cero': '0',
            'uno': '1',
            'dos': '2',
            'tres': '3',
            'cuatro': '4',
            'cinco': '5',
            'seis': '6',
            'siete': '7',
            'ocho': '8',
            'nueve': '9',
            'diez': '10',
            'once': '11',
            'doce': '12',
            'trece': '13',
            'catorce': '14',
            'quince': '15',
            'dieciséis': '16',
            'diecisiete': '17',
            'dieciocho': '18',
            'diecinueve': '19',
            'veinte': '20',
            # Paréntesis
            'abrir paréntesis': '(',
            'cerrar paréntesis': ')',
            '(': '(',
            ')': ')'
        }
        # Reemplazar palabras por operadores
        equation = equation.lower()
        # Reemplazos de frases largas primero
        for word, symbol in replacements.items():
            equation = re.sub(r'\b' + re.escape(word) + r'\b', symbol, equation)
        # Eliminar palabras desconocidas y espacios extra
        equation = re.sub(r'[^\d\+\-\*/\^\(\)\.\s]', '', equation)
        equation = ' '.join(equation.split())
        return equation

    def safe_eval(self, expr):
        """
        Evalúa de forma segura una expresión matemática.
        """
        # Definir operadores permitidos
        allowed_operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.USub: operator.neg
        }

        def eval_node(node):
            if isinstance(node, ast.Num):  # Números
                return node.n
            elif isinstance(node, ast.BinOp):  # Operaciones binarias
                op_type = type(node.op)
                if op_type in allowed_operators:
                    return allowed_operators[op_type](eval_node(node.left), eval_node(node.right))
                else:
                    raise ValueError('Operador no permitido')
            elif isinstance(node, ast.UnaryOp):  # Operaciones unarias
                op_type = type(node.op)
                if op_type in allowed_operators:
                    return allowed_operators[op_type](eval_node(node.operand))
                else:
                    raise ValueError('Operador no permitido')
            else:
                raise ValueError('Expresión no permitida')

        node = ast.parse(expr, mode='eval').body
        return eval_node(node)

    def save_text(self):
        """
        Guarda el texto reconocido en un archivo.
        """
        text = self.result_text.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("Advertencia", "No hay texto para guardar.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")])
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                messagebox.showinfo("Guardar", f"El texto se guardó en {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo.\n{e}")

    def clear_text(self):
        """
        Limpia el área de texto.
        """
        self.result_text.delete(1.0, tk.END)

# Para ejecutar la ventana de prueba
if __name__ == "__main__":
    root = tk.Tk()
    app = SpeechWindow(root, None)
    root.mainloop()
