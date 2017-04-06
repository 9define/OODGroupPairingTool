# email libs
import smtplib


# send an email via an smtp server given the proper fields
def send_msg(user, passwd, sender_name, recipients, subject, body, smtp_server, use_tls):
    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
            """ % (sender_name, ", ".join(recipients), subject, body)

    # try to send the message with SSL or TLS
    try:
        # get the correct kind of server connection object based on the user's preferred security protocol
        server = smtplib.SMTP(smtp_server, 587) if use_tls else smtplib.SMTP_SSL(smtp_server, 465)

        # open a connection to the smtp server
        server.ehlo()

        # if the user wants to use TLS, start doing so
        if use_tls:
            server.starttls()

        # try to login on the user's behalf
        server.login(user, passwd)

        # send the constructed message
        server.sendmail(user, recipients, message)

        # close the connection with the server
        server.close()

        # inform the user that the email has been sent
        print('Message sent!')

    # in case something goes wrong
    except:
        print("Failed to send message.")
