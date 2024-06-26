import os
import platform
import psutil
import wmi
import winreg
from clear import clear
from time import time
import sys

start_time = time()
clear()

yep = ["Yes", "yes", "Y", "y", "Да", "да", "1"]

wmix = wmi.WMI()

user_name = os.getlogin()
user_folder = os.path.expanduser('~')

print("User data collected!")

rel = platform.platform(aliased=True)
pc_name = platform.node()
pc_pid = os.getpid()

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

process = psutil.Process()
ram_total = psutil.virtual_memory().total

print("RAM data collected!")

cpu_cores = psutil.cpu_count(logical=True)
cpu_load = round(psutil.cpu_percent())

print("CPU data collected!")
print('\033[37m')
clear()

def print_all():
    print("----------------------------------------------------------")
    print("User:", user_name)
    print("User Dir:", user_folder)
    print(f"PC Name: {pc_name}")
    print(f"PID: {pc_pid}")
    print("OS:", rel)
    print("----------------------------------------------------------")
    print("Free Space: ~", space, "GB")

    for item in wmix.Win32_BaseBoard():
        print("Motherboard: {} ".format(item.Product))

    print("CPU: {}".format(cpudata))
    print("CPU Cores:", cpu_cores)
    print(f"CPU Load: {cpu_load} %")
    print("----------------------------------------------------------")

    i_gpu = 0
    try:
        from gpuinfo.nvidia import get_gpus
        for gpu in get_gpus():
            gpu_name = gpu.__dict__["name"]
            gpu_video = gpu.__dict__["total_memory"]
            gpu_clock_max = gpu.get_max_clock_speeds()["max_core_clock_speed"]
            gpu_vram_clock_max = gpu.get_max_clock_speeds()["max_memory_clock_speed"]
            gpu_clock = gpu.get_clock_speeds()["core_clock_speed"]
            gpu_vram_clock = gpu.get_clock_speeds()["memory_clock_speed"]
            gpu_used_memory = gpu.get_memory_details()["used_memory"]
            gpu_free_memory = gpu.get_memory_details()["free_memory"]
            
            print(f"GPU {i_gpu}: {gpu_name}")
            print(f"GPU {i_gpu} VRAM: {gpu_video} MB")
            print(f"GPU {i_gpu} Used VRAM: {gpu_used_memory} MB")
            print(f"GPU {i_gpu} Free VRAM: {gpu_free_memory} MB")
            print(f"GPU {i_gpu} Clock Speed: {gpu_clock} MHz")
            print(f"GPU {i_gpu} VRAM Clock Speed: {gpu_vram_clock} MHz")
            print(f"GPU {i_gpu} Max Clock Speed: {gpu_clock_max} MHz")
            print(f"GPU {i_gpu} Max VRAM Clock Speed: {gpu_vram_clock_max} MHz")
            print("----------------------------------------------------------")
            
            i_gpu += 1
    except Exception:
        from gpuinfo.windows import get_gpus
        for gpu in get_gpus():
            gpu_name = gpu.__dict__["name"]
            gpu_video = gpu.__dict__["total_memory"]
            print(f"GPU {i_gpu}: {gpu_name}")
            print(f"GPU {i_gpu} VRAM: {gpu_video}")
            i_gpu += 1
        print("----------------------------------------------------------")
        
    for monitor in wmix.Win32_PnPEntity():
        if 'monitor' in str(monitor.caption).lower():
            model_info = monitor.caption.split('(')[-1].replace(')', '')
            print(f"Monitor Model: {model_info}")
    print("----------------------------------------------------------")
            
    ram_slots = -1
    for item in wmix.Win32_PhysicalMemory():
        if item == item:
            ram_slots += 1
            print(f"RAM {ram_slots}: {{}}".format(item.PartNumber))
        else:
            print("RAM: {} ".format(item.PartNumber))
    print("RAM Capacity:", ram_total//1024//1024//1024, "GB")
    for item in wmix.Win32_PhysicalMemory():
        print(f"RAM Frequency: {item.Speed} Hz")
        break
    print("----------------------------------------------------------")
    print("")

file_name = pc_name + ".txt"

with open(file_name, "w") as f:
    sys.stdout = f
    print_all()

sys.stdout = sys.__stdout__
print_all()

end_time = time()
total_time = round(end_time - start_time, 2)

print('\033[33m')
print(f"Information search time: ~{total_time} seconds")
print(f"All your PC specs. writen in {pc_name}.txt!")
print("Bye!")
print("\(★ω★)/")
input()