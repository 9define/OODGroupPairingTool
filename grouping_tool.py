# argparse libs
import argparse

# for reading user cred files
from utils.creds import *

# for sending the emails
from utils.email_lib import *

# for parsing group data spreadsheets
from classes.spreadsheet import Spreadsheet


# run main with passed system args
def main():
    # get information about the email
    creds, smtp_server, use_tls = get_email_info()

    # parse csv file into the two messages and groups with ratings
    spreadsheet = Spreadsheet(args.csv_file)

    if args.one_person == False:
        # send all the emails!
        send_emails(creds, smtp_server, use_tls, spreadsheet, args.is_sorted == False, args.debug_mode == False, args.verbose)
    else:
        first_name, last_name = get_person_info()
        #send emails only for this person
        send_email_one_group(creds, smtp_server, use_tls, spreadsheet, args.is_sorted == False, first_name, last_name, args.debug_mode == False, args.verbose)    
        
# get first name and last name of only one person, for one-person mode
def get_person_info():
    # get the user's first name
    first_name = input('Input the first name of the person: ')
    
    # get the user's last name
    last_name = input('Input the last name of the person: ')
    
    return first_name, last_name


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
    use_tls = args.use_ssl is False

    return creds, smtp_server, use_tls


# create the circular group order
def order_groups(groups):
    # the final circular list of groups
    ordered = []

    # flag to switch when going back and forth through the list of groups to create the circle
    top = True

    # create the group circle by popping groups from the sorted list one-by-one
    while len(groups) > 0:
        if top:
            ordered.append(groups.pop(0))
            top = False
        else:
            ordered.append(groups.pop())
            top = True

    return ordered

# send emails just for one group
def send_email_one_group(creds, smtp_server, use_tls, spreadsheet, sort, first_name, last_name, send, verbose):
    # print the sorted groups, if desired
    if sort:
        spreadsheet.groups.sort()

    # print the circular ordered groups, if desired
    if sort:
        # order all the groups properly (that is, in a circle)
        spreadsheet.groups = order_groups(spreadsheet.groups)

    
    # for easy reference
    groups = spreadsheet.groups
    
    if verbose:
        for g in groups:
            print(str(g.get_emails()))
    
    #replace sender's name with actual sender in the spreadsheet messages
    spreadsheet.message_to_providers = spreadsheet.message_to_providers.replace('$sender_salutation',creds['sender_salutation'])
    
    spreadsheet.message_to_customers = spreadsheet.message_to_customers.replace('$sender_salutation',creds['sender_salutation'])
    
    if verbose:
        print('Message to providers:'+spreadsheet.message_to_providers)
        print('Message to customers:'+spreadsheet.message_to_customers)

    # set each group's provider and consumer
    for i in range(0, len(spreadsheet.groups)):
        # special i == 0 case (wrap around)
        if i == 0:
            groups[i].provider_group = groups[len(groups) - 1]
            groups[i].consumer_group = groups[i + 1]

        # special i == len - 1 case (wrap around)
        elif i == len(groups) - 1:
            groups[i].provider_group = groups[i - 1]
            groups[i].consumer_group = groups[0]

        # general case
        else:
            groups[i].provider_group = groups[i - 1]
            groups[i].consumer_group = groups[i + 1]

    
    for g in groups:
        # find if this group has the member
        if g.is_member(first_name,last_name) or g.provider_group.is_member(first_name,last_name) or g.consumer_group.is_member(first_name,last_name):
            if send:
                send_msg(creds['email address'], creds['password'], creds['user name'], g.get_emails(),
                 "CS 3500: Assignment 8 Code Exchange - Customer Info", g.fill_in_message(spreadsheet.message_to_providers),
                 smtp_server, use_tls)
        
            if verbose:
                print('Sent providers email to '+str(g.get_emails()))

            # send the group their provider info
            if send:
                send_msg(creds['email address'], creds['password'], creds['user name'], g.get_emails(),
                 "CS 3500: Assignment 8 Code Exchange - Provider Info", g.fill_in_message(spreadsheet.message_to_customers),
                 smtp_server, use_tls)

            if verbose:
                print('Sent customers email to '+str(g.get_emails()))        


