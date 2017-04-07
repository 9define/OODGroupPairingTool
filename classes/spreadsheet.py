# to get python's built-in csv libs
import csv

# be able to create groups
from classes.group import Group


# define a group data spreadsheet
class Spreadsheet(object):

    # init a spreadsheet with a given file
    def __init__(self, filepath):
        # create the csv file reader
        csv_reader = csv.reader(open(filepath), delimiter=';')

        # get the two messages
        message_line = next(csv_reader)
        self.message_to_senders = message_line[0].replace('\\n', '\n')
        self.message_to_consumers = message_line[1].replace('\\n', '\n')

        # read in all the remaining data rows into groups
        self.groups = [Group(row) for row in csv_reader]
