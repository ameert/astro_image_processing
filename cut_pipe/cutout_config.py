#### The configuration file for running the cutouts ####

### mysql info ###
table_name = 'manga_cast'

### Paths ###
data_dir = '/home/alan/Desktop/test/data/' #directory for downloading data
cut_dir =  '/home/alan/Desktop/test/cutouts/' #output directory

### Settings for cutouts ###
bands = 'gri' # list all desired bands in a single string
pix_scale = 0.396 # arcsec per pixel
cut_size = 20.0 # the radius of the cutout image in multiples of PetroRad50
min_size = 80.0 # minimum size in pixels
folder_size = 250 # num of galaxies/folder
folder_fmt = "%04d"

### params that are fetched by the SQL query ###
band_params = ['rowc','colc','petroR50'] #band-specific params needed
params = ['galcount','run','rerun','camCol','field'] #galaxy-specific information
