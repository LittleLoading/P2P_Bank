# Changelog

## 2026-01-26 - David Houra
* shared repo init

## 2026-01-26 - Nikola Poláchová
* Server.py for TCP server connection.
* BankWatcher.py some basic UI for monitoring bank actions. 
* Response.py for returning responses (success/error).
* JsonParser.py reads from json files (code from previous project).
* A bit of ReadMe.
* Class Response - methods success() and error().

## 2026-01-27 - David
* Copied database.py from a previous project and implemented auto-initialization of tables upon application startup
* Added BankCode.py to get host computers's IP address
* Connected BankCode.py Server.py and main 
* Added BankController.py to process commands with PUTTY terminal
* MySQL schema and automated init databse setup procedures in database.py - auto init from previous project
* Added AccountCreate.py with automatic free account number selection and setting balance to 0
* Added AccountDeposit.py and AccountWithdrawal.py, validation input format and transactions to database
* Added AccountBalance.py and AccountRemove.py and their logic and checking nonexistent accounts
* Added BankAmount and BankNumber with logic, to moniture amount of money in bank and number of clients
* Implemented proxy fucntions by refactoring AD, AW, AB and editing Client.py to connect to different ip banks and sending commands and retrieving response
* Added Scanner.py to scan availible banks in the network and on correct ports -> added RobberyPlan logic

## 2026-01-27 - Nikola Poláchová
* BankWatcher adding more format to the window. Split it into two, logs and list of clients connected.
* BankWatcher docs for method update_user_list
* Server added needed attributes, like ui, timeout and list of active users. Completely rewrote method handle_client. Most logic remains same.
* JsonParser changed method to be more usable.

## 2026-01-28
* Fixed bugs with databse
* Updated Readme file