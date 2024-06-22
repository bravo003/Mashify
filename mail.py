import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

def send_mail(to, filename):
    email_address = "bravo.work.me@gmail.com"
    email_password = "fqzalazjwlltsmnr"

    # Create the email container
    msg = MIMEMultipart()
    msg['Subject'] = "Mashup File"
    msg['From'] = email_address
    msg['To'] = to

    # Attach the text part
    body = MIMEText("Please find attached the mashup file.")
    msg.attach(body)

    # Attach the file
    with open(filename, 'rb') as f:
        part = MIMEApplication(f.read(), Name='Mashup.zip')
        part['Content-Disposition'] = f'attachment; filename="Mashup.zip"'
        msg.attach(part)

    # Send the email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(email_address, email_password)
            server.sendmail(email_address, to, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")






