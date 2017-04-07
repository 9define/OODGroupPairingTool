# for decoding of stored passwords
import base64

# hidden password input
import getpass


# get the user's creds if they don't provide a file at runtime
def get_user_creds():
    # get the user's/sender's name
    user_name = input('Input the sender\'s name: ')

    # get the user's/sender's email address
    user = input('Input the sender address: ')

    # get the user's password discreetly
    passwd = getpass.getpass()

    return {"user name": user_name, "email address": user, "password": passwd}


# parse a user creds file
def parse_creds_file(creds_file):
    # the credential dictionary to return
    creds = {}

    # get fields from the file and put them in the creds dict
    creds['user name'] = next(creds_file).rstrip()
    creds['email address'] = next(creds_file).rstrip()

    # decode the password and strip it of its leading b' and trailing '
    password = str(base64.b64decode(next(creds_file)))
    creds['password'] = password[2:2+len(password) - 3]

    return creds
