import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv
import os

# Cargar las variables del archivo .env
load_dotenv()

# Configuración de Notion
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# Configuración del correo
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
DESTINATARIO = os.getenv("DESTINATARIO")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def get_tasks_from_notion():
    """Obtener recordatorios pendientes desde Notion."""
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    response = requests.post(url, headers=headers)
    
    if response.status_code == 200:
        tasks = response.json()["results"]
        filtered_tasks = [
            {
                "title": task["properties"]["Name"]["title"][0]["text"]["content"],
                "date": task["properties"]["Date"]["date"]["start"] if task["properties"].get("Date") and task["properties"]["Date"].get("date") else "No hay fecha",
                "status": task["properties"]["Status"]["status"]["name"] if "Status" in task["properties"] else "Pendiente"
            }
            for task in tasks
            if task["properties"]["Status"]["status"]["name"] in ["Pendiente", "Sin empezar"]
        ]
        return filtered_tasks
    return []


def enviar_correo(recordatorios):
    """Envía un correo con los recordatorios desde Notion en formato HTML."""
    if not recordatorios:
        return

    asunto = "Recordatorios pendientes"
    cuerpo = """
    <html>
        <head>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    margin: 0;
                    padding: 20px;
                    background-color: #f4f4f4;
                }
                .container {
                    width: 80%;
                    margin: 0 auto;
                    background-color: #fff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }
                h2 {
                    color: #333;
                    text-align: center;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }
                table, th, td {
                    border: 1px solid #ddd;
                }
                th, td {
                    padding: 10px;
                    text-align: left;
                }
                th {
                    background-color: #f4f4f4;
                }
                tr:nth-child(even) {
                    background-color: #f9f9f9;
                }
                .status {
                    font-weight: bold;
                    padding: 5px;
                    border-radius: 5px;
                }
                .Pendiente {
                    background-color: #ffcc00;
                    color: #fff;
                }
                .SinEmpezar {
                    background-color: #f44336;
                    color: #fff;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Recordatorios pendientes</h2>
                <p>Estos son tus recordatorios pendientes:</p>
                <table>
                    <tr>
                        <th>Título</th>
                        <th>Fecha</th>
                        <th>Estado</th>
                    </tr>
    """
    
    for tarea in recordatorios:
        fecha = tarea["date"]
        title = tarea["title"]
        status = tarea["status"]
        status_class = "Pendiente" if status == "Pendiente" else "SinEmpezar"
        
        cuerpo += f"""
        <tr>
            <td>{title}</td>
            <td>{fecha}</td>
            <td><span class="status {status_class}">{status}</span></td>
        </tr>
        """

    cuerpo += """
                </table>
            </div>
        </body>
    </html>
    """

    # Crear el mensaje
    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = DESTINATARIO
    msg["Subject"] = asunto
    msg.attach(MIMEText(cuerpo, "html"))  # Usamos "html" para el cuerpo del correo

    try:
        # Enviar el correo
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Cifra la conexión
        server.login(EMAIL, PASSWORD)  # Inicia sesión con tu correo y contraseña de aplicación
        server.sendmail(EMAIL, DESTINATARIO, msg.as_string())  # Envía el correo
        server.quit()  # Cierra la conexión
        print("Correo enviado exitosamente.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")


def main():
    """Función principal que obtiene las tareas y las envía por correo."""
    tareas = get_tasks_from_notion()
    if tareas:
        enviar_correo(tareas)
    else:
        print("No hay recordatorios pendientes.")

# Ejecutar el script
if __name__ == "__main__":
    main()
