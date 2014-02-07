#ifndef MYFITSIO_H
#define MYFITSIO_H

#include "util.h"
#include "fitsio.h"

tmv::Matrix<double> read_fits(std::string filename);
void write_fits(std::string filename, const tmv::Matrix<double>& im);



#endif //MYFITSIO_H#include "fitsio.h"
