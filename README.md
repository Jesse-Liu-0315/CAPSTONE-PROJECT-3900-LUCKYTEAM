# capstone-project-3900h18bluckyteam

capstone-project-3900h18bluckyteam created by GitHub Classroom

(Lubuntu 20.4.1 LTS virtual machine image in the VirtualBox 6.1.44) 

Remember!!! Everytime open a new terminal you always run the code: 

$ sudo su 

$ cd 


6.1Checking the MySQL  

Firstly, check if the computer has the MySQL server. Open a terminal. 

Use the code: 

$ mysql -V 

If no version is displayed, it means that there is no MySQL on this computer. 
Then you need to install the MySQL. 

1.Update package list and upgrade packages: 

$ sudo apt-get update

$ sudo apt-get upgrade 

2.Install the MySQL package: 

$ sudo apt-get install mysql-server 

3.During the installation, you will be prompted to set a root password for MySQL. You should set the password as ‘123456’. 

$ ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '123456'; 

4.When installation was done, you can use the MySQL by using the command: 

$ mysql -uroot -p 

Then enter ‘123456’ 

5.Create the database by running: 

$ create database MOVIEFINDER; 


6.2 Checking the Nodejs 

Firstly, we need to install nodejs by entering: 

$ sudo apt install nodejs 

$ sudo apt install npm

$ sudo npm i -g yarn 

After these progress, you should check the nodejs version by entering: 

$ node -v 

If the version not >= 16.14.2 

You should run: 

$ npm install -g n 

$ n stable 

Then close the terminal, open the terminal again. Now check the nodejs version again. 
It will change to newest version. 


6.3 Checking the Python libraries. 

Before starting the backend, you should check if the python libraries is all installed. 

Just run: 

$ cd ~/capstone-project-3900h18bluckyteam 

$ pip install -r requirements.txt 

Then it will be ok. 


6.4 Starting the Backend:  

Open a new terminal, clone the project repository to the directory.  

~/capstone-project-3900h18bluckyteam. 

Next, use the commands:  

$ cd ~/capstone-project-3900h18bluckyteam/backend/src 

$ python3 server.py

It will start the backend. 


6.5 Starting the Frontend:  

Once the backend is running, open a new terminal.

run the frontend server by entering the next set of commands: 

$ cd ~/capstone-project-3900-h18b-luckyteam/frontend 

$ yarn install 

$ yarn start 

If you firstly using the code, you should enter the  

$ yarn install

Then every time you use it, you just need to type:

$ yarn start

At last, open the Firefox browser, go to the “http://localhost:3000”, then you can use the project well. 


6.6 Emergency 

When you newly open the backend and frontend, you will find that the word logout appears in the upper right corner of the page, and you cannot log out. In this case, the logout operation was not performed after the backend was forced, resulting in token invalidation. For details, see 6.6 Emergency in the report.
