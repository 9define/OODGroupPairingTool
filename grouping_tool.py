# email libs
import smtplib

# system functions
import sys

# hidden password input
import getpass


# run main with passed system args
def main(argv):
    # get the user's/sender's name
    user_name = input('Input the sender\'s name: ')

    # get the user's/sender's email address
    user = input('Input the sender address: ')

    # get the user's password discreetly
    passwd = getpass.getpass()

    # ask the user if they want to specify an smtp server
    use_gmail = input('Do you want to use gmail? (Y/n): ').upper() == 'Y'

    # determine the smtp server to use
    if use_gmail:
        smtp_server = 'smtp.gmail.com'
    else:
        smtp_server = input('Which smtp server then?: ')

    # determine SSL or TLS
    use_tls = input('Would you like to use SSL(S) or TLS(T)?: ').upper() == 'T'

    # get the message's recipients
    recipients = input('Input all recipients (separated by semi-colons with no spaces): ').split(';')

    # get the message subject
    subject = input('Input the message subject: ')

    # get the message body
    body = input('Input the message body: ')

    # send the email with the gathered info
    send_msg(user, passwd, user_name, recipients, subject, body, smtp_server, use_tls)


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
        print("Failed to sent message.")


# run script with sys args
if __name__ == "__main__":
    main(sys.argv)