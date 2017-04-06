<h1>OOD (HW8) Group Pairing Tool</h1>
A script to read CSV files, create group pairings, and automate the process of sending emails.
<br/><br/>

Groups are ordered from best to worst, and assignments are given out such that the best group gets the worst group's code, the second best group get's the second worst group's code and so on.
<br/><br/>

Once all pairings are generated, the script will ask for email credentials for the sender account, and notify all groups of who they need to send their code to (their "downstream customers") and from whom they'll be receiving their code (their "upstream providers").
<br/><br/>

<b>In order to specify a message (aka the email body) to the intended recipients, please read the section below on properly formatting the group data csv file.</b>
<br/><br/>

So far I've only developed the ability to send one email with prompts as to sender, recipient, etc, but that's probably the hardest part, more to come soon.

<h1>Notes</h1>
<ul>
    <li>The script assumes you input things correctly, using proper file structure outline below. If you mess something up, there aren't too many prompts, just start again, as it won't do any sort of input checking or re-prompting.</li>
    <li>Only servers that use SSL/TLS are supported at this time.</li>
    <li>If you're using regular/personal Gmail to send messages out, you need to enable unsafe apps to use your account (or potentially create an application password, if that functionality still exists).</li>
    <li>If you're using HuskyMail, make sure that you have created a Gmail app password for your account, otherwise it's impossible to authenticate.</li>
    <li>If you run this project in PyCharm, the password input <b>IS NOT HIDDEN</b>, as the IDE has a different TTY than getpass.</li>
    <li>It's super easy to copy-paste all this data (from wherever) into Excel and export it as a CSV. I would (and can) deal with XLSX files, but the xlrd library for Python is significantly slower than the built in CSV library and it doesn't come with stock Python.</li>
</ul>

<h1>Usage (theoretical)</h1>
Once completed, these are the two ways you will be able to run the script:
<ol>
    <li>python group_tool.py [group data csv file]</li>
    This option will <b><i>only</i></b> prompt you for email credentials, and send the email afterwards.
    <li>python group_tool.py [group data csv file] [email creds file]</li>
    This option is completely automated after cred file setup. When using this option, be sure to see below for more details about how to properly create your creds file.
</ol>
Please see the below section before proceeding.

<h1>Group Data CSV File Formatting</h1>
This file must be formatted relatively specifically, otherwise the script won't work. Assuming that you create the data file in Excel (and later on export as CSV), formatting goes as follows:
   <ul>
        <li>Cell A1 should contain the email body. Use escape sequences like \n and \t for a newline and tab, respectively.</li>
        <li>All subsequent rows are as follows:
            <ul>
                <li>The first columns contains the email addresses of the group members.</li>
                <li>The last column contains the group's overall grade</li>
            </ul>
        </li>
   </ul>

<h1>Creating the user credentials file</h1>
If you find yourself needing to run this script a lot and don't feel like typing in your name, email address, and password every time, here's how you can create a reusable credential file.
<ol>Steps:
    <li>Create a new text file with whatever name (and extension) you want.</li>
    <li>On the first line, put the name you'd like to appear in the email as the sender (e.g., John Smith).</li>
     <li>On the second line, put your email address.</li>
     <li>On the third line, put your base64 encoded email password, which can be generated as follows (in a Python shell or script):</li><br/>
     For Python2:<br/>
     >>> 'password text here'.encode('base64')<br/>
     >>> 'cGFzc3dvcmQgdGV4dCBoZXJl' &lt;-- use this value, without quotes<br/><br/>
     For Python3, however, things get a bit more complex:<br/>
     >>> import base64&lt;-- this actually works, oddly enough<br/>
     >>> base64.b64encode(bytes('password text here', 'utf-8')) <br/>
     >>> b'cGFzc3dvcmQgdGV4dCBoZXJl' &lt;-- use this value, without the quotes or the preceeding 'b'.<br/><br/>
     I'm choosing to use base64 here, as storing your email password in plaintext is usually bad practice. Unfortunately, it's impossible to send hashed/encrypted email passwords with Python's built-in smtp library, so obfuscation is the next best thing.<br/><br/>
     <li>That's it!</li>
</ol>

