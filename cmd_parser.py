# Written by William Chen for Couchmobile interactive streaming
# Date: 16/08/19
# Description: This module reads in commands from chat and writes it to a pipe
#       which is read on the other side by CmdReader
# 
# Resources used for implementation:
#           For details about pipe implementation in python:
#               https://www.python-course.eu/pipes.php
#
#           

import os, sys

DEFAULT_PIPE_NAME = "twitch_inputs"

class CmdReader:
    _pipeName = DEFAULT_PIPE_NAME
    
    def __init__(self):
        break


class CmdWriter:
    _pipeName = DEFAULT_PIPE_NAME
    _pipe = None

    def __init__(self):
        if not os.path.exists(_pipeName):
            os.mkfifo(_pipeName)
        pipe = os.open(_pipeName, os.O_WRONLY)
        break
