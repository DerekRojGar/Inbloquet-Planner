# Planificador Semanal INBLOQUET 📅

Esta es una aplicación web desarrollada con **Streamlit** para la planificación semanal de actividades en INBLOQUET. Permite a los usuarios registrar, editar, eliminar y exportar actividades relacionadas con escuelas, grupos, temas, participantes y notas adicionales.

---

## 🛠️ Librerías Utilizadas

El proyecto utiliza las siguientes librerías de Python:

- **`pandas`**: Para la manipulación y almacenamiento de datos en formato CSV.
- **`streamlit`**: Para la creación de la interfaz web interactiva.
- **`datetime`**: Para el manejo de fechas y generación de semanas.
- **`base64`**: Para la codificación de archivos en la exportación de datos.
- **`openpyxl`**: Para la creación de archivos Excel con diseño personalizado.
- **`os`**: Para verificar la existencia de archivos y manejo de rutas.

---

## 🚀 Funcionalidades Principales

1. **Configuración Inicial**:
   - Selección de semana y año.
   - Personalización de una frase inspiradora del día.

2. **Registro de Actividades**:
   - Formulario para agregar nuevas actividades.
   - Selección de escuelas, grupos, tema, participantes y notas adicionales.

3. **Visualización Semanal**:
   - Vista de calendario con actividades organizadas por día.
   - Expansión de tarjetas para ver detalles completos.

4. **Edición y Eliminación**:
   - Posibilidad de editar o eliminar actividades registradas.

5. **Exportación de Datos**:
   - Exportación de la planificación a archivos Excel y CSV.
   - Diseño personalizado en el archivo Excel generado.

6. **Persistencia de Datos**:
   - Los datos se guardan en un archivo `actividades.csv` para su reutilización.

---

## 🖥️ Interfaz de Usuario

### Barra Lateral
- **Logo**: Muestra el logo de INBLOQUET.
- **Configuración**: Selección de semana y año.
- **Frase Inspiradora**: Edición y guardado de una frase motivacional.

### Contenido Principal
- **Formulario de Actividades**: Permite agregar nuevas actividades.
- **Vista Semanal**: Muestra las actividades organizadas por día.
- **Detalle Completo**: Lista todas las actividades con opciones de edición y eliminación.
- **Exportación**: Botón para exportar los datos a Excel y CSV.

---

## 📂 Estructura del Proyecto

- **`planificador_final.py`**: Código principal de la aplicación.
- **`actividades.csv`**: Archivo CSV que almacena las actividades registradas.
- **`README.md`**: Este archivo, con la documentación del proyecto.
- **`Inbloquet.png`**: Imagen del logo de INBLOQUET (debe estar en la misma carpeta).

---

## 🛠️ Instalación y Ejecución

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/tu-usuario/nombre-del-repositorio.git
   cd nombre-del-repositorio