#!/usr/bin/env python3
import logging
import os
import time

import requests
from osgeo import gdal

logger = logging.getLogger("goes2pf")
logging.basicConfig(
    level=logging.INFO,
    format="{asctime} [{levelname}]: {message}",
    style="{",
    datefmt="%Y-%M-%d %H:%m:%S %z"
)

path = os.path.split(__file__)[0]
os.chdir(path)

GEOS19_URL="https://cdn.star.nesdis.noaa.gov/GOES19/ABI/CONUS/GEOCOLOR/GOES19-ABI-CONUS-GEOCOLOR-5000x3000.tif"
GEOS19_HASH="https://cdn.star.nesdis.noaa.gov/GOES19/ABI/CONUS/GEOCOLOR/GOES19-ABI-CONUS-GEOCOLOR-5000x3000.tif.sha256"

PLACEFILE = f"""
Title: GOES19 GEOCOLOR
RefreshSeconds: 30

Image: "{path}/geocolor-west.png"
    50, -140, 0, 0
    50, -100, 1, 0
    20, -100, 1, 1
    50, -140, 0, 0
    20, -100, 1, 1
    20, -140, 0, 1
End:
Image: "{path}/geocolor-east.png"
    50, -100, 0, 0
    50, -60, 1, 0
    20, -60, 1, 1
    50, -100, 0, 0
    20, -60, 1, 1
    20, -100, 0, 1
End:
"""
placefile_path = os.path.join(path, "goes_geocolor.txt")
with open(placefile_path, "w") as file:
    file.write(PLACEFILE)

logger.info(f"Placefile Path: '{placefile_path}'")

gdal.UseExceptions()
gdal.SetConfigOption('GTIFF_SRS_SOURCE', 'GEOKEYS')

lastHash = ""

while True:
    try:
        hashRes = requests.get(GEOS19_HASH)
    except Exception as e:
        time.sleep(30)
        logger.warning(str(e))
        continue
    if not hashRes.ok or hashRes.content == lastHash:
        time.sleep(150)
        continue

    logger.info("Downloading")
    try:
        res = requests.get(GEOS19_URL)
    except:
        logger.warning("Error with request. Waiting 10 seconds to try again")
        time.sleep(10)
        continue
    if res.ok:
        with open("GOES19-ABI-CONUS-GEOCOLOR-5000x3000.tif", "wb") as file:
            for chunk in res.iter_content(chunk_size=1<<20):
                file.write(chunk)
    else:
        continue
    lastHash = hashRes.content

    logger.info("Warpping")
    gdal.Warp(
        "geocolor-east.png", "GOES19-ABI-CONUS-GEOCOLOR-5000x3000.tif",
        options = gdal.WarpOptions(
            outputBounds = [-100, 20, -60, 50],
            outputBoundsSRS = "EPSG:4326",
            width = 2048,
            height = 2048,
            dstSRS = "EPSG:3857",
        )
    )
    gdal.Warp(
        "geocolor-west.png", "GOES19-ABI-CONUS-GEOCOLOR-5000x3000.tif",
        options = gdal.WarpOptions(
            outputBounds = [-140, 20, -100, 50],
            outputBoundsSRS = "EPSG:4326",
            width = 2048,
            height = 2048,
            dstSRS = "EPSG:3857",
        )
    )

    logger.info("Waiting For Refresh")
    time.sleep(30)
