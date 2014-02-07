#include "myfitsio.h"
using namespace std;


void write_fits(string filename, const tmv::Matrix<double>& im)
{
  filename = "!" + filename;
  fitsfile *outfptr;  /* FITS file pointers */
  int status = 0;  /* CFITSIO status value MUST be initialized to zero! */
  double *apix;
  long npixels = 1;


  /* create the new empty output file if the above checks are OK */
  if ( !fits_create_file(&outfptr, filename.c_str(), &status) )
    {
      int naxis = 2;
      long naxes[2];

      naxes[1] = im.nrows();
      naxes[0] = im.ncols();
      /* Create the primary array image (16-bit short integer pixels */
      fits_create_img(outfptr, DOUBLE_IMG, naxis, naxes, &status);
      double exposure = 1500.;
      fits_update_key(outfptr, TLONG, "EXPOSURE", &exposure,
		      "Total Exposure Time", &status);
      /* Initialize the values in the image with a linear ramp function */

      npixels = naxes[0]*naxes[1];  /* no. of pixels to read in each row */
      apix =  (double *) malloc(npixels * sizeof(double)); /* mem for 1 row */
	
      for (int jj = 0; jj < im.nrows(); jj++)
	for (int ii = 0; ii < im.ncols(); ii++)
	  apix[jj*im.ncols()+ii] = im[jj][ii];
      int fpixel = 1;
      fits_write_img(outfptr, TDOUBLE, fpixel, npixels, apix, &status);
	
      fits_close_file(outfptr, &status);
      if (status) fits_report_error(stderr, status);
      free(apix);
    }
  else
    {
      cerr << "Error writing fits file." << endl;
      if (status) fits_report_error(stderr, status);
      exit(-1);
    }
}

// Using cfitsio code 
// http://heasarc.gsfc.nasa.gov/fitsio/
tmv::Matrix<double> read_fits(string filename)
{
  if( filename.substr( filename.size()-3,3)=="txt")
    return read_image(filename.c_str());

  vector< vector<double> > image;
  
  fitsfile *fptr;   /* FITS file pointer, defined in fitsio.h */
  int status = 0;   /* CFITSIO status value MUST be initialized to zero! */
  int bitpix, naxis, ii;
    long naxes[2] = {1,1}, fpixel[2] = {1,1};
    double *pixels;

    if (!fits_open_file(&fptr, filename.c_str(), READONLY, &status))
    {
        if (!fits_get_img_param(fptr, 2, &bitpix, &naxis, naxes, &status) )
        {
          if (naxis > 2 || naxis == 0)
             printf("Error: only 1D or 2D images are supported\n");
          else
          {
            /* get memory for 1 row */
            pixels = (double *) malloc(naxes[0] * sizeof(double));

            if (pixels == NULL) {
                printf("Memory allocation error\n");
		exit(-1);
            }

	    // Automatically detect and subtract SOFTBIAS
	    // This is commonly added to SDSS images.
	    int sb=0;
	    if (fits_read_key(fptr, TINT, "SOFTBIAS",&sb,NULL,&status))
	      status = 0;
	      
            /* loop over all the rows in the image, top to bottom */
            for (fpixel[1] = naxes[1]; fpixel[1] >= 1; fpixel[1]--)
            {
	      vector<double> row;
	      if (fits_read_pix(fptr, TDOUBLE, fpixel, naxes[0], NULL,
                    pixels, NULL, &status) )  /* read row of pixels */
                  break;  /* jump out of loop on error */

               for (ii = 0; ii < naxes[0]; ii++)
		 {
		   row.push_back(pixels[ii]-sb);
		 }
	       image.push_back(row);
            }
            free(pixels);
          }
        }
        fits_close_file(fptr, &status);
    } 
    
    if (status) fits_report_error(stderr, status); /* print any error message */
    tmv::Matrix<double> tmp(image);
    int r = tmp.nrows();
    int c = tmp.ncols();
    tmv::Matrix<double> out(r,c);
    for( int i=0; i<r; i++)
      for( int j=0; j<c; j++)
	out[i][j] = tmp[r-i-1][j];
    return out;
}
