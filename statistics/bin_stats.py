import numpy as np
import pylab as pl
from scipy.misc import comb
import scikits.bootstrap as bootstrap  

class bin_stats:
    """class used to find mean, median, and 1-sigma of binned data"""

    def __init__(self, x_pos, data, bins, low_dat, high_dat, weight = [1], err_type = 'median', nsamples = 10000):
        self.err_type = err_type
        self.x_pos = np.array(x_pos)
        self.data = np.array(data)
        self.bins = np.array(bins)
        self.dat_range = [low_dat, high_dat]
        self.nsamples = nsamples

        if len(weight) != len(data):  # weight everything equally 
            print 'no weight or improper weight supplied...weighting equally'
            weight = np.ones_like(data)
        else:
            weight = np.array(weight) 
            
        self.digits = np.digitize(self.x_pos, self.bins)
        
        if len(self.bins) <2:
            print "You must have at least one complete bin (bin array needs at least 2 endpoints) or this will fail terribly\n\n\n"
            return

        if self.dat_range[0] != self.dat_range[1]:
            x_pos = np.extract(data <= self.dat_range[1], x_pos)
            weight = np.extract(data <= self.dat_range[1], weight)
            data = np.extract(data <= self.dat_range[1], data)
            self.x_pos = np.extract(data >= self.dat_range[0], x_pos)
            self.weight = np.extract(data >= self.dat_range[0], weight)
            self.data = np.extract(data >= self.dat_range[0], data)
        
        self.bin_mean = []
        self.bin_median = []
        self.bin_median2 = []
        self.bin_stdev = []
        self.bin_med95ci = []
        self.bin_68 = [ [],[], [], [],[],[], [], [] ]
        self.bin_95 = [ [],[], [],[],[],[], [], [] ]
        self.bin_99 = [ [],[],[],[],[],[], [], [] ]
        self.bin_ctr = []
        self.bin_number = []

        self.calc_binstats()
    
        #print self.bin_68
        self.bin_mean = np.array(self.bin_mean)
        self.bin_median =  np.array(self.bin_median)
        self.bin_stdev =  np.array(self.bin_stdev)
        self.bin_med95ci = np.array(self.bin_med95ci)
        self.bin_68 = np.array(self.bin_68)
        self.bin_95 = np.array(self.bin_95)
        self.bin_99 = np.array(self.bin_99)
        self.bin_ctr = np.array(self.bin_ctr)
        self.bin_number = np.array(self.bin_number)
        return


    def calc_binstats(self):
        
        for curr_num in range(len(self.bins)-1):
            curr_data = np.extract(self.x_pos > self.bins[curr_num], self.data)
            curr_weight = np.extract(self.x_pos > self.bins[curr_num], self.weight)
            
            curr_x_pos = np.extract(self.x_pos > self.bins[curr_num], self.x_pos)
            curr_data = np.extract(curr_x_pos <= self.bins[curr_num+1], curr_data)
            curr_weight = np.extract(curr_x_pos <= self.bins[curr_num+1], curr_weight)
            self.bin_ctr.append((self.bins[curr_num]+self.bins[curr_num+1])/2.0)
            self.bin_number.append(len(curr_data))
            self.do_bin(curr_data, curr_weight, self.err_type)

        return

    def get_val(self, data, weights, percentile):
        indicies = np.argsort(data)
        sdata = data[indicies]
        sweights = weights[indicies]/np.sum(weights)
        cumweight = np.cumsum(sweights)
        pos = np.where(cumweight<=percentile)[0]
        if len(pos)<1:
            pos = 0
        else:
            pos = np.max(pos)
        return sdata[pos]

    def med_bootstrap(self, alldata):
        percentile = 0.5
        data = np.array(alldata[:,0])
        weights = np.array(alldata[:,1])
        
        indicies = np.argsort(data)
        sdata = data[indicies]
        sweights = weights[indicies]/np.sum(weights)
        cumweight = np.cumsum(sweights)
        pos = np.where(cumweight<=percentile)[0]
        if len(pos)<1:
            pos = 0
        else:
            pos = np.max(pos)
        return sdata[pos]

    def mean_bootstrap(self, alldata):
        data = np.array(alldata[:,0])
        weights = np.array(alldata[:,1])
        
        return np.sum(data*weights)/np.sum(weights)
        
    def pi_vals(self, num):
        i = np.arange(0,num+1,1)
        i = i.astype(int)
        pi = 2**(-num)*comb(num, i)
        #factorial(num)
        #ifac = factorial(i)
        #nifac = factorial(num - i)
        #pi = pi/(ifac*nifac)
        print "pi"
        print pi
        return pi

    def bracket(self, pi_vals, ci, median_loc):
        loc_floor = int(np.floor(median_loc))
        loc_round = int(np.round(median_loc))
        if median_loc - loc_floor > 0.1:
            ci_indexes = np.array([loc_floor, loc_floor+1], dtype = int)
        else:
            ci_indexes = np.array([loc_round-1, loc_round + 1], dtype = int)

        bracket_val = np.sum(pi_vals[ci_indexes[0]:ci_indexes[1]])
        print pi_vals[ci_indexes[0]:ci_indexes[1]]
        print bracket_val
        while bracket_val < ci:
            ci_indexes += np.array([-1,1])
            bracket_val = np.sum(pi_vals[ci_indexes[0]:ci_indexes[1]])
            print pi_vals[ci_indexes[0]:ci_indexes[1]]
            print bracket_val
        return ci_indexes

    def get_median_ci(self, data, ci):
        ci_vals = bootstrap.ci(data=data, statfunction=get_val, n_samples = self.nsamples)
        return ci_vals
    
    def getmed95ci(self, curr_data, curr_weight):
        num_obj = float(len(curr_data))
        low = (num_obj/2.0 -1.96*np.sqrt(num_obj)/2.0)/num_obj
        high = (1.0+num_obj/2.0 +1.96*np.sqrt(num_obj)/2.0)/num_obj


        return (self.bin_median[-1]-self.get_val(curr_data, curr_weight, low),self.get_val(curr_data, curr_weight, high)-self.bin_median[-1])


    def do_bin(self, curr_data, curr_weight, err_type):
        # calculate bin statistics
        if len(curr_data)>5:
            self.bin_mean.append(np.sum(curr_data*curr_weight)/np.sum(curr_weight))
            self.bin_stdev.append(np.sqrt(np.sum(curr_weight*(self.bin_mean[-1] - curr_data)**2.0)/np.sum(curr_weight)))
            
            self.bin_median.append(self.get_val(curr_data, curr_weight, 0.5))

            self.bin_med95ci.append(self.getmed95ci(curr_data, curr_weight))
            end_pts = []
            
            if err_type == 'median':
                cifunction = self.med_bootstrap
                center = self.bin_median[-1]
                for percentile in [0.005, 0.025, .16, .84,.975, .995]: 
                    end_pts.append(self.get_val(curr_data, curr_weight, percentile))
                    
            elif err_type == 'mean':
                cifunction = self.mean_bootstrap
                center = self.bin_mean[-1]
                bot_bin = np.extract(curr_data <= self.bin_mean[-1],curr_data)
                bb_weight = np.extract(curr_data <= self.bin_mean[-1],curr_weight)
                for percentile in [0.01, 0.05, .32]: 
                    end_pts.append(self.get_val(bot_bin, bb_weight, percentile))
               
                top_bin = np.extract(curr_data >= self.bin_mean[-1],curr_data)
                tb_weight = np.extract(curr_data >= self.bin_mean[-1],curr_weight)
                for percentile in [.68,.95, .99]: 
                    end_pts.append(self.get_val(curr_data, curr_weight, percentile))

            ci_data = zip(curr_data, curr_weight)

            self.bin_68[0].append(center - end_pts[2])
            self.bin_68[1].append(end_pts[3] - center)
            self.bin_68[2].append(end_pts[2])
            self.bin_68[3].append(end_pts[3])

            #cis = bootstrap.ci(data=ci_data, statfunction= cifunction, alpha = .32, n_samples = self.nsamples)
            cis = [self.get_val(curr_data, curr_weight, .5 -.32),self.get_val(curr_data, curr_weight, .5 +.32)]
            #self.bin_68[4].append(center - cis[0])
            #self.bin_68[5].append(cis[1] - center)
            #self.bin_68[6].append(cis[0])
            #self.bin_68[7].append(cis[1])
            self.bin_68[4].append((center - cis[0])/np.sqrt(len(curr_data)))
            self.bin_68[5].append((cis[1] - center)/np.sqrt(len(curr_data)))
            self.bin_68[6].append((center - cis[0])/np.sqrt(len(curr_data))+center)
            self.bin_68[7].append((cis[1] - center)/np.sqrt(len(curr_data))+center)
           
            self.bin_95[0].append(center - end_pts[1])
            self.bin_95[1].append(end_pts[4] - center)
            self.bin_95[2].append(end_pts[1])
            self.bin_95[3].append(end_pts[4])
            
            #cis = bootstrap.ci(data=ci_data, statfunction= cifunction , alpha = .05, n_samples = self.nsamples)
            cis = [self.get_val(curr_data, curr_weight, 0.025),self.get_val(curr_data, curr_weight, 0.975)]
