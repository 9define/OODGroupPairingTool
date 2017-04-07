

# define a group member/person
class Member(object):

    # create a new person from one of the fields in a csv file
    def __init__(self, csv_member_field):
	
        # split the csv field on spaces
        parts = csv_member_field.split(' ')

        # save the name
        self.first_name = ' '.join(parts[0:len(parts) - 2]) if len(parts) > 3 else parts[0]
        self.last_name = parts[len(parts) - 2]

        # save the email address
        self.email = parts[len(parts) - 1].replace('<', '').replace('>', '')

    # toString for a member
    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' (' + self.email + ')'
