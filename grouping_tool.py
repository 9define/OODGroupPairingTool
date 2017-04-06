# argparse libs
import argparse

# for reading user cred files
from utils.creds import *

# for sending the emails
from utils.email_lib import *

# for parsing group data spreadsheets
from classes.spreadsheet import Spreadsheet


# run main with passed system args
def main(args):
    # get information about the email
    creds, smtp_server, use_tls = get_email_info()

    # parse csv file into the two messages and groups with ratings
    spreadsheet = Spreadsheet(args.csv_file)

    # # get the message's recipients
    # recipients = input('Input all recipients (separated by semi-colons with no spaces): ').split(';')
    #
    # # get the message subject
    # subject = input('Input the message subject: ')
    #
    # # get the message body
    # body = input('Input the message body: ')
    #
    # # send the email with the gathered info
    # send_msg(creds['email address'], creds['password'], creds['user name'],
    #          recipients, subject, body, smtp_server, use_tls)

    # send all the emails!
    send_emails(creds, smtp_server, use_tls, spreadsheet)


# get information about how to send the email, such as user creds, smtp server, and protocol type
def get_email_info():
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

    return creds, smtp_server, use_tls


# create the circular group order
def order_groups(groups):
    ordered = []
    top = True
    while len(groups) > 0:
        if top:
            ordered.append(groups.pop(0))
            top = False
        else:
            ordered.append(groups.pop())
            top = True

    return ordered


# send all emails
def send_emails(creds, smtp_server, use_tls, spreadsheet):
    spreadsheet.groups.sort()

    # order all the groups properly (that is, in a circle)
    spreadsheet.groups = order_groups(sorted(spreadsheet.groups))

    for g in spreadsheet.groups:
        print(str(g) + ' --- ' + str(g.grade))
    print('*************')

    groups = spreadsheet.groups

    # set each group's provider and consumer
    for i in range(0, len(spreadsheet.groups)):
        if i == 0:
            groups[i].provider_group = groups[len(groups) - 1]
            groups[i].consumer_group = groups[i + 1]
        elif i == len(groups) - 1:
            groups[i].provider_group = groups[i - 1]
            groups[i].consumer_group = groups[0]
        else:
            groups[i].provider_group = groups[i - 1]
            groups[i].consumer_group = groups[i + 1]

    # send each group a test email
    for g in groups:
        # send_msg(creds['email address'], creds['password'], creds['user name'], g.get_emails(), "Group test email (title/subject)",
        # "Group test email (body)", smtp_server, use_tls)

        # send the group their consumer info
        send_msg(creds['email address'], creds['password'], creds['user name'], g.get_emails(),
                 "OOD HW8 Code Exchange - Consumer Info", g.fill_in_message(spreadsheet.message_to_senders),
                 smtp_server, use_tls)

        # send the group their provider info
        send_msg(creds['email address'], creds['password'], creds['user name'], g.get_emails(),
                 "OOD HW8 Code Exchange - Provider Info", g.fill_in_message(spreadsheet.message_to_consumers),
                 smtp_server, use_tls)


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