#            self.bin_95[4].append(center - cis[0])
#            self.bin_95[5].append(cis[1] - center)
#            self.bin_95[6].append(cis[0])
#            self.bin_95[7].append(cis[1])
            self.bin_95[4].append((center - cis[0])/np.sqrt(len(curr_data)))
            self.bin_95[5].append((cis[1] - center)/np.sqrt(len(curr_data)))
            self.bin_95[6].append((center - cis[0])/np.sqrt(len(curr_data))+center)
            self.bin_95[7].append((cis[1] - center)/np.sqrt(len(curr_data))+center)

            self.bin_99[0].append(center - end_pts[0])
            self.bin_99[1].append(end_pts[5] - center)
            self.bin_99[2].append(end_pts[0])
            self.bin_99[3].append(end_pts[5])

            #cis = bootstrap.ci(data=ci_data, statfunction= cifunction , alpha = .01, n_samples = self.nsamples)
#            self.bin_99[4].append(center - cis[0])
#            self.bin_99[5].append(cis[1] - center)
#            self.bin_99[6].append(cis[0])
#            self.bin_99[7].append(cis[1])
            cis = [self.get_val(curr_data, curr_weight, .005),self.get_val(curr_data, curr_weight, .995)]
            self.bin_99[4].append((center - cis[0])/np.sqrt(len(curr_data)))
            self.bin_99[5].append((cis[1] - center)/np.sqrt(len(curr_data)))
            self.bin_99[6].append((center - cis[0])/np.sqrt(len(curr_data))+center)
            self.bin_99[7].append((cis[1] - center)/np.sqrt(len(curr_data))+center)
            
        else:
            self.bin_mean.append(np.nan)
            self.bin_stdev.append(np.nan)
            self.bin_median.append(np.nan)
            self.bin_med95ci.append((np.nan, np.nan))
            for count in range(0,8):
                self.bin_68[count].append(np.nan)
                self.bin_95[count].append(np.nan)
                self.bin_99[count].append(np.nan)
            
        
        return
    
    def to_log(self, direction):
        if direction == 1:
            con_function = np.log10
            print self.bin_med95ci
            new_binmed95ci = self.bin_median.T[:,np.newaxis]+self.bin_med95ci
            print new_binmed95ci
            self.bin_med95ci = con_function(new_binmed95ci)
            print self.bin_med95ci
            self.bin_med95ci = self.bin_med95ci- con_function(self.bin_median.T[:,np.newaxis])
            print self.bin_med95ci
            #self.bin_med95ci *= np.array([[1,-1],])
            print self.bin_med95ci
            
            
        if direction == -1:
            def con_function(val):
                return 10**(val)
        
        
        self.bin_mean = con_function(self.bin_mean)
        self.bin_median = con_function(self.bin_median)
        self.bin_median2 = con_function(self.bin_median2)
        self.bin_stdev = con_function(self.bin_stdev)
        self.bin_68 = con_function(self.bin_68)
        self.bin_95 = con_function(self.bin_95)
        self.bin_99 = con_function(self.bin_99)

        
        return

    def lay_bounds(self, color='b', lw = 1.5, zorder = 0, 
                   sigma_choice = [68,95,99], shift=0):
        line_st = {68:'--', 95:'-.', 99:':'}
        bins_nm = {68:self.bin_68[2:4], 95:self.bin_95[2:4], 99:self.bin_99[2:4]}
            
        sigs = []
        lines = []
        for a in sigma_choice: 
            sigs.append(bins_nm[a])
            lines.append(line_st[a])
        
        for a, b in zip(sigs, lines):
            for count in [0,1]:
                
                pl.plot(self.bin_ctr,a[count], color=color, linestyle=b, 
                        lw = lw, zorder = zorder)
        
        return

    def plot_ebar(self, ypt, ybar, **kwargs):
        pt_choice = {'median': self.bin_median, 'mean': self.bin_mean }
        pt_error = {'68':self.bin_68[0:2],'95':self.bin_95[0:2], 
                    '99':self.bin_99[0:2],'stdev': self.bin_stdev,
                    '68n':self.bin_68[4:6],'95n':self.bin_95[4:6], 
                    '99n':self.bin_99[4:6], 'med95ci':self.bin_med95ci.T}

        print self.bin_68[4:6]
        print self.bin_med95ci.T
        pl.errorbar(self.bin_ctr, pt_choice[ypt], yerr = pt_error[ybar], **kwargs)
        return



    def write_stats(self, table_name):
        ofile = open(table_name, 'w')
        ofile.write('binctr, bin_num, bin_low, bin_high, mean, stdev, median, 68 CI low, 68 CI high, 95 CI low, 95 CI high, 99 CI low, 99 CI high, 68 data low, 68 data high, 95 data low, 95 data high, 99 data low, 99 data high\n')
        joined_dat =zip(self.bin_ctr, self.bin_number, self.bins[0:-1], 
                        self.bins[1:], self.bin_mean, self.bin_stdev, 
                        self.bin_median, self.bin_68[6], self.bin_68[7],
                        self.bin_95[6], self.bin_95[7],
                        self.bin_99[6], self.bin_99[7],
                        self.bin_68[2], self.bin_68[3],
                        self.bin_95[2], self.bin_95[3],
                        self.bin_99[2], self.bin_99[3])
        for dat in joined_dat:
            str_dat = ['%4.3E' %a for a in dat]
            str_dat = ','.join(str_dat)
            str_dat += '\n'
            ofile.write(str_dat)

        ofile.close()
        return

    
