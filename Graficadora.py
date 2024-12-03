# Graficadora.py

import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import numpy as np
import mplcursors  # Para anotaciones interactivas
from matplotlib.widgets import Slider
import math  # Necesario para evaluar funciones matemáticas en bisección

axcolor = 'lightgoldenrodyellow'  # Define el color que desees


def open_graficar_window(parent, exercise):
    """
    Abre una nueva ventana para graficar el ejercicio seleccionado con interactividad mejorada.

    Parámetros:
    - parent: La ventana padre de Tkinter.
    - exercise: Diccionario que contiene los detalles del ejercicio.
    """
    # Agregar depuración
    print(f"Tipo de exercise: {type(exercise)}")
    print(f"Contenido de exercise: {exercise}")

    # Verificar que exercise sea un diccionario
    if not isinstance(exercise, dict):
        messagebox.showerror("Error de Graficación", f"El ejercicio debe ser un diccionario, pero se recibió {type(exercise)}.")
        return

    # Crear una nueva ventana Toplevel
    graficar_window = tk.Toplevel(parent)
    graficar_window.title("Graficar Ejercicio")
    graficar_window.geometry("1000x800")  # Aumentar el tamaño para mayor espacio

    # Crear un Frame para contener el gráfico y los controles
    frame = ttk.Frame(graficar_window)
    frame.pack(fill='both', expand=True, padx=10, pady=10)

    # Crear la figura de matplotlib
    fig, ax = plt.subplots(figsize=(8, 6))
    plt.subplots_adjust(left=0.1, bottom=0.25)  # Ajustar el espacio para controles

    # Dependiendo del tipo de ejercicio, graficar lo correspondiente
    ejercicio_tipo = exercise.get('type', '').lower()
    detalles = exercise.get('details', {})

    try:
        if 'gauss' in ejercicio_tipo:
            graficar_gauss(detalles, ax, fig)
        elif 'escalonada' in ejercicio_tipo:
            graficar_matriz_escalonada(detalles, ax, fig)
        elif 'ecuaciones' in ejercicio_tipo:
            graficar_ecuaciones_matrices(detalles, ax, fig)
        elif 'biseccion' in ejercicio_tipo:
            graficar_biseccion(detalles, ax, fig)
        else:
            messagebox.showerror("Error", f"Tipo de ejercicio '{ejercicio_tipo}' no soportado para graficar.")
            graficar_window.destroy()
            return
    except Exception as e:
        messagebox.showerror("Error de Graficación", f"No se pudo graficar el ejercicio.\n{e}")
        graficar_window.destroy()
        return

    # Integrar la figura en Tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side='top', fill='both', expand=True)

    # Añadir la barra de herramientas de navegación
    toolbar = NavigationToolbar2Tk(canvas, frame)
    toolbar.update()
    canvas.get_tk_widget().pack(side='top', fill='both', expand=True)

    # Añadir anotaciones interactivas
    mplcursors.cursor(ax, hover=True)

    # Botón para cerrar la ventana de graficación
    close_button = ttk.Button(frame, text="Cerrar", command=graficar_window.destroy)
    close_button.pack(side='bottom', pady=10)


