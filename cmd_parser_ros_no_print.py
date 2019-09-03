import socket
#import twitch
import time
import datetime

# Config for commands to receive from chat (left side) and send to couch (right)
# "chat command" : "couch command"
cmds = {'1' :'1',
        '2' :'2',
        '3' :'3',
        '4' :'4',
        '5' :'5',
        '6' :'6',
        '7' :'7'
        }

# Config for admin commands by twitch chat
adminUsers = ["exactlyestimated"]
adminCmds = ["killbot", "killcouch"]

SERVER = "irc.chat.twitch.tv"
PORT = 6667
PASS = "oauth:zfi31yaqrdi4980mhq2hvs1xjyad0u"
BOT = "exactlyestimated"
CHANNEL = "exactlyestimated"
OWNER = "exactlyestimated"
irc = socket.socket()
irc.connect((SERVER, PORT))
irc.send((  "PASS " + PASS + "\n" +
            "NICK " + BOT + "\n" +
            "JOIN #" + CHANNEL + "\n").encode())
irc.settimeout(5)
def joinchat():
    Loading = True
    while Loading:
        readbuffer_join = irc.recv(1024)
        readbuffer_join = readbuffer_join.decode()
        for line in readbuffer_join.split("\n")[0:-1]:
            print(line)
            Loading = loadingComplete(line)
def loadingComplete(line):
    if ("End of /NAMES list" in line):
        print("Bot has joined" + CHANNEL + "'s Channel")
        sendMessage(irc, "Chat Room Joined")
        return False
    else:
        return True
def sendMessage(irc, message):
    messageTemp = "PRIVMSG #" + CHANNEL + " :" + message
    irc.send((messageTemp + "\n").encode())
def getUser(line):
    separate = line.split(":", 2)
    user = separate[1].split("!", 1)[0]
    return user
def getMessage(line):
    try:
        message = (line.split(":", 2))[2]
    except:
        message = ""
    return message
def Console(line):
    if "PRIVMSG" in line:
        return False
    else:
        return True

# Parses the input cmdString and maps it to a command character
# This is for cases where commands are not characters: e.g. "STOP" maps to 'x'
def parseCmd(cmdString):
    cmd = None
    try:
        cmd = cmds[cmdString]
    except KeyError:
        return None
    else:
        return cmd

# Sends the command over to the couch controller program
# TODO
def sendCmd(cmd):
    print("Sending command: %s" % cmd)
    return

joinchat()

# in 5 second interval:
    # tally all the commands
    # store their counts in a dictinary
# after 5 seconds
    # find max tally
    # send message with the max tally
def groupthink(first_message):
    tally = {}
    tally[first_message] = 1
    print(first_message)
    end = datetime.datetime.now() + datetime.timedelta(seconds=10)
    while datetime.datetime.now() <= end:
        message = ""
        try:
            readbuffer = irc.recv(1024).decode()
        except:
            readbuffer = ""
        for line in readbuffer.split("\r\n"):
            if line == "":
                continue
            else:
                user = getUser(line)
                message = getMessage(line)

            if "PING" in line and Console(line):
                msgg = "PONG tmi.twitch.tv\r\n".encode()
                irc.send(msgg)
                print(msgg)
                continue
        print(message)
        if message == "killbot":
            running = False
        elif message not in list(cmds.keys()):
            message = ""
        else:
            if message not in list(tally.keys()):
                tally[message] = 1
            else:
                tally[message] = tally[message] + 1
    max_value = max(list(tally.values()))
    max_key = None
    for key in list(tally.keys()):
        if tally[key] == max_value:
            max_key = key
    sendCmd(max_key)
    print(user + " : " + max_key)

# TODO implement taking a consensus for each unique vote on what to do
running = True
while running:
    try:
        readbuffer = irc.recv(1024).decode()
        for line in readbuffer.split("\r\n"):
            first_message = getMessage(line)

            if "PING" in line and Console(line):
                msgg = "PONG tmi.twitch.tv\r\n".encode()
                irc.send(msgg)
                print(msgg)
                continue
            else:
                groupthink(first_message)
    except:
        pass

    #time.sleep(0.05) # Sleep in seconds
