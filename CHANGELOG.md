# Changelog

## 2026-01-26 - Nikola Poláchová
* Server.py for TCP server connection.
* BankWatcher.py some basic UI for monitoring bank actions. 
* Response.py for returning responses (success/error).
* JsonParser.py reads from json files (code from previous project).
* A bit of ReadMe.
* Class Response - methods success() and error().

## 2026-01-27 - Nikola Poláchová
* BankWatcher adding more format to the window. Split it into two, logs and list of clients connected.
* BankWatcher docs for method update_user_list
* Server added needed attributes, like ui, timeout and list of active users. Completely rewrote method handle_client. Most logic remains same.

