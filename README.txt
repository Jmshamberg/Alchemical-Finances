Alchemical Finances - Manual Personal Finances
Alpha Version 1.7 - 20200909
Beaker Labs llc. [Comming? Maybe? Different Name?]

------------------------------------------------------------------
Purpose to Developer:
------------------------------------------------------------------
The information provided in the next section will outline the functional purpose of the project and explain the original inspiration for the overall program. The purpose
behind the project for me the developer is to use this program to teach myself to code in python and the associated skills. Many aspects of the ledgers developed has steamed 
from either a need to learn a new skill, or in an attempt to put a new skill into practice. This project provides a great canvas to try many different skills such as
--- General Python Code and OOP
--- SQLlite
--- Numpy, Pandas, Matplotlib
--- PyQt5
--- Reportlab (Pdf Generator)
--- and more.

------------------------------------------------------------------
Description / Purpose of the Project:
------------------------------------------------------------------
--- The project is designed to replace the use of Microsoft Excel for the purposes of tracking a users Personal Finances 
without the need to move to a program like Mint.com / Quicken / Personal Capital ect. This provides a few benefits such as:
--- -- [A] No 2nd/3rd party Data Mining of user information
--- -- [B] All Data is currently stored on the Users Computer only 
--- -- [C] No Automatically filled ledgers
--- -- [D] Ability to attached Invoices/Receipts to all transactions. 
--- -- [#] Future features are planned [See Bottom for mini pipeline]
--- The program is built on the concept that people understand their finances better when they interact with them rather than watch them.
Having the user manually input transactions helps them pay attention to their exspenses and helps them feel in control. The future addition of
graphs/generated budgets will reinforce this. [Generated budgets will be built from past input data by user selected Categories. Then allow the user to build the following months budget]

------------------------------------------------------------------
Request to Testers
------------------------------------------------------------------
--- Please break my program! Find where my coding needs some work and could benefit from some additional attention. Some things to consider
---  -- - Test User Inputs, Creating New Accounts, Posting/Selecting/Updating/Deleting Transactions, account details ect. Basically everything at this point.
--- Critique the design and concept. At heart the project is meant for me to replace excel but I would like to share to those interested.

------------------------------------------------------------------
Pre-Requisites:
------------------------------------------------------------------
--- Current Design should not require the installation of any additional software. The .exe file should take work independandtly 
--- PyQt5 5.11.2 and Python 3.8 used to code the program

------------------------------------------------------------------
Installation 
------------------------------------------------------------------
Python
--- 1 -- Download all files in the repository. 
--- 2 -- Load the program from the Executable.pyw file.
---   -- -- Be sure to check the Requirements.txt for all associated dependancies required for this program to opperate properly.

------------------------------------------------------------------
Create New User
------------------------------------------------------------------
--- 1 -- Click New Profile
--- 2 -- User Profile is not case sensitive. Everything will be made lowercase.
--- 3 -- Password must be more than 6 characters long and must be alphanumeric. 
---   -- -- Unallowed symbols: ["~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "=", ":",
                     		"+", "<", "?", ";", "'", "[", "]", "{", "}", '"', "-", ".", ","]
--- 4 -- Submit new profile
--- 5 -- Cancel out of the new profile screen
--- 6 -- Login
  
------------------------------------------------------------------
User Manual
------------------------------------------------------------------
--- The file USER_MANUAL.pdf can be found in the same directory as this README.txt.
--- The User Manual will include images and full instructions/conceptual comments about the program.  
--- The User Manual will be accessable from within the program as well. 
   
------------------------------------------------------------------
Data Storage
------------------------------------------------------------------
--- All User information will be stored locally on the system in the directory the program was installed on. All files will be created within the "dist/Executable" directory
--- if you move the program be sure to move the data and receipt files as well or the program will create new ones.
--- User data is stored in the data directory
--- Receipts are stored in the Receipts directory by profile name then account ledger

  
------------------------------------------------------------------
Pipeline Production - Overview room to expand/Change
------------------------------------------------------------------	 
~~ Obsolete: Project development has mostly cooled down. Still many things that an be done and implimented.
~~ Focus has shifted to learning Data Science. Which would be useful in upgrades to this program. Like Graphing Category Spending.

--- 1  -- Equity and Retirement Ledger [COMPLETED]
--- 2  -- Summary Tab [COMPLETED]
---    -- Archive Tab [COMPLETED]
---    -- About Tab [COMPLETED]
---    -- User Manual [COMPLETED]
--- 3  -- Saving databases - Program Creates a temp file, then saves over the primary .db File
--- 4  -- Generating Printable Reports [COMPLETED - Summary Report]
--- 5  -- CSV exporting
--- 6  -- User Data Back-up
--- 7  -- Ledger to track Large Exspense Purchases
--- 8  -- Ledger to track Long Term Projects
--- 9  -- Work on Ui to adjust to user display. [Completed?]
--- 10  -- Rebrand website to destribute program
       -- -- Purchase Commercial Version of PyQt5
       -- -- Find Initial Beta Testers
       -- -- Will make Visual instructions
	   -- -- Include Blog
	   -- -- Comparison to Mint.com and Personal Capital (Maybe Quicken)
--- 11 -- Graphs for budgeting  [Inprogress] and Net Worth Tracking  [COMPLETED]
--- 12 -- Expand Receipt Display to have a few more features
--- 13 -- Encryption
--- 14 -- User E-mail Address to reset lost passwords
--- 15 -- Explore taking the program to server/cloud storage
--- 16 -- Explore E-mail notifications
       -- -- User Set reminders
	   -- -- Bills Due? Maintence Due? ect?
--- 17 -- Explore Andriod app

-- Maybe -- Webscrapping some Equity Data -- Unsure at this time if i will dive into webscrapping [Found API for Equity]
-- Maybe -- Ledger to track subscriptions
