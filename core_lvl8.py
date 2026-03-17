import time 
import re
from netmiko import ConnectHandler
import os 
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException
from email.message import EmailMessage
import smtplib
import sysmodule as cus

os.chdir("/home/dekaraj22/Desktop/Projects/Automation_Projects/Automation_Project_3/Core_R/lvl5to7")

Core_router = cus.Devices("Core_R","cisco_ios","10.1.14.1","ad.hlab","admin2026","homelab123")
Core_router.lvl8_pattern()
Core_router.timming()
Core_router.engine_lvl8()
