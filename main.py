import os
import platform
import requests
import psutil
import wmi
import GPUtil
import tempfile
import speedtest as st
import uuid
import geocoder
import time

os.system('cls' if os.name == 'nt' else 'clear')
print("Dev: ShamHyper, Daun-Dev Studios")
print("Wait, we collect data about your PC...")
print("")

start_time = time.time()
st = st.Speedtest()
download_speed = round(st.download()//1000000)
upload_speed = round(st.upload()//1000000)
mac_address = uuid.getnode()
user_name = os.getlogin()
user_folder = os.path.expanduser('~')
rel = platform.platform(aliased=True)
ip_response = requests.get('https://api.ipify.org?format=json')
ip_address = ip_response.json()['ip']
total_free_space = 0
g = geocoder.ip('me')
city = g.city
country = g.country

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
os.system('cls' if os.name == 'nt' else 'clear')
print("User:", user_name)
print("User Dir:", user_folder)
print("OS:", rel)
print("Free Space: ~", space, "GB")
for item in x.Win32_BaseBoard():
    print("Motherboard: {} ".format(item.Product))
print("CPU {}:".format(cpudata))
print("CPU Cores:", cpu_cores)
print("GPU: {}".format(videodata))
print("GPU VRAM:", gpu_vram, "GB")
for item in x.Win32_PhysicalMemory():
    if item == item:
        print("RAM: {} ".format(item.PartNumber))
        break
    else:
        print("RAM: {} ".format(item.PartNumber))
print("RAM Capacity:", ram_total//1024//1024//1024, "GB")
print("IP:", ip_address)
print(f"You are located in {city}, {country}")
print(f"Download Speed: {download_speed} MB/ps")
print(f"Upload Speed: {upload_speed} MB/ps")
print("")

#########################################################################

end_time = time.time()

total_time = round(end_time - start_time)

print("Information search time: ~", total_time, "seconds")

os.system("pause") # stoper


