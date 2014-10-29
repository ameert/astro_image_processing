import os


band = 'i'

path  = '/data2/home/ameert/catalog/%s/plotting/' %band


bad_folders = {}

for folder in range(1, 2684):
    newpath = path + '%04d' %folder
    print 'checking %s' %newpath
    for count in range((folder-1)*250 +1, folder*250+1):
        if not os.path.isfile('%s/%08d_%s_input.fits' %(newpath, count, band)):
            try:
                bad_folders[folder].append(count)
            except KeyError:
                bad_folders[folder]=[count,]


print 'bad_folders'
print sorted(bad_folders.keys())

#print bad_folders
