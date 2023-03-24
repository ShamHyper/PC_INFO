import wmi
import re

c = wmi.WMI()
gpu_info = c.Win32_VideoController()[0]
manufacturer = gpu_info.VideoProcessor

def AMDFinder(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

if not AMDFinder('AMD')(manufacturer):
    print("Why?")
    print(manufacturer)
