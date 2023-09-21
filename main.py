import os
import platform
import psutil
import wmi
import time
import GPUtil
import sys
import re
import winreg

x = wmi.WMI()

yep = ["Yes", "yes", "Y", "y", "Да", "да", "1"]

def clear():
    print('\033[37m')
    os.system('cls' if os.name == 'nt' else 'clear')

clear()

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
print("Bye!")
print("")
print("\(★ω★)/")
print("")
input()