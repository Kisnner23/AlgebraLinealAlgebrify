# Algebrify

**Algebrify** es una calculadora de álgebra lineal desarrollada en Python, pensada para estudiantes y profesionales que buscan resolver problemas de álgebra de manera sencilla e intuitiva. La aplicación incluye una interfaz gráfica moderna, características personalizables, y funciones avanzadas para trabajar con ecuaciones y matrices.

## Características

1. **Interfaz de Usuario Moderna**: Pantalla de bienvenida animada que muestra el progreso de carga, menú principal en pantalla completa con colores y estilo personalizables, y una barra de búsqueda para acceso rápido a las funciones de álgebra.

2. **Operaciones de Álgebra Lineal**: Incluye resolución de ecuaciones lineales individuales, resolución de sistemas con métodos como sustitución y eliminación, y simplificación de matrices a su forma escalonada para análisis y resolución de sistemas lineales.

3. **Gestión del Historial de Ejercicios**: Almacena cada operación realizada en un archivo JSON (`history.json`) que se actualiza automáticamente. Permite eliminar ejercicios específicos o descargar el historial en formato PDF. Incluye detalles de cada ejercicio, como los pasos y resultados, accesibles desde la interfaz.

4. **Personalización de Apariencia**: Configuración de colores de fondo y texto para la interfaz, adaptable a las preferencias del usuario.

## Estructura del Proyecto

El repositorio contiene los siguientes archivos y carpetas: **MainMenu.py**: Archivo principal que contiene la interfaz y lógica de Algebrify. **assets/**: Carpeta para íconos y gráficos, como el logo, símbolo matemático, y botones de descarga. **history.json**: Archivo para almacenar el historial de ejercicios resueltos. **README.md**: Este documento, con detalles sobre el uso y las funcionalidades de Algebrify.

## Requisitos

Antes de comenzar, asegúrate de tener los siguientes elementos: **Python 3.x**, **tkinter** (incluido en la mayoría de las instalaciones de Python), y **reportlab** para la generación de archivos PDF, instalable con `pip install reportlab`.

## Instalación

1. Clona el repositorio: `git clone https://github.com/tuusuario/Algebrify.git` y entra en la carpeta del proyecto con `cd Algebrify`.
2. Asegúrate de instalar las dependencias necesarias con `pip install -r requirements.txt`.
3. Verifica que la carpeta **assets** contenga los íconos necesarios (logo, símbolo matemático, icono de descarga). Si necesitas cambiar las rutas, ajusta los valores de `LOGO_PATH`, `MATH_SYMBOL_PATH`, y `DOWNLOAD_ICON_PATH` en `MainMenu.py`.

## Uso

Para ejecutar Algebrify, utiliza el siguiente comando: `python MainMenu.py`. Una vez iniciada la aplicación, sigue estos pasos:

1. **Pantalla de Bienvenida**: Una pantalla de carga con barra de progreso y logo que muestra la transición al menú principal.
2. **Menú Principal**: Incluye una barra de búsqueda, accesos directos a operaciones y un botón de configuración para personalizar la apariencia.
3. **Historial**: Permite ver, descargar o eliminar ejercicios anteriores. También puedes descargar el historial completo en formato PDF.
4. **Salida**: Presiona `Esc` para salir del modo de pantalla completa o usa el botón **Salir** en el menú principal.

## Documentación de Funcionalidades

### Pantalla de Bienvenida

- **Objetivo**: Dar una introducción visual al usuario mientras la aplicación carga.
- **Componentes**: Logo de Algebrify, barra de progreso con actualización en tiempo real, y mensaje de bienvenida.

### Menú Principal

- **Objetivo**: Ofrecer una interfaz intuitiva para la navegación y selección de operaciones.
- **Funciones**: Barra de búsqueda para encontrar rápidamente una operación, botón de configuración para personalizar colores de fondo y texto, y accesos directos a la lista de operaciones y al historial de ejercicios.

### Lista de Operaciones

- **Objetivo**: Proporcionar acceso rápido a funciones de álgebra.
- **Operaciones Disponibles**: Incluye ecuaciones lineales, sistema de ecuaciones lineales y escalonadas.

### Historial de Ejercicios

- **Objetivo**: Facilitar el acceso y revisión de ejercicios anteriores.
- **Opciones**: Eliminar ejercicios específicos del historial, descargar un ejercicio seleccionado en PDF, y exportar el historial completo en PDF.

### Configuración de Apariencia

- **Objetivo**: Permitir la personalización de la interfaz.
- **Opciones**: Selección de colores para fondo y texto, usando el selector de color de tkinter.

## Contribuciones

¡Tus aportaciones son bienvenidas! Si deseas contribuir, haz un fork del repositorio, crea una nueva rama con tu función o mejora (`git checkout -b feature/nueva-funcionalidad`), haz commit de tus cambios (`git commit -m "Descripción de la mejora"`), sube tu rama y envía un pull request (`git push origin feature/nueva-funcionalidad`).

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más información.

---

**Algebrify** - Simplifica tu trabajo de álgebra con una herramienta poderosa y accesible.
