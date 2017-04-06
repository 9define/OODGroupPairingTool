# use the group evaluation/grade enum
from .eval import Eval

# use the group memeber/person class
from .member import Member


# define a group
class Group(object):

    # make a group of people
    def __init__(self, row):
        self.members = []
        # parse all of the members from the row data
        for cell in row[:len(row) - 1]:
            if not cell == '':
                self.members.append(Member(cell))

        # parse the group's overall grade
        self.grade = Eval[row[len(row) - 1].upper().replace(' ', '_')]

        # the group cycle hasn't been determined yet
        self.provider_group = None
        self.consumer_group = None

    # set this group's provider group
    def set_provider(self, provider_group):
        self.provider_group = provider_group

    # set this group's consumer group
    def set_consumer(self, consumer_group):
        self.consumer_group = consumer_group

    # get the first names of the group members (for email sending purposes)
    def get_first_names(self):
        if len(self.members) == 1:
            return str(self.members[0].first_name)
        elif len(self.members) == 2:
            return str(self.members[0].first_name) + ' and ' + str(self.members[1].first_name)
        else:
            out = ''
            for i in range(0, len(self.members)):
                if i < len(self.members) - 1:
                    out += str(self.members[i].first_name) + ', '
                else:
                    out += 'and ' + str(self.members[i].first_name)
            return out

    # get the emails of the group members (for email sending purposes)
    def get_emails(self):
        return [m.email for m in self.members]

    # given the message template, generate the filled in email message to send
    def fill_in_message(self, message):
        return message.replace('$group_first_names', self.get_first_names())\
            .replace('$recipients_full_info', str(self.consumer_group))\
            .replace('$senders_full_info', str(self.provider_group))

    # extensional equality for groups
    def __eq__(self, other):
        return self.grade == other.grade

    # lt for comparisons when sorting lists of groups
    def __lt__(self, other):
        return self.grade < other.grade

    # gt for comparisons when sorting lists of groups
    def __gt__(self, other):
        return self.grade > other.grade

    # toString for groups
    def __str__(self):
        # if the group is one person, simple case
        if len(self.members) == 1:
            out = str(self.members[0])
        elif len(self.members) == 2:
            out = str(self.members[0]) + ' and ' + str(self.members[1])
        else:
            out = ''

            for i in range(0, len(self.members)):
                if i < len(self.members) - 1:
                    out += str(self.members[i]) + ', '
                else:
                    out += 'and ' + str(self.members[i])

        return out
