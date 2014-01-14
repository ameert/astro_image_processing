# These functions standardize the flags across all files
import numpy as np

class badflag(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr('Bad flag operation: '+self.value)
 


class flag():
	"""A class that makes handling flags more intuitive"""
	def __init__(self, bit_defs, value = 0):
		"""input is a list of (flag name, bit number) pairs and 
		optionally an initial value of the flag"""

		# initialize the flagvalue
		self.flag_value=value
		
		# initialize the bit counter
		self.bit_counter = 0

		# and the bit dictionary
		self.bit_dict = {}

		# store the flag bit definitions
		for pair in bit_defs:
			self.add_bit(pair)
		
		return

	def add_bit(pair):
		"""adds the bit to the bit dictionary and updates the bit count"""
		return 
	   






   
def GetFlag(flagname):
        FlagDict = dict([('REPEAT', 0),
                         ('FIT_BULGE_CNTR', 1),
                         ('FIT_DISK_CNTR', 2),
			 ('FIT_BULGE', 3),
                         ('FIT_DISK', 4),                         
                         ('FIT_SKY', 5),
			 ('FIT_POINT', 6),
			 ('FIT_BAR', 7),
			 ('NEIGHBOUR_FIT', 8),
                         ('EXCEED_SIZE', 9),
                         ('NO_TARGET', 10),
			 ('ASYM_NOT_CONV', 11),
                         ('ASYM_OUT_FRAME', 12),
                         ('ELLIPSE_FAIL', 13),
                         ('CASGM_FAIL', 14),
                         ('GALFIT_FAIL', 15),
                         ('PLOT_FAIL', 16),
			 ('ERRORS_FAILED', 17),
			 ('AVGIE_FAILED', 18),
                         ('BACK_FAILED', 19),
                         ('DETAIL_FAILED', 20)
                         ])
        return FlagDict[flagname]

def Get_FitFlag(flagname):
        FlagDict = dict([('LARGE_CHISQ', 0),
                         ('SMALL_GOODNESS', 1),
                         ('FAKE_CNTR', 2),
                         ('IE_AT_LIMIT', 3),
                         ('ID_AT_LIMIT', 4),
			 ('RERD_AT_LIMIT', 5),
                         ('BT_AT_LIMIT', 6),
			 ('N_AT_LIMIT', 7),
			 ('RE_AT_LIMIT', 8),
			 ('RD_AT_LIMIT', 9),
			 ('EB_AT_LIMIT', 10),
			 ('ED_AT_LIMIT', 11)
			 ])	                 
        return FlagDict[flagname]

def Get_FinalFlag(flagname):
        FlagDict = dict([('TOTAL FIT', 0),
                         ('m_tot', 1),
                         ('Hrad_corr',2),
                         ('BT', 3),
                         ('m_bulge', 4),
                         ('r_bulge', 5),
                         ('n_bulge', 6),
                         ('ba_bulge', 7),
			 ('pa_bulge', 8),
                         ('m_disk', 9),
                         ('r_disk', 10),
			 ('ba_disk', 11),
			 ('pa_disk', 12),
			 ('neighbor fit', 13)
			 ])	                 
        return FlagDict[flagname]

def isset(flag, bit):
        """Return True if the specified bit is set in the given bit mask"""
        return (flag & (1 << bit)) != 0

def SetFlag(Flag, bit):
	if isset(Flag, bit):
		raise badflag("Tried to set a flag that was already set")
	Flag += 2**bit
	return Flag

def ClrFlag(Flag, bit):
	if not isset(Flag, bit):
		raise badflag("Tried to clear a flag that was not set")
	Flag -= 2**bit
	return Flag