# send all emails
def send_emails(creds, smtp_server, use_tls, spreadsheet, sort, send, verbose):
    # print the sorted groups, if desired
    if sort:
        spreadsheet.groups.sort()

    # print the circular ordered groups, if desired
    if sort:
        # order all the groups properly (that is, in a circle)
        spreadsheet.groups = order_groups(spreadsheet.groups)

    
    # for easy reference
    groups = spreadsheet.groups
    
    if verbose:
        print("Sorted groups:")
        for g in groups:
            print(str(g.get_emails())+":"+str(g.get_grade()))
            print()
    
    #replace sender's name with actual sender in the spreadsheet messages
    spreadsheet.message_to_providers = spreadsheet.message_to_providers.replace('$sender_salutation',creds['sender_salutation'])
    
    spreadsheet.message_to_customers = spreadsheet.message_to_customers.replace('$sender_salutation',creds['sender_salutation'])
    
    if verbose:
        print('Message to providers:'+spreadsheet.message_to_providers)
        print('Message to customers:'+spreadsheet.message_to_customers)

    # set each group's provider and consumer
    for i in range(0, len(spreadsheet.groups)):
        # special i == 0 case (wrap around)
        if i == 0:
            groups[i].provider_group = groups[len(groups) - 1]
            groups[i].consumer_group = groups[i + 1]

        # special i == len - 1 case (wrap around)
        elif i == len(groups) - 1:
            groups[i].provider_group = groups[i - 1]
            groups[i].consumer_group = groups[0]

        # general case
        else:
            groups[i].provider_group = groups[i - 1]
            groups[i].consumer_group = groups[i + 1]

    
    for g in groups:
        # send the group their consumer info
        # send each group a test email, if desired
        if send:
            send_msg(creds['email address'], creds['password'], creds['user name'], g.get_emails(),
                 "CS 3500: Assignment 8 Code Exchange - Customer Info", g.fill_in_message(spreadsheet.message_to_providers),
                 smtp_server, use_tls)
        
        if verbose:
            print('Sent providers email to '+str(g.get_emails()))

        # send the group their provider info
        if send:
            send_msg(creds['email address'], creds['password'], creds['user name'], g.get_emails(),
                 "CS 3500: Assignment 8 Code Exchange - Provider Info", g.fill_in_message(spreadsheet.message_to_customers),
                 smtp_server, use_tls)

        if verbose:
            print('Sent customers email to '+str(g.get_emails()))         

# create the program args
def add_prog_args():
    # create the new argparse object with a description
    parser = argparse.ArgumentParser(description=
                                     "A script to read CSV files, create group pairings, and automate the "
                                     "process of sending emails.")

    # add the CSV file required parameter
    parser.add_argument('csv_file', metavar='CSVfile', type=str,
                        help="The CSV file containing the email message to send out and all groups with their "
                             "evaluations. See the project README for more info on how to format this file.")

    # add the smtp server optional param
    parser.add_argument('--server', type=str,
                        help="If you wish to use a non-Gmail email server.")

    # add the user creds optional param
    parser.add_argument('--creds', metavar='CRED_FILE', type=str,
                        help="Custom user credentials file, if you're going to be using this "
                             "script a lot and don't want to repeatedly enter your email server "
                             "info.")

    # let the user choose SSL over TLS, if desired
    parser.add_argument('--use-ssl', help="Use SSL instead of the default TLS.", action='store_true')

    # enable the user to specify if their input data is pre-sorted
    parser.add_argument('--is-sorted', help="If the input data is pre-sorted.", action='store_true')

    # enable the user to run in debug mode, which doesn't send the emails, just give group output
    parser.add_argument('--debug-mode', help="Run the application without actually sending the messages.",
                        action='store_true')
    #one-member mode so that it asks for first and last name of a single person and emails only groups relevant to that group                    
    parser.add_argument('--one-person', help="Send emails relevant to only one person.",
                        action='store_true')

    #verbose mode so that it prints helpful messages as it is working                    
    parser.add_argument('--verbose', help="Run the application in verbose mode.",
                        action='store_true')

    # put all the args together
    return parser.parse_args()


# run script with sys args
if __name__ == "__main__":
    # add the program args
    args = add_prog_args()

    # run the program
    main()
