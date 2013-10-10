import subprocess as sub
import pickle

def exec_cmd(job_str):
    p1=sub.Popen(job_str, shell=True, stdout = sub.PIPE)
    output = p1.communicate()[0]
    output = output.strip()
    return output

def IsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def pickle_data(data, filename):
    a = open(filename, 'w')
    pickle.dump(data,a)
    a.close()
    return

def un_pickle_data(filename):
    a = open(filename)
    data = pickle.load(a)
    a.close()
    return data

def send_mail(comp_job, address = 'none'):
    cmd = """echo "pymorph %s job complete" | mail -s "pymorph %s job complete" %s""" %(comp_job, comp_job, address)
    exec_cmd(cmd)
    return

