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
total_free_space = 0

for partition in psutil.disk_partitions():
    mount_point = partition.mountpoint

    try:
        usage = psutil.disk_usage(mount_point)
        total_free_space += usage.free
    except PermissionError:
        continue

space = total_free_space // (1024**3)

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

process = psutil.Process()
ram_count = process.memory_info().rss
ram_total = psutil.virtual_memory().total


x = wmi.WMI()

# Вывод информации
print("User:", user_name)
print("User Dir:", user_folder)
print("OS:", rel)
print("IP:", ip_address)
print("Free Space: ~", space, "GB")
for item in x.Win32_BaseBoard():
    print("Motherboard: {} ".format(item.Product))
print("CPU: {}".format(cpudata))
print("GPU: {}".format(videodata))
for item in x.Win32_PhysicalMemory():
    if item == item:
        print("RAM: {} ".format(item.PartNumber))
        break
    else:
        print("RAM: {} ".format(item.PartNumber))
print("RAM Capacity(with pagefile):", ram_count//1024//1024, "GB")
print("Ram Total:", ram_total//1024//1024//1024, "GB")

os.system("pause")
