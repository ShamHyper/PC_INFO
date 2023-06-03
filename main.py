import os
import platform
import requests
import psutil
import wmi
import geocoder
import time
import GPUtil
import sys
import re
import socket
import subprocess
import winreg
from tqdm import tqdm

x = wmi.WMI()

yep = ["Yes", "yes", "Y", "y", "Да", "да", "1"]

def clear():
    print('\033[37m')
    os.system('cls' if os.name == 'nt' else 'clear')

clear()

print('\033[31m')
print("Dev: ShamHyper, Daun-Dev Studios")
print('\033[32m')
print("Wait, we collect data about your PC...")

start_time = time.time()

user_name = os.getlogin()
user_folder = os.path.expanduser('~')

print("User data collected!")

rel = platform.platform(aliased=True)

print("OS data collected!")

total_free_space = 0
for partition in psutil.disk_partitions():
    mount_point = partition.mountpoint

    try:
        usage = psutil.disk_usage(mount_point)
        total_free_space += usage.free
    except PermissionError:
        continue
space = total_free_space // (1024**3)

print("Free space collected!")

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
    print("Windows OS supported only!")

gpus = GPUtil.getGPUs()
for gpu in gpus:
    gpuwho = gpu.name

key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Enum\DISPLAY")
num_monitors = winreg.QueryInfoKey(key)[0]