def graficar_gauss(detalles, ax, fig):
    """
    Grafica una distribución de Gauss (Normal) con controles interactivos.

    Parámetros:
    - detalles: Diccionario con las claves 'media', 'desviacion', 'rango', 'num_puntos'.
    - ax: Eje de matplotlib donde se dibujará el gráfico.
    - fig: Figura de matplotlib para añadir widgets.
    """
    # Valores iniciales
    media = detalles.get('media', 0)
    desviacion = detalles.get('desviacion', 1)
    rango = detalles.get('rango', (-10, 10))
    num_puntos = detalles.get('num_puntos', 1000)

    # Crear datos iniciales
    x = np.linspace(rango[0], rango[1], num_puntos)
    y = (1 / (desviacion * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - media) / desviacion) ** 2)
    line, = ax.plot(x, y, label=f'Distribución de Gauss (μ={media}, σ={desviacion})', color='blue')

    # Configurar el gráfico
    ax.set_title('Distribución de Gauss (Normal)')
    ax.set_xlabel('x')
    ax.set_ylabel('Densidad de Probabilidad')
    ax.legend()
    ax.grid(True)

    # Crear sliders para interactuar con la media y desviación usando matplotlib.widgets
    axcolor = 'lightgoldenrodyellow'
    ax_media = plt.axes([0.15, 0.1, 0.65, 0.03], facecolor=axcolor)
    slider_media = Slider(ax_media, 'Media', rango[0], rango[1], valinit=media, valstep=0.1)

    ax_desviacion = plt.axes([0.15, 0.05, 0.65, 0.03], facecolor=axcolor)
    slider_desviacion = Slider(ax_desviacion, 'Desviación', 0.1, 10.0, valinit=desviacion, valstep=0.1)

    # Función para actualizar la gráfica
    def actualizar(val):
        new_media = slider_media.val
        new_desviacion = slider_desviacion.val
        y_new = (1 / (new_desviacion * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - new_media) / new_desviacion) ** 2)
        line.set_ydata(y_new)
        line.set_label(f'Distribución de Gauss (μ={new_media}, σ={new_desviacion})')
        ax.legend()
        fig.canvas.draw_idle()

    # Asociar los sliders a la función de actualización
    slider_media.on_changed(actualizar)
    slider_desviacion.on_changed(actualizar)


def graficar_matriz_escalonada(detalles, ax, fig):
    """
    Grafica una matriz escalonada como una imagen de calor con interactividad mejorada.

    Parámetros:
    - detalles: Diccionario con la clave 'matriz', que es una lista de listas o un arreglo de NumPy.
    - ax: Eje de matplotlib donde se dibujará el gráfico.
    - fig: Figura de matplotlib para añadir widgets.
    """
    matriz = detalles.get('matriz', [])

    if not matriz:
        raise ValueError("La matriz está vacía o no se proporcionó.")

    matriz = np.array(matriz)

    cax = ax.imshow(matriz, cmap='viridis', aspect='auto')
    ax.set_title('Matriz Escalonada')
    ax.set_xlabel('Columnas')
    ax.set_ylabel('Filas')
    fig.colorbar(cax, ax=ax, label='Valor')

    # Añadir interactividad para mostrar el valor de cada celda al pasar el cursor
    def format_coord(x, y):
        col = int(x + 0.5)
        row = int(y + 0.5)
        if 0 <= row < matriz.shape[0] and 0 <= col < matriz.shape[1]:
            z = matriz[row, col]
            return f'x={col}, y={row}, value={z}'
        else:
            return f'x={x:.1f}, y={y:.1f}'

    ax.format_coord = format_coord


