# astro_image_processing

This repository holds the code used by Alan Meert for research in Astrophysics at the University of Pennsylvania. There are many packages here. 

## Installation
To install, make sure that your __PYTHONPATH__ includes the directory holding this repository. Then run the _create_user_params.sh_ script which will create a file called _user_settings.py_ that holds your credentials for MySQL, SDSS CasJobs, and some paths.

## The fitting pipeline
A large part of this project is the fitting pipeline for SDSS galaxies. This can be divided into several steps. The steps are outlined below along with the relevant modules in this code.

1. __Catalog construction__ - (see the _casjobs\_query_ module) Prior to fitting, a catalog of galaxies is needed. In addition, relevant details about the galaxies are necessary to extract the postage stamp images of each galaxy. An identifying ID number, SDSS run, SDSS rerun, SDSS camCol, SDSS field, band-specific rowc, band-specific colc, and half-light radius are needed for fitting. The ID number is referred as _galcount_ and used throughout the pipeline for record-keeping. The run, rerun, camCol, field specify the image to use for extraction. The rowc and colc specify the pixel coordinates of the center of the galaxy in the image. The half-light radius sets the scale for the size of the cutout. The _casjobs_query_ module is intended to be used to collect this data.

2. __Image collection and extraction__ - (see the _cut\_pipe_ module) After collecting the catalog, we need to extract the postage stamp image, construct a weight image, and extract the PSF image. The _cut\_pipe_ mdule does this. It downloads the SDSS image frame and SDSS psField file and then extracts the postage stamp, constructs the weight image, and extracts the PSF image.

3. __Running the fitting__ - (see _grid\_management.job\_manager_) The stamps have to be fit, the job_manager handles the Pymorph config file construction and running Pymorph. This also assumes that Pymorph, Galfit, and SExtractor are installed on your machine. See the _INSTALL.txt_ file for information on these dependencies.

4. __Post-processing of the fits__ - (see the _post\_processing_ module) After fitting, measurement of the non-PSF convolved half-light radius, and profile measurements are made.

5. __Flagging__ - (see the _flagging_ module) Finally the flagging must be run.

## Other included modules 
There are many other included modules in this codebase. These will be listed here eventually.

  