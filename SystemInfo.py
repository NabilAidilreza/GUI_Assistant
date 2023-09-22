import platform
import psutil

def getPCInfo():
    main_string = ""
    info = ["|| System Information ||\n",
    (f"Computer network name: {platform.node()}"),
    (f"Machine type: {platform.machine()}"),
    (f"Processor type: {platform.processor()}"),
    (f"Platform type: {platform.platform()}"),
    (f"Operating system: {platform.system()}"),
    (f"Operating system release: {platform.release()}"),
    (f"Operating system version: {platform.version()}")]
    for inf in info:
        main_string += inf + "\n"
    return main_string[0:-2]


def getCPU():
    #Current frequency
    print(f"Current CPU frequency: {psutil.cpu_freq().current}")
    #Min frequency
    print(f"Min CPU frequency: {psutil.cpu_freq().min}")
    #Max frequency
    print(f"Max CPU frequency: {psutil.cpu_freq().max}")

    #System-wide CPU utilization
    print(f"Current CPU utilization: {psutil.cpu_percent(interval=1)}")
    #System-wide per-CPU utilization
    print(f"Current per-CPU utilization: {psutil.cpu_percent(interval=1, percpu=True)}")

    #Total RAM
    print(f"Total RAM installed: {round(psutil.virtual_memory().total/1000000000, 2)} GB")
    #Available RAM
    print(f"Available RAM: {round(psutil.virtual_memory().available/1000000000, 2)} GB")
    #Used RAM
    print(f"Used RAM: {round(psutil.virtual_memory().used/1000000000, 2)} GB")
    #RAM usage
    print(f"RAM usage: {psutil.virtual_memory().percent}%")


