import re
import smtplib
from time import sleep
from email.mime.text import MIMEText

# Configuración del servidor SMTP
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL = 'pablopedrosap@gmail.com'
PASSWORD = 'wtfq xfza lwme yywx'

# Función para procesar emails y generar nombres amigables
def procesar_emails(archivo_txt):
    with open(archivo_txt, 'r') as file:
        emails = file.readlines()
    
    lista_procesada = []
    for email in emails:
        email = email.strip()
        local = re.sub(r'@kidsandus\.es', '', email)  # Quita el dominio
        if '.cat' in email:
            local = re.sub(r'@kidsandus\.cat', '', email)    # Quita el dominio
        if '.net' in email:
            local = re.sub(r'@kidsandus\.net', '', email)    # Quita el dominio
        
        
        local = local.replace('.', ' ').title()  # Convierte a formato amigable
        lista_procesada.append({'email': email, 'nombre_local': local})
    
    return lista_procesada

# Enviar correo
def enviar_email(destinatario, nombre_local):
    subject = "Sobre vuestros informes"
    body = f"""
Hola Equipo de Kids&Us de {nombre_local},

Me llamo Pablo Pedrosa y actualmente estoy ayudando a varios centros en la generación de informes para sus alumnos.
Conozco el esfuerzo que supone preparar los reports de manera manual y corregir los de los profesores. Por ello, he desarrollado una solución automatizada que ya está funcionando con éxito en otros centros, ahorrándoles muchísimo tiempo.

Los informes quedan escritos directamente en MyClassroom en cuestión de minutos, manteniendo el nivel de calidad y personalización que requerís sin precisar revisión posterior por vuestra parte.

Para que podáis probarlo sin compromiso, me encantaría ofreceros 50 informes gratuitos. De esta manera, podréis evaluar si esta solución aporta valor a vuestro centro. También puedo poneros en contacto con otros coordinadores y directores, que estarán encantados de compartir su experiencia de primera mano.

Si os interesa, estoy a vuestra disposición para organizar una videollamada en la que podamos resolver cualquier duda.

Un cordial saludo,
Pablo Pedrosa
LinkedIn: https://www.linkedin.com/in/pablo-pedrosa-ppp/
    """

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL
    msg['To'] = destinatario

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)
            print(f"Correo enviado a {destinatario}")
    except Exception as e:
        print(f"Error al enviar a {destinatario}: {e}")

# Programa principal
def main():
    emails = procesar_emails('cleaned_emails.txt')
    for i, email_info in enumerate(emails):
        enviar_email(email_info['email'], email_info['nombre_local'])
        if (i + 1) % 100 == 0:  # Limitar a 100 correos por día
            print("Límite diario alcanzado. Continuando mañana...")
            break
        sleep(10)  # Pausa de 10 segundos entre correos para evitar bloqueos

if __name__ == "__main__":
    main()
