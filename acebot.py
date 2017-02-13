
# coding: utf-8

# # AceBot
# ### This program is for a slack bot called AceBot

# The first part of this program will import the needed librarys and set the required IDs.  The BOT_ID and the SLACK_BOT_TOKEN have already been put into my virtualenv. 

# In[ ]:

import os
import time
from slackclient import SlackClient

BOT_ID = os.environ.get("BOT_ID")

AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


# Create a function that check if messages are directed at the bot.  Return none if @AceBot is not used within message.  If it is used then return the text, channel and the timestamp of the message. 

# In[ ]:

def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                return output['text'].split(AT_BOT)[1].strip().lower(), output['channel'], output['ts']
    return None, None, None


# Create a function that handles the bots responses back to the channel.  First it checks to see if certain words, phrases are used.  Depending on the logic statements it will load an answer into the response and post back to channel at the end. (Should maye split this into multiple functions or hold the data in a datasource....)

# In[ ]:

def handle_command(command, channel, ts):	
    response = "We still need to add this command"
    if command.startswith('show karik'):
        response = "https://ibb.co/goaOgF"

    elif command.startswith('ace'):
        response = ace_song()

    elif command.startswith('web'):
        response = r"\\dom1\data\hq\102pf\shared\group_lcdshd2\analytical services\cicfas\teams\ace\projects\20 ddd frontpage - discovery-alpha\datainput\index.html"
    elif command.startswith('file link'):
        response = r"\\dom1\data\hq\102pf\shared\group_lcdshd2\analytical services\cicfas\teams\ace" + "\\" + command[10:]
    elif command =="tumbleweed":
        response = "https://media.giphy.com/media/5x89XRx3sBZFC/giphy.gif"

    elif command == "doc library":
        response = "coding doc, folder doc, learn python, learn R, data security, software doc"
    elif command == "coding doc":
        response = "https://docs.google.com/document/d/1bqVkH9k4Nv4Av_-Lvewcl6un_aedOkK6v4s7Nm0V_Qk/edit"
    elif command =="folder doc":
        response = "https://docs.google.com/document/d/1BL57inTbBxukVJ_ti35L7fz_Un1WYybSkRi8UKEb1tA/edit#heading=h.6v5ejfe0vgdg"
    elif command == "learn python":
        response = "https://docs.google.com/document/d/1aAeiiXhrAVZPVrbKK3k6ELxbZyeKuTHnr2-pCIyAtfQ/edit#heading=h.dqyv71zc3gzp"
    elif command =="learn R":
        response = "https://docs.google.com/document/d/1R4hBMf26T9HEnCdVz56PpZhwiCv5RhberYL3BxOSKsA/edit"
    elif command == "software doc":
        response = "https://docs.google.com/document/d/1avLqSnh6cB5FFktr1PZZbWTstkuWlGOHGBLeREA_ow4/edit?pli=1"
    elif command.startswith('data security'):
        response = r"\\dom1\data\hq\102pf\shared\group_lcdshd2\analytical services\cicfas\teams\ace\policies\20160712 data security and the macbook platform final.doc"

    elif 'dsh' in command or 'dash' in command:
        response = "AceBot does not recognise this team name.  Please use 'ACE' or 'the team formerly known as ACE' when talking to me"

    elif 'pie chart' in command:
        response = "AceBot is disgusted by pie charts.  They are held in the same regard as the name DaSH."

    elif 'weather' in command:
        response = "It is always sunny in the land of ACE."


    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)


# This function outputs the ACE song.  It put out the three letter and then sends the last command back to the main function to output.

# In[ ]:

def ace_song():
    slack_client.api_call("reactions.add", channel=channel, timestamp=ts, name="ace")
    slack_client.api_call("reactions.add", channel=channel, timestamp=ts, name="thumbsup")

    slack_client.api_call("chat.postMessage", channel=channel, text="Give me an A", as_user=True)
    time.sleep(1)
    slack_client.api_call("chat.postMessage", channel=channel, text="Give me a C", as_user=True)
    time.sleep(1)
    slack_client.api_call("chat.postMessage", channel=channel, text="Give me an E", as_user=True)
    time.sleep(1)
    return "I regret everything"


# Load the bot to slack and print a message if successful or not.  Also run a loop that will run the two main functions (checking if a message is directed at AceBot and responding to any messages).

# In[ ]:

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1
    if slack_client.rtm_connect():
        print("AceBot connected and running!")
        while True:
            command, channel, ts = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel, ts)
            time.sleep(READ_WEBSOCKET_DELAY)

    else:
        print("Connection failed.  Invalid Slack token or bot ID?")