def graficar_ecuaciones_matrices(detalles, ax, fig):
    """
    Grafica las soluciones de un sistema de ecuaciones lineales representado por una matriz con interactividad.

    Parámetros:
    - detalles: Diccionario con las claves 'matriz' y 'resultados'.
    - ax: Eje de matplotlib donde se dibujará el gráfico.
    - fig: Figura de matplotlib para añadir widgets.
    """
    matriz = detalles.get('matriz', [])
    resultados = detalles.get('resultados', [])

    if not matriz or not resultados:
        raise ValueError("La matriz o los resultados están vacíos o no se proporcionaron.")

    matriz = np.array(matriz)
    resultados = np.array(resultados)

    try:
        soluciones = np.linalg.solve(matriz, resultados)
    except np.linalg.LinAlgError as e:
        raise ValueError(f"Error al resolver el sistema de ecuaciones: {e}")

    num_var = len(soluciones)
    variables = [f'x{i+1}' for i in range(num_var)]

    # Configurar el gráfico
    if num_var == 2:
        # Graficar líneas de ecuaciones en 2D
        x_vals = np.linspace(-10, 10, 400)
        for i, row in enumerate(matriz):
            if row[1] != 0:
                y_vals = (resultados[i] - row[0] * x_vals) / row[1]
                ax.plot(x_vals, y_vals, label=f'Ecuación {i+1}: {variables[0]}={soluciones[i]:.2f}', linewidth=2)
            else:
                # Línea vertical
                x = resultados[i] / row[0]
                ax.axvline(x=x, label=f'Ecuación {i+1}: {variables[0]}={soluciones[i]:.2f}', linestyle='--', linewidth=2)
        ax.scatter(soluciones[0], soluciones[1], color='red', zorder=5, label='Solución', s=100)
        ax.set_xlabel(variables[0])
        ax.set_ylabel(variables[1])
        ax.set_title('Sistema de Ecuaciones Lineales')
        ax.legend()
        ax.grid(True)

        # Añadir interactividad para mostrar coordenadas
        mplcursors.cursor(ax, hover=True)
    elif num_var == 3:
        # Graficar planos de ecuaciones en 3D
        from mpl_toolkits.mplot3d import Axes3D  # Importación necesaria para 3D

        ax = fig.add_subplot(111, projection='3d')
        x_vals = np.linspace(-10, 10, 20)
        y_vals = np.linspace(-10, 10, 20)
        X, Y = np.meshgrid(x_vals, y_vals)

        for i, row in enumerate(matriz):
            if row[2] != 0:
                Z = (resultados[i] - row[0] * X - row[1] * Y) / row[2]
                ax.plot_surface(X, Y, Z, alpha=0.5)
            elif row[1] != 0:
                # Plano horizontal
                Y_plane = resultados[i] / row[1]
                ax.plot_surface(X, Y_plane * np.ones_like(X), Y, alpha=0.5)
            else:
                # Plano vertical
                X_plane = resultados[i] / row[0]
                ax.plot_surface(X_plane * np.ones_like(Y), Y, X, alpha=0.5)

        ax.scatter(soluciones[0], soluciones[1], soluciones[2], color='red', s=100, label='Solución')
        ax.set_xlabel(variables[0])
        ax.set_ylabel(variables[1])
        ax.set_zlabel(variables[2])
        ax.set_title('Sistema de Ecuaciones Lineales en 3D')
        ax.legend()

        # Añadir interactividad para mostrar coordenadas
        mplcursors.cursor(ax, hover=True)

        # Añadir sliders para rotar la vista
        ax_elev = plt.axes([0.15, 0.15, 0.65, 0.02], facecolor=axcolor)
        slider_elev = Slider(ax_elev, 'Elevación', 0, 90, valinit=30, valstep=1)

        ax_azim = plt.axes([0.15, 0.10, 0.65, 0.02], facecolor=axcolor)
        slider_azim = Slider(ax_azim, 'Azimut', -180, 180, valinit=45, valstep=1)

        def actualizar_vista(val):
            ax.view_init(elev=slider_elev.val, azim=slider_azim.val)
            fig.canvas.draw_idle()

        slider_elev.on_changed(actualizar_vista)
        slider_azim.on_changed(actualizar_vista)
    else:
        # Para sistemas con más variables, no se puede graficar directamente
        ax.text(0.5, 0.5, "Visualización no disponible para más de 3 variables.", transform=ax.transAxes,
                fontsize=14, ha='center')
        ax.axis('off')

    ax.grid(True)

    # Opcional: Añadir botones para rotar la vista en 3D
    if num_var == 3:
        # Ya se implementaron sliders para controlar la vista
        pass  # Se puede eliminar o mantener según preferencia


