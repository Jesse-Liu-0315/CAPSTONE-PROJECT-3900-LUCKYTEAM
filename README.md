# 🎬 Capstone Project – MovieFinder

This project is developed as part of a capstone course using a pre-configured Lubuntu virtual machine.

---

## 🖥️ Environment

- OS: Lubuntu 20.04.1 LTS
- VM: VirtualBox 6.1.44

⚠️ **Important**  
Every time you open a new terminal, run:

```bash
sudo su
cd
```

---

## ⚙️ 1. MySQL Setup

### 1.1 Check MySQL Installation

```bash
mysql -V
```

If no version is shown, install MySQL:

---

### 1.2 Install MySQL

```bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install mysql-server
```

---

### 1.3 Set Root Password

During installation, set:

Password: 123456

Then run:

```sql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '123456';
```

---

### 1.4 Start MySQL

```bash
mysql -uroot -p
# Enter password: 123456
```

---

### 1.5 Create Database

```sql
CREATE DATABASE MOVIEFINDER;
```

---

## 🟢 2. Node.js Setup

### 2.1 Install Node.js & Tools

```bash
sudo apt install nodejs
sudo apt install npm
sudo npm i -g yarn
```

---

### 2.2 Check Version

```bash
node -v
```

Required version:

>= 16.14.2

---

### 2.3 Upgrade Node.js (if needed)

```bash
npm install -g n
n stable
```

Then restart terminal and re-check version.

---

## 🐍 3. Python Dependencies

```bash
cd ~/capstone-project-3900h18bluckyteam
pip install -r requirements.txt
```

---

## 🚀 4. Run the Project

### 4.1 Start Backend

```bash
cd ~/capstone-project-3900h18bluckyteam/backend/src
python3 server.py
```

---

### 4.2 Start Frontend

```bash
cd ~/capstone-project-3900-h18b-luckyteam/frontend
yarn install   # First time only
yarn start
```

---

### 4.3 Access Application

Open browser:

http://localhost:3000

---

## ⚠️ 5. Notes

- Make sure backend is running before starting frontend
- Use separate terminals for backend and frontend

---

## 🆘 6. Troubleshooting

### Logout Issue

Problem:
- "Logout" button is visible but not working

Cause:
- Backend was forcefully stopped
- Token state became invalid

Solution:
- Restart backend
- Refresh browser
- Or re-login

Refer to section 6.6 Emergency in the report for more details.

---

## 📦 Project Structure

```
capstone-project/
├── backend/
├── frontend/
├── requirements.txt
└── README.md
```

---

## 👨‍💻 Author

Capstone Project Team – Lucky Team
