IRCQwitter-python
=================

IRCQwitter written in Python. Refer to IRCQwitter for more details

Commands that are build in:
*!join <channel> : tell the bot to join another channel
*!say <channel> <message> : tell the bot to say whatever
*!quo/!quoth : quote the specified message

-PYTHON'S SUPPORT FOR UNICODE
In order to make the bot not crash and burn when someone decides to send some random unicode into a channel,  you must set the irc library to decode using a less strict ruleset. Open up your favorite text editor and change the buffer.py file. Make the error variable = "replace" for an easy fix. In Arch, this file is locaed at /usr/lib/python3.x/site-packages/irc/buffer.py In Ubuntu, this file is located at /usr/local/lib/python3.x/dist-packages/irc/buffer.py.

