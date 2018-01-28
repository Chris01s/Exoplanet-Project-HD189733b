#!/bin/bash

NUM=$1

sudo mv	red_science_blue.fits	red_science_blue$NUM.fits
sudo mv	fluxcal_science_blue.fits	fluxcal_science_blue$NUM.fits
sudo mv red_science_blue$NUM.fits	/home/chris/Documents/Exoplanet_Research/HD189733/pro_path/blue
sudo mv fluxcal_science_blue$NUM.fits	/home/chris/Documents/Exoplanet_Research/HD189733/pro_path/blue
