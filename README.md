# Automated Syslog Message Filtering by Severity (AP3)

## Project Overview

This is a **Python-based network automation work** designed to **fetch syslog messages of a network device filtered by severity levels**, primarily using the **Netmiko** and **Regular Expression (re)** library.
Netmiko is a Python library that automates network devices over **SSH and Telnet**. It is built on top of **Paramiko**, providing device-specific features and greater control for network automation tasks.
**re** is a Python library used for pattern matching and manipulation of strings, allowing searching, matching, splitting, and replacing text based on specified patterns.

A custom module named "sysmodule" is **created** which **fetches** syslog messages of a particular date or current date from a network device or a syslog server and **mails** the syslog message of a specific level (based on severity) to network admins or management.
The script is automated using **cron**, making it suitable for **real-world NOC-style monitoring scenarios**.
The script also includes exception handling for SSH timeouts, Authentication failures, Unreachable devices, SMTP connection issues.

---

## Objectives

* Automate syslog message fetching filtered by severity levels.
* Store device severity-level specific logs in specific text files.
* Send email notifications if a severity level of 0-4 is detected.
* No duplicate alarms and emails.
* Gracefully handle SSH, timeout, and authentication failures.
* Run fully unattended using **cron jobs**.

---

## Technologies Used

* **Python 3**
* **Netmiko** – SSH connection, sending commands, receiving output
* **re** - Regular expression, to fetch specific level syslog messages
* **smtplib** – Connecting to SMTP server and sending email
* **email.message** - Email formatting
* **time** - For timestamps
* **os** - Specify file locations
* **Linux Cron** – Task scheduling

---

## Project Structure 
```
Automation_Project_3/
|
├── core_lvl0.py
├── core_lvl3.py
├── core_lvl4.py
├── core_lvl8.py
├── sysmodule.py
│
├── Photos/
│
└── README.md
```
---

## How the Script Works

### sysmodule (The custom module)

The module **consists** of a class named "Devices" that **introduces** some attributes and methods for its objects:

1. Six instance-level attributes (dev_name, dev_type, ip_addr, user, pas, sec)
2. A function named "timming" with only self as parameter and **uses** regex to fetch the Month and Date format and return Month and Date
3. Four functions (lvl4_pattern, lvl3_pattern, lvl0_pattern, lvl8_pattern) with only self as parameter and **return** a pattern object of a specific level to be used.
4. Four **functions** (engine_lvl4, engine_lvl3, engine_lvl0, engine_lvl8) with **only** self parameter. This is the main engine of the code.

### Device specific scripts filtered by severity level of syslog:

These are the device specific scripts in which the "sysmodule" module is imported. In this script a "Devices" class object is created and specific object methods are executed to fetch the syslog messages filtered by severity level.

The working of the main engine of the code is stated below:

1. First it **connects** to the device via SSH using Netmiko ConnectHandler
2. It calls the timming function and **keeps** the value in a variable named "t0"
3. It calls the lvl()_pattern function and **keeps** the pattern object in a variable named "syslogpat"
4. It sends the command "sh log | i Month Date" and **stores** the output (string) in a variable named "syslog"
5. It **disconnects** the SSH session with the device.
6. It compares the regex pattern with the content of syslog variable using re.findall() method and **stores** the output (List(Tuples) → as we have groups in our regex pattern) in a variable named "rawout"
7. It creates an empty list **named** "syslist"
8. Then it uses a for loop to convert all the tuples **inside** the rawout list and convert them to strings using the join() method and **stores** them in a variable named "cookedout" and append the values of cookedout in the empty list **named** syslist (List[strings]).
9. It converts the syslist list into a set using type conversion and **keeps** the output in a variable called "content" (set{strings})
   → Since **it's** a set there will be no duplicate syslog messages
10. Using the join function it converts the syslist list into a string with "\n" (new line) as **separator** and keeps the output in a variable called "content_str" (string)
11. Using with, it opens a file named {self.dev_name}_l()_logs.txt in a+ mode as logs (string) (At first when the file **doesn't** exist, it creates one), it then moves the cursor to position 0. It then reads the file using the read() method and then **converts** the content into a list using splitlines() method and then converts that list to a set using type conversion. The output is then stored into a variable called "counter" (set{strings})
12. Now the script has two sets, content and counter.
    It then subtracts the contents in the "counter" set from the "content" set and **stores** the difference in a variable named "newlogs" (set{strings})
    Case 0: Initially (1st time only) the counter set will be empty, so newlogs variable will store all the contents in the content set.
    Generally: In the rest of the time newlogs set will store only the new syslog messages which came new from the devices.
    → This is done only to reduce duplicate emailing and storing of syslog messages.
13. Using join() method it converts the newlogs set into a string **separated** by "\n" and stores it in a variable named "newlogs_str" (string)
14. Then if newlogs is truthy, then using with open a file named {self.dev_name} in w mode as "sysmsg" and write the newlogs_str content into it. After that it **mails** the contents of newlogs_str to the **respective** admins and management → This file **stores** only the new syslog messages, not all.
    If newlogs is falsy it does nothing. Hence no duplicate emailing and storing of syslog messages.
15. Using with it again opens the file named {self.dev_name}_l()_logs.txt but this time in w mode as logs and writes all the content of "content_str" variable.

---

## Challenges Faced 

### 1. Confusion with opening file with different modes:

Due to not using the correct mode to open, read, write, and append a file, the script was not yielding the desired output.
To overcome this issue, I **revisited** the Python file modes concepts.

### 2. Attempting to read a file outside the "with" block.

Which was throwing an error stating "File not readable".
To overcome this error I revised the with block concept and realized the core feature of with block, that with block automatically **closes** the file and all the operations on the file need to be done inside the block.

### 3. Cursor positioning issue with file.read() method.

file.read(n) reads the first n lines in the file (leaves the cursor at the current position).
So if we use:

```
a = file.read()
b = file.read()
```

The first file.read() reads the whole file and leaves the cursor at the end of the file.
After that the second file.read() starts at the end of the file resulting in nothing to read (empty output).

To overcome this issue, I used the file.seek(n) method.

---

## Future Enhancements

* Packet capture and traffic analyzing (Integrating Wireshark)
* Integration of API to retrieve interface and routing data (Restconf/Netconf)
* Integrating alarm system for actual NOC environments
* Integrating Grafana

---

## Author:

Raj Pallab Deka
💼 Current Role: [Network Field Engineer], [Coforge], [Under Government NIC-NKN Project]
🌐 Network Automation & Cybersecurity Enthusiast
🔗 GitHub: [https://github.com/RajPallabDeka](https://github.com/RajPallabDeka)
🔗 LinkedIn: [https://www.linkedin.com/in/your-profile](https://www.linkedin.com/in/your-profile)

---

⭐ If you like this project, consider giving the repository a star — it helps the profile stand out!
