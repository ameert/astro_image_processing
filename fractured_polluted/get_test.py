import os

a = """122899 
|   251863 
|   588738 
|   385152 
|   597065 
"""

a="""115 
|      162 
|      186 
|      188 
|      194 
|      213 
|      247 
|      326 
|      517 
|      533 
|      665 
|      694 
|      801 
|      806 
|      813
"""

a = a.replace('\n', '')
a = a.replace('|', '')
a = a.split()
a = [int(b) for b in a]
a.sort()

print a

for gal in a:
    print 'getting gal ', gal
    os.system('scp ameert@folio.sas.upenn.edu:/data2/home/ameert/catalog/r/fits/deep/ser/%04d/O_r_%08d_*.fits ./' %((gal-1)/250 +1, gal))