def graficar_biseccion(detalles, ax, fig):
    """
    Grafica el proceso del método de bisección, mostrando la función y cómo el intervalo se reduce en cada iteración.

    Parámetros:
    - detalles: Diccionario con las claves 'function', 'history', 'a', 'b'.
    - ax: Eje de matplotlib donde se dibujará el gráfico.
    - fig: Figura de matplotlib para añadir widgets.
    """
    # Obtener detalles
    func_str = detalles.get('function', '')
    history = detalles.get('history', [])
    a_initial = detalles.get('a', 0)
    b_initial = detalles.get('b', 1)

    if not func_str or not history:
        raise ValueError("Detalles insuficientes para graficar el método de bisección.")

    # Crear una función segura para evaluar f(x)
    def evaluate_function(func, x):
        try:
            allowed_names = {"x": x, "math": math}
            return eval(func, {"__builtins__": None}, allowed_names)
        except Exception as e:
            raise ValueError(f"Error al evaluar la función: {e}")

    # Crear datos para graficar f(x)
    # Determinar el rango de x basado en los valores a y b
    buffer = (b_initial - a_initial) * 0.1  # 10% de buffer
    x_min = a_initial - buffer
    x_max = b_initial + buffer
    x = np.linspace(x_min, x_max, 1000)
    y = [evaluate_function(func_str, xi) for xi in x]
    ax.plot(x, y, label=f"f(x) = {func_str}", color='blue')

    # Dibujar el eje y=0
    ax.axhline(0, color='black', linewidth=0.5)

    # Colores para iteraciones
    colors = plt.cm.viridis(np.linspace(0, 1, len(history)))

    # Plotear cada iteración
    for idx, record in enumerate(history):
        a = record['a']
        b = record['b']
        c = record['c']
        fc = record['f(c)']
        color = colors[idx]

        # Dibujar líneas verticales para a y b
        ax.axvline(a, color=color, linestyle='--', linewidth=1, alpha=0.7)
        ax.axvline(b, color=color, linestyle='--', linewidth=1, alpha=0.7)

        # Marcar el punto c
        ax.plot(c, fc, marker='o', color=color)

        # Añadir una línea horizontal desde c hasta el eje y=0
        ax.plot([c, c], [0, fc], color=color, linestyle=':', linewidth=1)

        # Añadir anotación de iteración
        ax.annotate(f"{record['iteration']}", (c, fc), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8, color=color)

    # Configurar el gráfico
    ax.set_title('Método de Bisección')
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.legend()
    ax.grid(True)

    # Opcional: Añadir sliders o interactividad adicional si se desea


# Las demás funciones graficar_gauss, graficar_matriz_escalonada y graficar_ecuaciones_matrices permanecen igual...

# Ejemplo de uso
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Aplicación de Graficación")

    # Ejemplo de ejercicio de distribución de Gauss
    ejercicio_gauss = {
        'type': 'Gauss',
        'details': {
            'media': 0,
            'desviacion': 1,
            'rango': (-10, 10),
            'num_puntos': 1000
        }
    }

    # Ejemplo de ejercicio de matriz escalonada
    ejercicio_escalonada = {
        'type': 'Escalonada',
        'details': {
            'matriz': [
                [1, 2, 3],
                [0, 1, 4],
                [0, 0, 1]
            ]
        }
    }

    # Ejemplo de ejercicio de ecuaciones
    ejercicio_ecuaciones = {
        'type': 'Ecuaciones',
        'details': {
            'matriz': [
                [2, 1, -1],
                [-3, -1, 2],
                [-2, 1, 2]
            ],
            'resultados': [8, -11, -3]
        }
    }

    # Ejemplo de ejercicio de bisección
    ejercicio_biseccion = {
        'type': 'Biseccion',
        'details': {
            'function': 'math.cos(x) - x',  # Ejemplo: f(x) = cos(x) - x
            'a': 0,                           # Intervalo inicial [0, 1]
            'b': 1,
            'history': [
                {'iteration': 1, 'a': 0, 'b': 1, 'c': 0.5, 'f(c)': math.cos(0.5), 'relative_error': None},
                {'iteration': 2, 'a': 0.5, 'b': 1, 'c': 0.75, 'f(c)': math.cos(0.75), 'relative_error': abs((0.75 - 0.5) / 0.75) * 100},
                {'iteration': 3, 'a': 0.75, 'b': 1, 'c': 0.875, 'f(c)': math.cos(0.875), 'relative_error': abs((0.875 - 0.75) / 0.875) * 100},
                # Añade más iteraciones según sea necesario
            ]
        }
    }

    # Botones para abrir ventanas de graficación
    btn_gauss = ttk.Button(root, text="Graficar Gauss", command=lambda: open_graficar_window(root, ejercicio_gauss))
    btn_gauss.pack(pady=10)

    btn_escalonada = ttk.Button(root, text="Graficar Matriz Escalonada", command=lambda: open_graficar_window(root, ejercicio_escalonada))
    btn_escalonada.pack(pady=10)

    btn_ecuaciones = ttk.Button(root, text="Graficar Ecuaciones", command=lambda: open_graficar_window(root, ejercicio_ecuaciones))
    btn_ecuaciones.pack(pady=10)

    btn_biseccion = ttk.Button(root, text="Graficar Bisección", command=lambda: open_graficar_window(root, ejercicio_biseccion))
    btn_biseccion.pack(pady=10)

    root.mainloop()
