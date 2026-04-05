import os

from osgeo import osr

for path in osr.GetPROJSearchPaths():
    if os.path.exists(os.path.join(path, "proj.db")):
        print(path)
        exit()

print("Could not find any proj.db.")
exit(1)
