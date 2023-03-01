import csv
import glob
import os
import sys
import time
from string import ascii_uppercase


def getmsg(name: str, info: str, warning="No Information", file=sys.stdout) -> str:
    print(name, info, warning, sep="\n", end="\n\n", file=file)


def printdata(data_, mode_, dest=sys.stdout):
    for idx, elem in enumerate(data_[0]):
        if isinstance(data_[1][idx], float):
            if "temp" in elem.lower() and data_[1][idx] > 45:
                getmsg(elem, data_[1][idx], msgs["temp"], dest)
            elif "life" in elem.lower() and data_[1][idx] < 25:
                getmsg(elem, data_[1][idx], msgs["life"], dest)
            elif "space" in elem.lower() and data_[1][idx] > 90:
                getmsg(elem, data_[1][idx], msgs["space"], dest)
            elif "available memory" in elem.lower() and data_[1][idx] < 1:
                getmsg(elem, data_[1][idx], msgs["available memory"], dest)
            elif "fan" in elem.lower() and data_[1][idx] < 300:
                getmsg(elem, data_[1][idx], msgs["fan"], dest)
            else:
                if mode_ in (1, 2):
                    getmsg(elem, data_[1][idx], msgs["ok"], dest)
        else:
            if mode_ == 1:
                getmsg(elem, "...")


def exiting():
    print("Exiting...")
    time.sleep(1)
    quit()


msgs = {"temp": "---> WARNING: Component temperature above 45C! <---",
        "life": "---> WARNING! SSD life is depleted by more than 75%! <---",
        "space": "---> WARNING! The drive is more than 90% full! <---",
        "available memory": "---> WARNING! Less than 1GB of free RAM! <---",
        "fan": "---> WARNING! Check the fan! <---",
        "ok": "---> OK <---",
        }

mode = 0
while mode not in (1, 2, 3, 4):
    print("1. Full report\n"
          "2. Full report, ignore 'no info' components\n"
          "3. Warnings only\n"
          "4. Exit\n")

    try:
        mode = int(input("Enter a number: "))
    except ValueError:
        continue

if mode == 4:
    exiting()

drive = input("Enter the drive letter where the OHM is located: ").upper()
for root, subdirs, files in os.walk(drive + r":\\"):
    for d in subdirs:
        if d == "OpenHardwareMonitor":
            fullpath = os.path.join(root, d)
            break
    else:
        continue
    break

csv_files = glob.glob(fullpath + r"\*.csv")
latest = max(csv_files, key=os.path.getctime)

with open(latest, "r", encoding="utf-8") as f:
    data = list(csv.reader(f))

for i, e in enumerate(data[0]):
    data[0][i] = f"{data[1][i]} -- {e}" if e else data[1][i]

del data[1]

for i in data[1:]:
    for k, j in enumerate(i):
        try:
            i[k] = float(j)
        except ValueError:
            i[k] = None

for i, e in enumerate(data[1]):
    if e:
        mean = sum(data[j][i] for j in range(1, len(data))) / (len(data) - 1)
        data[1][i] = round(mean, 4)
    else:
        data[1][i] = None

del data[2:]

printdata(data, mode)

print("Save results to txt file? (Y/N): ", end="")
save = input()

if save.lower() == "y":
    while True:
        filename = input("Enter file name: ") + ".txt"
        try:
            with open(filename, "w", encoding="utf-8") as r:
                printdata(data, mode, r)
            break
        except OSError:
            print("Can't name a file like that")
            continue

exiting()
