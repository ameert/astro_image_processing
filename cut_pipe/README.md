Cut Pipe
================
The cut_pipe takes a given catalog (usually supplied through a SQL table and downloads the frame images and psField files from 
the SDSS3 website. It then makes cutouts of all the galaxies in the given catalog and produces weight images and PSF images
to be used in fitting. A few notes about the program:
1. This is currently configured to run on SDSS3 data. There is old code to run on SDSS2, but you need to make changes to the code.
2. The code relies on a MySQL database for the input data. This can be moditied, but it is up to the user at this time.
3. There is a small test case available for the user. The data is pickled and can be run without MySQL.


Running the cutouts
--------------------
The run_cutouts executable python file will run the code. The code accepts two command line agruments "start_num" and "end_num" which correspond to the starting and ending id numbers of the galaxies that you wish to cutout. All galaxies with ids between these two will be cut. This allows multiple instances of the cutout routine to be run at once. HOWEVER, there are periodic clean-ups of the intermediate files that are created by the code (in particular, the unzipped fits images) which may cause conflicts between multiple instances. The best way to prevent deletion of intermediate files would be to run the bands separately (i.e. separate instances for g, r, and i bands). The best option would be to parallelize the code in the program, and coordinate the cleaning, but this has not been implemented.

To run the test case, type:
    ./run_cutouts.py -t 0 10

The -t option directs the program to use the test data rather than look for regular data. The start and stop ids are 0 and 10.

