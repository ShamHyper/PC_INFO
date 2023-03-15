import os
import platform
import requests
import psutil
import wmi
import subprocess

user_name = os.getlogin()
user_folder = os.path.expanduser('~')
rel = platform.platform(aliased=True)
ip_response = requests.get('https://api.ipify.org?format=json')
ip_address = ip_response.json()['ip']
space1 = psutil.disk_usage("C:").free//(1024*1024*1024)
space2 = psutil.disk_usage("D:").free//(1024*1024*1024)
space = int(space1 + space2)

system = platform.system()
platform = platform.platform()

if system == "Windows":
    import winreg

    cpudata = ""
    regpath = r"HARDWARE\DESCRIPTION\System\CentralProcessor\0"
    valuename = "ProcessorNameString"

    try:
        keyval = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, regpath)
        cpudata = winreg.QueryValueEx(keyval, valuename)[0]
    except WindowsError:
        cpudata = "N/A"

    from subprocess import Popen, PIPE

    videodata = ""
    cmd = "wmic path win32_VideoController get name"
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    output, error = p.communicate()
    if not error:
        videodata = output.strip().decode('utf-8').split('\n')[1].strip()
    else:
        videodata = "N/A"

else:
    print("Ваш компьютер не на ОС Windows!")

x = wmi.WMI()

# Вывод информации
print("Имя пользователя ПК:", user_name)
print("Папка пользователя ПК:", user_folder)
print("Сборка:", rel)
print("IP:", ip_address)
print("Свободное место: ~", space,"ГБ")
for item in x.Win32_BaseBoard():
    print("Материнская Плата: {} ".format(item.Product))
print("CPU: {}".format(cpudata))
print("GPU: {}".format(videodata))
for item in x.Win32_PhysicalMemory():
    if item == item:
        print("RAM: {} ".format(item.PartNumber))
        break
    else:
        print("RAM: {} ".format(item.PartNumber))

os.system("pause")








