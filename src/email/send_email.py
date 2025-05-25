import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(recipient, message):
    try:
        # SMTP Gmail Configuration
        smtp_server = "smtp.gmail.com"
        port = 587
        sender = 'xxxx'
        password = 'xxxx'
        
        # MIME Object Creation
        email = MIMEMultipart()
        email["From"] = sender
        email["To"] = recipient
        email["Subject"] = 'Appointment Information'
        
        # Create a messages
        email.attach(MIMEText(message, "plain"))
        
        # Make a connection to Gmail's SMTP server
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        
        # Login to the email server
        server.login(sender, password)
        
        # Send the email
        text = email.as_string()
        server.sendmail(sender, recipient, text)
        
        # Close the connection
        server.quit()
        return True, "Email berhasil dikirim!"
        
    except Exception as e:
        return False, f"Terjadi kesalahan: {str(e)}"
