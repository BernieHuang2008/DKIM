import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import dkim


def send_email():
    # use 163 mail as an example
    server = smtplib.SMTP("smtp.163.com", 25)
    server.login("berniehuang2008@163.com", "BYISPUMDNZHJAPBK")
    # [TODO: Need login]

    # construct a email object
    # Create a multipart message and set headers
    msg = MIMEMultipart()
    msg["From"] = "黄锦源<berniehuang@openteens.org>"
    msg["To"] = "berniehuang2008<berniehuang2008@163.com>"
    msg["Subject"] = "测试dkim"

    # Add body to email
    msg.attach(MIMEText("这是测试内容", "plain"))

    # Add DKIM-Signature to email
    with open("private_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(), password=None, backend=default_backend()
        )
        private_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

    dkim.sign(msg.as_bytes(), b"testdkim", b"openteens.org", private_key)

    # send the email
    server.send_message(msg)


send_email()
