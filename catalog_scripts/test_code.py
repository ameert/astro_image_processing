from scipy.interpolate import dfitpack
try:
    dfitpack.sproot(-1, -1, -1)
except Exception, e:
    dfitpack_error = type(e)
    print Exception
    print e
    print type(e)
    
try:
    dfitpack.sproot(-1, -1, -1)
except dfitpack_error:
    print "Got it!"
