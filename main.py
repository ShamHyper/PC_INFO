import os
import platform
import requests
import psutil
import wmi
import speedtest as st
import geocoder
import time
import GPUtil
import sys
import re
import socket
import subprocess
import winreg

x = wmi.WMI()
os.system('cls' if os.name == 'nt' else 'clear')

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
os.system('cls' if os.name == 'nt' else 'clear')
# Bruh?
os.system('cls' if os.name == 'nt' else 'clear')
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

#I HATE THIS PART OF CODE!!!!!!!!!!!!!!!!
for gpu in gpus:
    print(f"GPU: {gpu.name} \nGPU VRAM: {(round(gpu.memoryTotal))//1024} GB")
    print("GPU Load:", gpu.load * 100, "%")
    print("GPU Free Memory:", round(gpu.memoryFree), "MB")
    print("GPU Used Memory:", round(gpu.memoryUsed), "MB")
    print("GPU Temperature:", round(gpu.temperature), "°C")
    print("GPU UUID:", gpu.uuid)
    print(f"GPU Driver: {gpu.driver}")
    if Intel_AMD_Finder('NVIDIA')(gpuwho):
        print(f"GPU Clock Speed: {clock_rate} MHz")
        print(f"GPU Memory Clock Rate: {memory_clock_rate} MHz")
#I HATE THIS PART OF CODE!!!!!!!!!!!!!!!!

print("----------------------------------------------------------")
for item in x.Win32_PhysicalMemory():
    if item == item:
        print("RAM: {} ".format(item.PartNumber))
        break
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

print("Do you want to collect data about your internet?")

internet_need = 2
input_check = input("[Yes/No]: ")

if input_check == "Yes":
    internet_need = 1
    if input_check == "No":
        internet_need = 0

os.system('cls' if os.name == 'nt' else 'clear')

if internet_need == 1:
    print("Collecting data about your internet...")
    hostname = socket.gethostname()
    ip_address_h = socket.gethostbyname(hostname)
    st = st.Speedtest()
    download_speed = round(st.download()//1000000)
    upload_speed = round(st.upload()//1000000)
    ip_response = requests.get('https://api.ipify.org?format=json')
    ip_address = ip_response.json()['ip']
    g = geocoder.ip('me')
    city = g.city
    country = g.country   

    os.system('cls' if os.name == 'nt' else 'clear')

    print("IP:", ip_address)
    print("IP (internal):", ip_address_h)
    print(f"You are located in {city}, {country}")
    print(f"Download Speed: {download_speed} MB/ps")
    print(f"Upload Speed: {upload_speed} MB/ps")
    print("")

print("Do you want to clear temp files?")
temp_need = 2
temp_check = input("[Yes/No]: ")

if temp_check == "Yes":
    temp_need = 1
    if temp_check == "No":
        temp_need = 0

os.system('cls' if os.name == 'nt' else 'clear')

if temp_need == 1:
    def clean_temp_files(root_dir):
        for subdir, dirs, files in os.walk(root_dir):
            for file in files:
                file_path = os.path.join(subdir, file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(f'Error: {file_path} - {e}')
    
    def clean_temp_directory():
        temp_dir = os.getenv('temp')
        cache_dir = os.path.expanduser('~\\AppData\\Local\\Temp')
        for dir_path in (temp_dir, cache_dir):
            clean_temp_files(dir_path)

    clean_temp_directory()

    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("All temp files that were accessed have been deleted!")

print("Do you want to check the integrity of Windows system files?")
sfc_need = 2
sfc_check = input("[Yes/No]: ")

if sfc_check == "Yes":
    sfc_need = 1
    if sfc_check == "No":
        sfc_need = 0

os.system('cls' if os.name == 'nt' else 'clear')

if sfc_need == 1:
    print("Running sfc...")
    subprocess.run(["sfc", "/scannow"]) 

print("")
print("Bye!")
print("")
print("\(★ω★)/")
os.system("pause") # stoper



