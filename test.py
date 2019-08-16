import socket, string

# Set all the variables necessary to connect to Twitch IRC
HOST = "irc.twitch.tv"
NICK = "***username***"
PORT = 6667
PASS = "oauth:PLACE_CODE_HERE"
readbuffer = ""
MODT = False

# Connecting to Twitch IRC by passing credentials and joining a certain channel
s = socket.socket()
s.connect((HOST, PORT))
s.send(("PASS " + PASS + "\r\n").encode())
s.send(("NICK " + NICK + "\r\n").encode())
s.send(("JOIN #YOURCHANNELNAME \r\n").encode())
