# PC_INFO 5
Collecting general information about the PC, displayed as a console

It is advisable to run as an administrator!

It works stably only on Windows OS and Nvidia GPUs ~~(AMD/Intel supported, but can work wrong!)~~ - __Now there is support for AMD/Intel video cards, but you will not be able to find out the frequency of the video core and memory:__
```py
def Intel_AMD_Finder(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

if Intel_AMD_Finder('NVIDIA')(gpuwho): #Sorry, but so far it is
```
You must have python installed to work properly!

![image](https://user-images.githubusercontent.com/104412752/225889613-69aed1d0-d947-4ed9-a47f-9f906b9f2771.png)

![image](https://user-images.githubusercontent.com/104412752/225889700-cc280e92-02d1-48e6-989b-34eac4b11233.png)

![image](https://user-images.githubusercontent.com/104412752/225889737-53d162df-1d02-473f-8e8f-209c4c9f679c.png)

