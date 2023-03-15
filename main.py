import os
import platform
import requests
import psutil
import wmi
import GPUtil
import tempfile
import shutil

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
    print("Windows OS supported only!")

process = psutil.Process()
ram_count = process.memory_info().rss
ram_total = psutil.virtual_memory().total

x = wmi.WMI()

gpu = GPUtil.getAvailable(order='first', limit=1, maxLoad=0.5, maxMemory=0.5, includeNan=False, excludeID=[], excludeUUID=[])[0]
gpu_vram = round(GPUtil.getGPUs()[gpu].memoryTotal / 1024.0)

cpu_cores = psutil.cpu_count(logical=True)

path = r"C:\Windows\Temp"
size = 0
path2 = tempfile.gettempdir()

def get_directory_size(directory):
    path2_size = 0
    with os.scandir(directory) as it:
        for entry in it:
            if entry.is_file():
                path2_size += entry.stat().st_size
            elif entry.is_dir():
                path2_size += get_directory_size(entry.path)
    return path2_size

tempdir_path2_size = get_directory_size(tempfile.gettempdir())

for dirpath, _, filenames in os.walk(path):
    for f in filenames:
        fp = os.path.join(dirpath, f)
        size += ((os.path.getsize(fp)//(1024*1024*1024))) + (tempdir_path2_size//(1024*1024*1024))

# Bruh?
print("User:", user_name)
print("User Dir:", user_folder)
print("OS:", rel)
print("IP:", ip_address)
print("Free Space: ~", space, "GB")
for item in x.Win32_BaseBoard():
    print("Motherboard: {} ".format(item.Product))
print("CPU: {}".format(cpudata))
print("CPU Cores:", cpu_cores)
print("GPU: {}".format(videodata))
print("GPU VRAM:", gpu_vram, "GB")
for item in x.Win32_PhysicalMemory():
    if item == item:
        print("RAM: {} ".format(item.PartNumber))
        break
    else:
        print("RAM: {} ".format(item.PartNumber))
print("RAM Capacity(with pagefile):", ram_count//1024//1024, "GB")
print("RAM Total:", ram_total//1024//1024//1024, "GB")
if size > 5:
    print("Temp files size is too big! (", (size),"GB )")
    input("Press ENTER to delete temp files...")
    for foldername in os.listdir(tempfile.gettempdir()):
        folderpath = os.path.join(tempfile.gettempdir(), foldername)
        if os.path.isdir(folderpath):
            for filename in os.listdir(folderpath):
                filepath = os.path.join(folderpath, filename)
                try:
                    os.remove(filepath)
                except Exception as e:
                    print(f"Error on deleting {filepath}: {e}, try to run as administrator!")
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)         
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Error on deleting ' + file_path + '. Reason: ' + str(e))
    print('Cleaning is complete!')
else:
    print("Temp files size:", (size),"GB")

os.system("pause")  # stoper
