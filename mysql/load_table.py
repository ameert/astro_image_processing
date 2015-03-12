from astro_image_processing.mysql import *

def load_table(cursor, table_name, file_name, columns, column_types, delimiter = ',', make_table = 1):
    if make_table:
        cmd = 'create table %s (%s %s);' %(table_name,columns[0], column_types[0])
        cursor.execute(cmd)
        for col_n, col_t in zip(columns[1:], column_types[1:]):
            cmd = 'ALTER TABLE '+table_name+ ' add column '+col_n+' '+col_t+' default -888;'
            print cmd       
            cursor.execute(cmd)
   
    cmd_stem = 'insert ignore into %s (%s) value (' %(table_name,','.join(columns))

    fip = open(file_name)

    for line in fip.readlines():
        if line[0] not in '#':
            if delimiter == ' ':
                line = ','.join(line.split())
            # if an entry is a string
            #line = line.split(',')
            #line[1] = "'"+line[1]+"'"
            #line = ','.join(line)
            line = line.replace('NaN', '-999')
            line = line.replace('null', '-888')
            cmd = cmd_stem + line + ');'
            #print cmd
            cursor.execute(cmd)
        else:
            print 'skipping line: ' + line
            
    fip.close()
