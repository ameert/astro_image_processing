Cut Pipe
================
The cut_pipe takes a given catalog (usually supplied through a SQL table and downloads the frame images and psField files from 
the SDSS3 website. It then makes cutouts of all the galaxies in the given catalog and produces weight images and PSF images
to be used in fitting. A few notes about the program:

1. This is currently configured to run on SDSS3 data. There is old code to run on SDSS2, but you need to make changes to the code.
2. All the run-specific settings are contained in cutout_config.py. Be sure to update this file prior to running.
3. The code relies on a MySQL database for the input data. This can be moditied, but it is up to the user at this time.
4. There is a small test case available for the user. The data is pickled and can be run without MySQL.


Running the cutouts
--------------------
The run_cutouts executable python file will run the code. The code accepts two command line agruments "start_num" and "end_num" which correspond to the starting and ending id numbers of the galaxies that you wish to cutout. All galaxies with ids between these two will be cut. This allows multiple instances of the cutout routine to be run at once. HOWEVER, there are periodic clean-ups of the intermediate files that are created by the code (in particular, the unzipped fits images) which may cause conflicts between multiple instances. The best way to prevent deletion of intermediate files would be to run the bands separately (i.e. separate instances for g, r, and i bands). The best option would be to parallelize the code in the program, and coordinate the cleaning, but this has not been implemented.

To run the test case, type:

    ./run_cutouts.py -t 0 10

The -t option directs the program to use the test data rather than look for regular data. The start and stop ids are 0 and 10.


Description of files
---------------------
* __run_cutouts.py__ -
    This is the main program that runs the pipeline. This is the only truly executable file. All others will run a diagnostic test or do nothing if run directly.
* __cut_example_data.pickle__ -
    Example data in pickled format for testing. Do not modifiy this file in any way.
* __cut_images.py__ - [*DEPRECATED*] The old image cutting routine for SDSS2 data.
* __cutout_config.py__ - File containing configuration settings for the cutouts. User must modify this file prior to running.
* __cut_sdss3.py__ - The current version of cut_images.py. This file contains the cutout code for cutting SDSS3 images.
* __download_files.py__ - The downloading scripts for SDSS2 and SDSS3 versions. 
* __get_data.py__ - The MySQL scripts for fetching and creating the data dictionary used by the cutout pipeline. Directions on replacing this file are below.
* __make_dirs.py__ - The scrupting used to verify the directory structure and fix it, if needed.
* __prepare_psf.py__ - The script that constructs the PSF image from the psField file at the location of the target galaxy. This should be/is independent of choice of SDSS2 or SDSS3. 
* __README.md__ - This file.
* __\_\_init\_\_.py__ - The book-keeping file for python that allows these files to be imported like a module.
* __SDSS3_image_DN.py__ - A class written to handle the SDSS3 frame fits data. This class can convert between nano-maggies and DN as well as reconstruct the image prior to background subtraction. A background-included image is required to get the weight image correct for GALFIT.

Modifying the get_data.py file to get other data
--------------------------------------------------------------------
The user may want to get data from somewhere other than MySQL. Any function can be used to 
return the data to the main program. The input of such a function should be the starting and ending id numbers (both ints). The output of any replacement function must return a 
dictionary with the following keywords:

* _galcount_ - An int numpy array with the id number of each galaxy for which cutouts are to be produced
* _dir_end_ - A string for the appended directory within which the cutouts will be placed. This allows the cutouts to be split into chucks for parallel processing on a cluster. The default folder size is 250 galaxies/folder. For example, as the default is setup, the cutouts of galaxies 1-250 will go in folder 0001 and galaxies 251-500 will go in folder 0002 and so on. 
* _run_ - An int array of SDSS run numbers for each galaxy
* _rerun_ - An int array of the SDSS rerun number for each galaxy
* _camCol_ - An int array of the SDSS camCol number for each galaxy
* _field_ - An int array of the SDSS field number for each galaxy
* _rowc_ - A float array of the rowc value for the galaxy center. There should be multiple instances of this keyword for each band in which cutouts are made. If cutouts are run on the g, r, and i bands, then there should be a _rowc_g_, _rowc_r_, and _rowc_i_ array.
* _colc_ - The same as _rowc_ except for the _colc_ values
* _petroR50_ - As with _rowc_ and _colc_ there should be multiple instances of this keyword for each band (_petroR50_g_, _petroR50_r_, and _petroR50_i_). This should be the petroR50 value in arcseconds or some other similar radius. It does not have to be the PetroRad, but should be named such to work in the code. This radius sets the scale of the cutout, which is set at __20 times__ this value in either direction.


The expected directory structure
----------------------------------
This code requires two directories exist:

* A __data_dir__ - Where the downloaded data will be stored
* A __cut_dir__ - Where the produced cutouts will be stored

Both of these paths are specified in the _cutout_config.py_ file. If these directories do not exist at runtime, the cut\_pipe will attempt to create them. 

Subdirectories will be created inside these directories. Inside _data_dir_  there will be a _psField_ directory that holds all the downloaded psField files. In addition, there will be a directory created for each band (usually g, r, i) that contain the downloaded frame files. Inside _cut_dir_, there will be a g, r, and i band directory and each of these directories will have directories with names specified by the _folder_fmt_ variable in the _cutout_config.py_ file. 

#### A simple example
Assume that _cut_dir_ = /home/your_name/data and _data_dir_ = /home/your_name/cutouts and that _folder_size_ = 250 and _folder_fmt_ = "%04" and you are doing the g, r, and i band. Then the resulting output would be:

* /home/your_name/data
  
  - /home/your_name/data/psField -containing the psField files for all galaxies
  - /home/your_name/data/g - the g-band frames
  - /home/your_name/data/r - the r-band frames
  - /home/your_name/data/i - the i-band frames
     
* /home/your_name/cutouts

  - /home/your_name/cutouts/g
 
    * /home/your_name/cutouts/g/0001 - g-band cutouts for galaxies 1-250
    * /home/your_name/cutouts/g/0002 - g-band cutouts for galaxies 251-500

  - /home/your_name/cutouts/r
 
    * /home/your_name/cutouts/r/0001 - r-band cutouts for galaxies 1-250
    * /home/your_name/cutouts/r/0002 - r-band cutouts for galaxies 251-500

  - /home/your_name/cutouts/i
 
    * /home/your_name/cutouts/i/0001 - i-band cutouts for galaxies 1-250
    * /home/your_name/cutouts/i/0002 - i-band cutouts for galaxies 251-500
