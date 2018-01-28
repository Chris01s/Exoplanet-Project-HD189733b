#!/bin/bash

NUM=$1

sudo mv	red_science_redl.fits	red_science_redl$NUM.fits
sudo mv fluxcal_science_redl.fits	fluxcal_science_redl$NUM.fits
sudo mv red_science_redl$NUM.fits	/home/chris/Documents/Exoplanet_Research/HD189733/pro_path/redl
sudo mv fluxcal_science_redl$NUM.fits	/home/chris/Documents/Exoplanet_Research/HD189733/pro_path/redl

sudo mv	red_science_redu.fits	red_science_redu$NUM.fits
sudo mv fluxcal_science_redu.fits	fluxcal_science_redu$NUM.fits
sudo mv red_science_redu$NUM.fits	/home/chris/Documents/Exoplanet_Research/HD189733/pro_path/redu
sudo mv fluxcal_science_redu$NUM.fits	/home/chris/Documents/Exoplanet_Research/HD189733/pro_path/redu
