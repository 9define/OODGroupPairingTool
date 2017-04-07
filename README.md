<h1>OOD (HW8) Group Pairing Tool</h1>
A script to read CSV files, create group pairings, and automate the
process of sending emails.
<br/><br/>

Groups are ordered from best to worst, and assignments are given out
such that the best group gets the worst group's code, the second best group get's the second worst group's code and so on.
<br/><br/>

The script will first ask for email credentials for the sender account,
then generate all group pairings and notify all groups of who they
need to send their code to (their "downstream customers"), and from
whom they'll be receiving code (their "upstream providers").
<br/><br/>

<b>In order to specify a message (aka the email body) to the intended
recipients, please read the section below on properly formatting the
group data csv file.</b>
<br/><br/>

<h1>Notes</h1>
<ul>
    <li>The script assumes you input things correctly, using proper
    file structure outline below. If you mess something up, there
    aren't too many prompts, just start again, as it won't do any
    sort of input checking or re-prompting.</li>
    <li>Only servers that use SSL/TLS are supported at this time.</li>
    <li>If you're using regular/personal Gmail to send messages out,
    you need to enable unsafe apps to use your account (or potentially
    create an application password, if that functionality still
    exists).</li>
    <li>If you're using HuskyMail, make sure that you have created a
    Gmail app password for your account, otherwise it's impossible to
    authenticate.</li>
    <li>If you run this project in PyCharm, the password input <b>IS
    NOT HIDDEN</b>, as the IDE has a different TTY than getpass.</li>

</ul>

<h1>Usage</h1>
<pre>usage: grouping_tool.py [-h] [--server SERVER] [--creds CREDS]
CSVfile<br/>
positional arguments:
  CSVfile     The CSV file containing the email message to send out and
                   all groups with their evaluations. See the project
                   README
                   for more info on how to format this file.<br/>
optional arguments:
  -h, --help       show this help message and exit
  --server SERVER  If you wish to use a non-Gmail email server.
  --creds CREDS    Custom user credentials file, if you're going to be using
                   this script a lot and don't want to repeatedly enter your
                   email server info.</pre>
Please see the below section before proceeding.</p>

<h1>Group Data CSV File Formatting</h1>
This file must be formatted relatively specifically, otherwise the
script won't work. Assuming that you create the data file in Excel (and
later on export as CSV), formatting goes as follows:
   <ul>
        <li>Cell A1 should contain the email body. Use \n for a newline,
        Write $senders_first_names, $recipients_first_names,
        $senders_full_info, and $recipients_full_info to expand to the
        relevant info when sending the info.</li>
        <li>All subsequent rows are as follows:
            <ul>
                <li>The first n columns contain the email addresses of
                the group members, where n is the number of group
                members.</li>
                <li>The last column contains the group's overall
                evaluation (Very Good, Good, Fair, Bad)</li>
            </ul>
        </li>
   </ul>
   See the example csv file in the test_data directory for more.

<h1>Creating the user credentials file</h1>
If you find yourself needing to run this script a lot and don't feel
like typing in your name, email address, and password every time,
here's how you can create a reusable credential file.
<ol>Steps:
    <li>Create a new text file with whatever name (and extension) you
    want.</li>
    <li>On the first line, put the name you'd like to appear in the
    email as the sender (e.g., John Smith).</li>
     <li>On the second line, put your email address.</li>
     <li>On the third line, put your base64 encoded email password,
     which can be generated as follows (in a Python shell or script):
     </li><br/>
     For Python2:<br/>
     <pre>
     >>> 'password text here'.encode('base64')
     >>> 'cGFzc3dvcmQgdGV4dCBoZXJl' &lt;-- use this value, without
     quotes</pre><br/>
     For Python3, however, things get a bit more complex:<br/>
     <pre>
     >>> import base64
     >>> base64.b64encode(bytes('password text here', 'utf-8'))
     >>> b'cGFzc3dvcmQgdGV4dCBoZXJl' &lt;-- use this value, without the
     quotes or the preceeding 'b'.</pre><br/>
     I'm choosing to use base64 here, as storing your email password in
     plaintext is usually bad practice. Unfortunately, it's impossible
     to send hashed/encrypted email passwords with Python's built-in
     smtp libs (or anything else really).
</ol>