def Intel_AMD_Finder(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

if Intel_AMD_Finder('NVIDIA')(gpuwho):
    try:
        from py3nvml import py3nvml as nvidia_smi
    except:
        print("Please install the package 'nvidia-ml-py3' to get GPU information.")
        sys.exit()
    nvidia_smi.nvmlInit()
    device_count = nvidia_smi.nvmlDeviceGetCount()

    for i in range(device_count):
        handle = nvidia_smi.nvmlDeviceGetHandleByIndex(i)
        clock_rate = nvidia_smi.nvmlDeviceGetClockInfo(handle, nvidia_smi.NVML_CLOCK_GRAPHICS)
        memory_clock_rate = nvidia_smi.nvmlDeviceGetClockInfo(handle, nvidia_smi.NVML_CLOCK_MEM)

print("GPU data collected!")

process = psutil.Process()
ram_total = psutil.virtual_memory().total

print("RAM data collected!")

cpu_cores = psutil.cpu_count(logical=True)

print("CPU data collected!")

# Bruh?
clear()
# Bruh?
clear()
# Bruh?

print('\033[37m')
print("----------------------------------------------------------")
print("User:", user_name)
print("User Dir:", user_folder)
print("OS:", rel)
print("----------------------------------------------------------")
print("Free Space: ~", space, "GB")
for item in x.Win32_BaseBoard():
    print("Motherboard: {} ".format(item.Product))
print("CPU: {}".format(cpudata))
print("CPU Cores:", cpu_cores)
print("----------------------------------------------------------")

gpu_slots = -1
for gpu in gpus:
    gpu_slots += 1
    print(f"GPU {gpu_slots}: {gpu.name}")
    print(f"GPU {gpu_slots} Load:", gpu.load * 100, "%")
    print(f"GPU {gpu_slots} VRAM Total:", round(gpu.memoryTotal), "MB")
    print(f"GPU {gpu_slots} VRAM Free:", round(gpu.memoryFree), "MB")
    print(f"GPU {gpu_slots} VRAM Used:", round(gpu.memoryUsed), "MB")
    print(f"GPU {gpu_slots} Temperature:", round(gpu.temperature), "°C")
    print(f"GPU {gpu_slots} Driver: {gpu.driver}")   
    if Intel_AMD_Finder('NVIDIA')(gpuwho):
        print(f"GPU {gpu_slots} Clock Speed: {clock_rate} MHz")
        print(f"GPU {gpu_slots} Memory Clock Rate: {memory_clock_rate} MHz")
print("----------------------------------------------------------")

ram_slots = -1
for item in x.Win32_PhysicalMemory():
    if item == item:
        ram_slots += 1
        print(f"RAM {ram_slots}: {{}}".format(item.PartNumber))
    else:
        print("RAM: {} ".format(item.PartNumber))
print("RAM Capacity:", ram_total//1024//1024//1024, "GB")
for item in x.Win32_PhysicalMemory():
    print(f"RAM Frequency: {item.Speed} Hz")
    break
print("----------------------------------------------------------")
for i in range(num_monitors):
    monitor_name = winreg.EnumKey(key, i)
    if monitor_name != "Default_Monitor":
        print(f"Screen: {monitor_name}")
print("----------------------------------------------------------")
print("")

end_time = time.time()
total_time = round(end_time - start_time)

print('\033[33m')
print("Information search time: ~", total_time, "seconds")
print("")
print('\033[37m')
print("Do you want to collect data about your internet?")

internet_need = False
input_check = input("Type [Yes/yes/Y/y] or press Enter to skip: ")
if input_check in yep:
    internet_need = True
else:
    internet_need = False

clear()

if internet_need == True:
    print("Collecting data about your internet...")
    hostname = socket.gethostname()
    ip_address_h = socket.gethostbyname(hostname)

    ip_response = requests.get('https://api.ipify.org?format=json')
    ip_address = ip_response.json()['ip']
    g = geocoder.ip('me')
    city = g.city
    country = g.country   

    clear()

    print("IP:", ip_address)
    print("IP (internal):", ip_address_h)
    print(f"You are located in {city}, {country}")
    print("")

print("Do you want to clear temp files?")
temp_need = False
temp_check = input("Type [Yes/yes/Y/y] or press Enter to skip: ")

if temp_check in yep:
    temp_need = True
else:
    temp_need = False

clear()

if temp_need == True:
    def clean_win_temp():
        Wtemp_path = os.path.abspath("C:\\Windows\\Temp")
        win_temp_size = 0
        for root, dirs, files in os.walk(Wtemp_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    win_temp_size += os.path.getsize(file_path)
                except PermissionError:
                    pass
                except FileNotFoundError:
                    pass
            for file in files:
                Wtemp_path = os.path.join(root, file)
                try:
                    win_temp_size_ = os.path.getsize(Wtemp_path)
                    win_temp_size += win_temp_size_
                    os.mkdir(Wtemp_path)
                except PermissionError:
                    pass
                except FileNotFoundError:
                    pass
                except FileExistsError:
                    pass
        return win_temp_size / 1024 / 1024 / 1024

    def clean_temp_files(root_dir):
        total_size = 0
        for subdir, dirs, files in os.walk(root_dir):
            for file in files:
                file_path = os.path.join(subdir, file)
                try:
                    if os.path.isfile(file_path):
                        file_size = os.path.getsize(file_path)
                        total_size += file_size
                        os.unlink(file_path)
                except Exception as e:
                    print(f'Error: {file_path} - {e}')
        return total_size / 1024 / 1024 / 1024

    def clean_temp_directory():
        temp_dir = os.getenv('temp')
        cache_dir = os.path.expanduser('~\\AppData\\Local\\Temp')
        total_size = 0
        for dir_path in (temp_dir, cache_dir):
            dir_size = clean_temp_files(dir_path)
            total_size += dir_size
        return total_size

    def clear_nvidia_cache():
        nvidia_path_1 = os.path.join(user_folder, "AppData", "Local", "NVIDIA", "DXCache")
        nvidia_path_2 = os.path.join(user_folder, "AppData", "Local", "NVIDIA", "GLCache")
        nvidia_cache_size = 0
        for dir_path in (nvidia_path_1, nvidia_path_2):
            dir_size = clean_temp_files(dir_path)
            nvidia_cache_size += dir_size
        return nvidia_cache_size

    win_temp_size = clean_win_temp()
    total_size = clean_temp_directory()
    nvidia_cache_size = clear_nvidia_cache()
    all_cache = total_size + win_temp_size + nvidia_cache_size

    clear()

    print(f"Total size of deleted files: {all_cache:.2f} GB")

print("Do you want to check the integrity of Windows system files?")
sfc_need = False
sfc_check = input("Type [Yes/yes/Y/y] or press Enter to skip: ")

if sfc_check in yep:
    sfc_need = True
else:
    sfc_need = False

clear()

if sfc_need == True:
    print("Running sfc...")
    subprocess.run(["sfc", "/scannow"]) 

print("Bye!")
print("\(★ω★)/")
print("")

print("The program will close at the end of the timer:")
mylist = [x for x in range(1, 300)]
for i in tqdm(mylist):
    time.sleep(0.00001)
