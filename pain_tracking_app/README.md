Application name: Pain Tracker
Installer: installer.py

Pain Tracker:
The application consists of 3 screens, the home screens makes you choose Pain entry or Medication entry. For pain entry you have to specify which body location(s) is painful, and the degree of the pain.
For medication you have to choose which medicine you have used associated with the dosage.

Installer
The installer populate the locations and the medicines you will be able to choose from.

Know Issues:
There is a bug that the app does not record the pain degree and the medicine dosage for each location and medicine correctly.

Build and Running:
First you have to create empty database before using the installer
to do so you have to access MySQL from the console by using 

mysql --user=root -p

then create new data base by using

create database pain_tracking;

make sure that the database was created by using

show database;

then you have to run the installer up to populate the data before using the tracker. After running the installer you can use the app. 
