# email libs
import smtplib

# argparse libs
import argparse

# hidden password input
import getpass

# for decoding user creds
import base64


# run main with passed system args
def main(args):
    # if the user didn't provide a creds file, get their creds
    creds = None
    if args.creds is None:
        creds = get_user_creds()
    else:
        creds = parse_creds_file(open(args.creds))

    # determine the smtp server to use
    if args.server is None:
        smtp_server = 'smtp.gmail.com'
    else:
        smtp_server = args.server

    # determine SSL or TLS
    use_tls = args.usessl is False

    # get the message's recipients
    recipients = input('Input all recipients (separated by semi-colons with no spaces): ').split(';')

    # get the message subject
    subject = input('Input the message subject: ')

    # get the message body
    body = input('Input the message body: ')

    # send the email with the gathered info
    send_msg(creds['email address'], creds['password'], creds['user name'],
             recipients, subject, body, smtp_server, use_tls)


# get the user's creds if they don't provide a file at runtime
def get_user_creds():
    # get the user's/sender's name
    user_name = input('Input the sender\'s name: ')

    # get the user's/sender's email address
    user = input('Input the sender address: ')

    # get the user's password discreetly
    passwd = # input('Password: ')

    return {"user name": user_name, "email address": user, "password": passwd}


# parse a user creds file
def parse_creds_file(creds_file):
    # the credential dictionary to return
    creds = {}

    # get fields from the file and put them in the creds dict
    creds['user name'] = next(creds_file).rstrip()
    creds['email address'] = next(creds_file).rstrip()

    password = str(base64.b64decode(next(creds_file)))
    creds['password'] = password[2:2+len(password) - 3]

    return creds


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


# run script with sys args
if __name__ == "__main__":
    # create the new argparse object with a description
    parser = argparse.ArgumentParser(description=
                                     "A script to read CSV files, create group pairings, and automate the process of "
                                     "sending emails.")

    # add the CSV file required parameter
    parser.add_argument('csv_file', metavar='CSVfile', type=str,
                        help="The CSV file containing the email message to send out and all groups with their "
                             "evaluations. See the project README for more info on how to format this file.")

    # add the smtp server optional param
    parser.add_argument('--server', type=str,
                        help="If you wish to use a non-Gmail email server.")

    # add the user creds optional param
    parser.add_argument('--creds', type=str, help="Custom user credentials file, if you're going to be using this "
                                                  "script a lot and don't want to repeatedly enter your email server "
                                                  "info.")

    # let the user choose SSL over TLS, if desired
    parser.add_argument('--usessl', help="Use SSL instead of the default TLS.", action='store_true')

    # put all the args together
    args = parser.parse_args()

    # run the program
    main(args)
