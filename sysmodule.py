import time 
import re
from netmiko import ConnectHandler
import os 
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException
from email.message import EmailMessage
import smtplib
#os.chdir("/home/dekaraj22/Desktop/Projects/Automation_Projects/Automation_Project_3/Outputs")


class Devices :
        def __init__(self ,dev_name,dev_type,ip_addr,user,pas,sec="None"):
                self.dev_name = dev_name
                self.dev_type = dev_type
                self.ip_addr = ip_addr
                self.user = user
                self.pas= pas
                self.sec = sec
        def  timming(self):
                tym= time.ctime()#ctime methond gives a time format of (Day Mon DD HH:MM:SS YYYY)
                tpattern = re.compile(r"\w{3}\s{1,2}\d{1,2}")
                t1  = re.findall(tpattern,tym) #output is a list 
                act_time = " ".join(t1) #join method is a method used to convert a list or a tuple into a string and the " " is the seperator .
                return act_time
        def lvl4_pattern(self):
                syslogpat4 = re.compile(r"(\d+:) (\*\w{3}\s{1,2}\d{1,2}) (\d{2}:\d{2}:\d{2}\.\d{3}:) (%\w+-4-\w*:) (.*)") # syslog pattern is a variable that stores the pattern we are searching for in the logs only (%FACILITY-SEVERITY-MNEMONIC: )
                return syslogpat4
        def lvl3_pattern(self):
                syslogpat3 = re.compile(r"(\d+:) (\*\w{3}\s{1,2}\d{1,2}) (\d{2}:\d{2}:\d{2}\.\d{3}:) (%\w+-3-\w*:) (.*)")
                return syslogpat3
        def lvl0_pattern(self):
                syslogpat0 = re.compile(r"(\d+:) (\*\w{3}\s{1,2}\d{1,2}) (\d{2}:\d{2}:\d{2}\.\d{3}:) (%\w+-[0-2]-\w*:) (.*)")
                return syslogpat0
        def lvl8_pattern(self):
                syslogpat0 = re.compile(r"(\d+:) (\*\w{3}\s{1,2}\d{1,2}) (\d{2}:\d{2}:\d{2}\.\d{3}:) (%\w+-[5-7]-\w*:) (.*)")
                return syslogpat0
        
        def engine_lvl4(self):
                try: 
                        connection = ConnectHandler(
                                device_type = self.dev_type,
                                host = self.ip_addr,
                                username = self.user,
                                password = self.pas,
                                secret = self.sec
                                )
                        t0 = self.timming()
                        syslogpat = self.lvl4_pattern()
                        syslog = connection.send_command(f"sh log | i {t0}")
                        connection.disconnect()
                        rawout= re.findall(syslogpat,syslog)
                        syslist = []
                        for i in rawout :
                                cookedout = " ".join(i)
                                syslist.append(cookedout)
                        content =set(syslist)
                        content_str = "\n".join(syslist)
                        with open(f"{self.dev_name}_l4_logs.txt","a+") as logs : #This will keep all the specific level logs of day t0 
                                logs.seek(0)
                                counter = set((logs.read()).splitlines())
                        try:
                                newlogs = sorted(content - counter)
                                newlogs_str = "\n".join(newlogs)
                                if newlogs: 
                                        with open(f"{self.dev_name}_l4_{t0}.txt","w") as sysmsg: #This is the current status of syslog messages 
                                                sysmsg.write(newlogs_str)
                                                sysmsg.seek(0)
                                        mail = EmailMessage() #an EmailMessage object is created 
                                        mail["From"] = "labtest.raj@gmail.com" # Here ["From"] access the email header field 
                                        password = "" #EmailMessage has nothing to do with passwords or authentication , its just for the email format , we will simple pass mail["From"] and password to server.login(mail["From"],password), where passowrd is a variable where our password is sotred
                                        mail["To"] = "rajdeka.official@gmail.com" # Here ["To"] access the email header field 
                                        mail["Cc"] = "labtest.raj@gmail.com" # Here ["Cc"] access the email header field 
                                        to_list = ["rajdeka.official@gmail.com"] #List of To reciepents 
                                        cc_list = ["labtest.raj@gmail.com"] #List of CC reciepents
                                        all_receiver = to_list + cc_list #smtp ignores headers for delivery , we should pass it to smtp without headers 
                                        mail.set_content(f"ALERT ⚠️ ,\n\nState change detected in device.\nSYSLOG LEVEL - 04(WARNING)\n\n{newlogs_str}\n\nKindly look into the as soon as possible.\n\nThis is a system generated message")
                                        server = smtplib.SMTP("smtp.gmail.com", 587 , timeout=30)#an smtplip.SMTP() object is created 
                                        server.starttls()
                                        server.login(mail["From"],password)
                                        server.sendmail(mail["From"],all_receiver,mail.as_string())
                                        server.close()
                                        with open(f"{self.dev_name}_l4_logs.txt","") as logs : 
                                                logs.seek(0)
                                                logs.write(content_str)
                        except Exception as e:
                                         print(e)                        
                        
                except NetmikoTimeoutException : 
                        print("Connection cannot be establish at the moment , please try again later")
                except NetmikoAuthenticationException : 
                        print("Connection failed due to authentication issue . ")
                except Exception as e :
                        print(e)
        def engine_lvl3(self):
                try: 
                        connection = ConnectHandler(
                                device_type = self.dev_type,
                                host = self.ip_addr,
                                username = self.user,
                                password = self.pas,
                                secret = self.sec
                                )
                        t0 = self.timming()
                        syslogpat = self.lvl3_pattern()
                        syslog = connection.send_command(f"sh log | i {t0}")
                        connection.disconnect()
                        rawout= re.findall(syslogpat,syslog)
                        syslist = []
                        for i in rawout :
                                cookedout = " ".join(i)
                                syslist.append(cookedout)
                        content =set(syslist)
                        content_str = "\n".join(syslist)
                        with open(f"{self.dev_name}_l3_logs.txt","a+") as logs : #This will keep all the specific level logs of day t0 
                                logs.seek(0)
                                counter = set((logs.read()).splitlines())
                        try:
                                newlogs = sorted(content - counter)
                                newlogs_str = "\n".join(newlogs)
                                if newlogs: 
                                        with open(f"{self.dev_name}_l3_{t0}.txt","w") as sysmsg: 
                                                sysmsg.write(newlogs_str)
                                                sysmsg.seek(0)#if statement does not require any true and flase statement explicitly , it checks whether something is trythy or falsy 
                                        mail = EmailMessage() #an EmailMessage object is created 
                                        mail["From"] = "labtest.raj@gmail.com" # Here ["From"] access the email header field 
                                        password = "" #EmailMessage has nothing to do with passwords or authentication , its just for the email format , we will simple pass mail["From"] and password to server.login(mail["From"],password), where passowrd is a variable where our password is sotred
                                        mail["To"] = "rajdeka.official@gmail.com" # Here ["To"] access the email header field 
                                        mail["Cc"] = "labtest.raj@gmail.com" # Here ["Cc"] access the email header field 
                                        to_list = ["rajdeka.official@gmail.com"] #List of To reciepents 
                                        cc_list = ["labtest.raj@gmail.com"] #List of CC reciepents
                                        all_receiver = to_list + cc_list #smtp ignores headers for delivery , we should pass it to smtp without headers 
                                        mail.set_content(f"ALERT ⚠️ ,\n\nError state detected in device.\nSYSLOG LEVEL - 03(ERROR)\n\n{newlogs_str}\n\nKindly look into the as soon as possible.\nThis is a system generated message")
                                        server = smtplib.SMTP("smtp.gmail.com", 587 , timeout=30)#an smtplip.SMTP() object is created 
                                        server.starttls()
                                        server.login(mail["From"],password)
                                        server.sendmail(mail["From"],all_receiver,mail.as_string())
                                        server.close()
                                        with open(f"{self.dev_name}_l3_logs.txt","") as logs : 
                                                logs.seek(0)
                                                logs.write(content_str)
                        except Exception as e:
                                         print(e)                        
                        
                except NetmikoTimeoutException : 
                        print("Connection cannot be establish at the moment , please try again later")
                except NetmikoAuthenticationException : 
                        print("Connection failed due to authentication issue . ")
                except Exception as e :
                        print(e)
        def engine_lvl0(self):
                try: 
                        connection = ConnectHandler(
                                device_type = self.dev_type,
                                host = self.ip_addr,
                                username = self.user,
                                password = self.pas,
                                secret = self.sec
                                )
                        t0 = self.timming()
                        syslogpat = self.lvl0_pattern()
                        syslog = connection.send_command(f"sh log | i {t0}")
                        connection.disconnect()
                        rawout= re.findall(syslogpat,syslog)
                        syslist = []
                        for i in rawout :
                                cookedout = " ".join(i)
                                syslist.append(cookedout)
                        content =set(syslist)
                        content_str = "\n".join(syslist)
                        with open(f"{self.dev_name}_l0_logs.txt","a+") as logs : #This will keep all the specific level logs of day t0 
                                logs.seek(0)
                                counter = set((logs.read()).splitlines())
                        try:
                                newlogs = sorted(content - counter)
                                newlogs_str = "\n".join(newlogs)
                                if newlogs:
                                        with open(f"{self.dev_name}_l0_{t0}.txt","w") as sysmsg: #This is the current status of syslog messages 
                                                sysmsg.write(newlogs_str)
                                                sysmsg.seek(0)
                                        mail = EmailMessage() #an EmailMessage object is created 
                                        mail["From"] = "labtest.raj@gmail.com" # Here ["From"] access the email header field 
                                        password = "" #EmailMessage has nothing to do with passwords or authentication , its just for the email format , we will simple pass mail["From"] and password to server.login(mail["From"],password), where passowrd is a variable where our password is sotred
                                        mail["To"] = "rajdeka.official@gmail.com" # Here ["To"] access the email header field 
                                        mail["Cc"] = "labtest.raj@gmail.com" # Here ["Cc"] access the email header field 
                                        to_list = ["rajdeka.official@gmail.com"] #List of To reciepents 
                                        cc_list = ["labtest.raj@gmail.com"] #List of CC reciepents
                                        all_receiver = to_list + cc_list #smtp ignores headers for delivery , we should pass it to smtp without headers 
                                        mail.set_content(f"🚨EMERGENCY🚨 ,\n\nCritical state detected in device.\nSYSLOG LEVEL - (0-2)\n\n{newlogs_str}\n\nKindly look into the matter immediately .\n\nThis is a system generated message")
                                        server = smtplib.SMTP("smtp.gmail.com", 587 , timeout=30)#an smtplip.SMTP() object is created 
                                        server.starttls()
                                        server.login(mail["From"],password)
                                        server.sendmail(mail["From"],all_receiver,mail.as_string())
                                        server.close()
                                        with open(f"{self.dev_name}_l0_logs.txt","") as logs : 
                                                logs.seek(0)
                                                logs.write(content_str)
                        except Exception as e:
                                         print(e)                        
                        
                except NetmikoTimeoutException : 
                        print("Connection cannot be establish at the moment , please try again later")
                except NetmikoAuthenticationException : 
                        print("Connection failed due to authentication issue . ")
                except Exception as e :
                        print(e)      
        def engine_lvl8(self):
                try: 
                        connection = ConnectHandler(                   #1
                                device_type = self.dev_type,
                                host = self.ip_addr,
                                username = self.user,
                                password = self.pas,
                                secret = self.sec
                                )
                        t0 = self.timming() #2
                        syslogpat = self.lvl8_pattern() #3
                        syslog = connection.send_command(f"sh log | i {t0}")#4
                        connection.disconnect() #5
                        rawout= re.findall(syslogpat,syslog) #6
                        syslist = [] #7
                        for i in rawout : #8
                                cookedout = " ".join(i)
                                syslist.append(cookedout)
                        content =set(syslist)   #9             
                        content_str = "\n".join(syslist)    #10
                        with open(f"{self.dev_name}_l8_logs.txt","a+") as logs :     #11                  
                                logs.seek(0)
                                counter = set((logs.read()).splitlines())
                        try:
                                newlogs = sorted(content - counter) #12
                                newlogs_str = "\n".join(newlogs)       #13
                                if newlogs: #14
                                        with open(f"{self.dev_name}_l8_{t0}.txt","w") as sysmsg: #This is the current status of syslog messages 
                                                sysmsg.write(newlogs_str)
                                                sysmsg.seek(0)
                                        mail = EmailMessage() #an EmailMessage object is created 
                                        mail["From"] = "labtest.raj@gmail.com" # Here ["From"] access the email header field 
                                        password = "" #EmailMessage has nothing to do with passwords or authentication , its just for the email format , we will simple pass mail["From"] and password to server.login(mail["From"],password), where passowrd is a variable where our password is sotred
                                        mail["To"] = "rajdeka.official@gmail.com" # Here ["To"] access the email header field 
                                        mail["Cc"] = "labtest.raj@gmail.com" # Here ["Cc"] access the email header field 
                                        to_list = ["rajdeka.official@gmail.com"] #List of To reciepents 
                                        cc_list = ["labtest.raj@gmail.com"] #List of CC reciepents
                                        all_receiver = to_list + cc_list #smtp ignores headers for delivery , we should pass it to smtp without headers 
                                        mail.set_content(f"INFORMATIONAL,\n\nChange detected in device.\nSYSLOG LEVEL - (5-7) INFORMATIONAL \n\n{newlogs_str}\n.\n\nThis is a system generated message")
                                        server = smtplib.SMTP("smtp.gmail.com", 587 , timeout=30)#an smtplip.SMTP() object is created 
                                        server.starttls()
                                        server.login(mail["From"],password)
                                        server.sendmail(mail["From"],all_receiver,mail.as_string())
                                        server.close()
                                        with open(f"{self.dev_name}_l8_logs.txt","") as logs : #15
                                                logs.seek(0)
                                                logs.write(content_str)
                                else :
                                        pass
                        except Exception as e:
                                         print("Error :" , e)                        
                        
                except NetmikoTimeoutException : 
                        print("Connection cannot be establish at the moment , please try again later")
                except NetmikoAuthenticationException : 
                        print("Connection failed due to authentication issue . ")
                except Exception as e :
                        print(e)
        


