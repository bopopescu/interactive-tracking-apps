Capstone project developed by Soft 161 Team 6.   The project includes an installer app which creates the combined database.  A provider app, which allows access to patient records stored from the caretaking, pain tracking apps and from Open MRS.
The caretaking app allows the user to record a patient’s observations recorded by a caretaker.  The pain tracking app allows the user to record pain severity and medications taken by a patient.   The provider app connects to the Open MRS database
and allows the user to sign in using the Open MRS ID.



Status of Installer APP:  As of now there are currently no issues with the installer app.



Running the Installer:  To run the installer, open the project in Pycharm, in the directory open the “Installer” folder.  Within the folder select “combined_database_installer.py”.  Click the green play button at the top left corner of the screen.  After it has run, a message should verify that the tables have been created at the bottom of the screen.



Know issues with the caretaking App: When entering a date of birth, in the observation window it will currently allow the user to enter any string, rather that the format “XX/XX/XX”.   Also, when a user creates an account and goes back to the account selection screen that account is not shown on the dropdown.  On the other hand, when you exit the app and restart it that account is then shown.
                                    Also the review screen does not work after a user hits submit in the observation entry screen.


Know issues with the pain tracking App:  It is the same issue with creating account and review screen as the caretaking App.



Know issues with the Provider App: The provider app currently only pulls data from the caretaking app, and does not retrieve data from pain tracking or OpenMRS. 

