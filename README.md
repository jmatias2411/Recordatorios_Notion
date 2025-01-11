# Bot de Recordatorios con Notion!

Este proyecto es un script de Python que obtiene tareas pendientes desde Notion y envía un correo electrónico con los recordatorios. El script filtra las tareas según su estado (Pendiente o Sin Empezar) y las muestra de manera atractiva en formato HTML.

## Requisitos

- Python 3.x
- `requests` para interactuar con la API de Notion.
- `smtplib` y `email.mime` para enviar correos electrónicos.
- `python-dotenv` para cargar variables de entorno desde un archivo `.env`.

## Instalación

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/jmatias2411/Recordatorios_Notion.git
   cd notion-reminder-bot
   ```

2. **Crea un entorno virtual y activa**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En macOS/Linux
   venv\Scripts\activate  # En Windows
   ```

3. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Crea un archivo `.env`** para almacenar las credenciales y tokens sensibles. Asegúrate de agregar el siguiente contenido en el archivo `.env`:

   ```dotenv
   NOTION_TOKEN=tu_notion_token
   DATABASE_ID=tu_notion_database_id
   EMAIL=tu_correo@gmail.com
   PASSWORD=tu_contraseña_de_aplicación
   DESTINATARIO=destinatario@dominio.com
   ```

   - Puedes obtener el `NOTION_TOKEN` y `DATABASE_ID` desde la [API de Notion](https://www.notion.so/my-integrations) y configurando una base de datos en tu cuenta de Notion.
   - **Nota**: Si usas Gmail, necesitas generar una [contraseña de aplicación](https://support.google.com/accounts/answer/185833) para poder usarla en este script.

## Uso

1. **Ejecuta el script**:
   ```bash
   python recuerdame.py
   ```

2. El script obtendrá las tareas desde la base de datos de Notion que tengan el estado **Pendiente** o **Sin Empezar** y enviará un correo HTML con los detalles de estas tareas.

## Descripción del código

- **`get_tasks_from_notion()`**: Esta función obtiene todas las tareas de la base de datos de Notion, filtra las tareas con estado **Pendiente** o **Sin Empezar** y devuelve los detalles de cada tarea.
- **`enviar_correo()`**: Esta función envía un correo HTML con los recordatorios pendientes, mostrando la fecha, el título y el estado de cada tarea.
- **`main()`**: Esta función principal ejecuta el proceso: obtiene las tareas y las envía por correo.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.

---
