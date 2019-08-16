import socket
import twitch
import time

SERVER = "irc.chat.twitch.tv"
PORT = 6667
PASS = "oauth:164qv5hw70adstvlkikg2uca0f7cw4"
BOT = "myrustybanana"
CHANNEL = "myrustybanana"
OWNER = "myrustybanana"
irc = socket.socket()
irc.connect((SERVER, PORT))
irc.send((  "PASS " + PASS + "\n" +
            "NICK " + BOT + "\n" +
            "JOIN #" + CHANNEL + "\n").encode())
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

cmds = [1, 2, 3, 4, 5, 6, 7]
cmds = [str(x) for x in cmds]
# Parses the input cmdString and maps it to a command character
# This is for cases where commands are not characters: e.g. "STOP" maps to 'x'
def parseCmd(cmdString):
    if cmdString in cmds:
        return cmdString
    else:
        return None

# Sends the command over to the couch controller program
# TODO
def sendCmd(cmd):
    print("Sending command: %s" % cmd)
    return

joinchat()


# TODO implement taking a consensus for each unique vote on what to do
while True:
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
            print(user + " : " + message)
            cmd = parseCmd(message)
            if cmd:
                sendCmd(cmd)

        if "PING" in line and Console(line):
            msgg = "PONG tmi.twitch.tv\r\n".encode()
            irc.send(msgg)
            print(msgg)
            continue
        time.sleep(0.05) # Sleep in seconds 
