import numpy as np

class bin_stats:
    """class used to find mean, median, and 1-sigma of binned data"""

    def __init__(self, x_pos, data, bins, low_dat, high_dat, weight = [1], err_type = 'median'):
        self.err_type = err_type
        self.x_pos = np.array(x_pos)
        self.data = np.array(data)
        self.bins = np.array(bins)
        self.dat_range = [low_dat, high_dat]
        if len(weight) != len(data):  # weight everything equally 
            print 'no weight or improper weight supplied...weighting equally'
            weight = np.ones_like(data)
        else:
            weight = np.array(data) 
            
        self.digits = np.digitize(self.x_pos, self.bins)
        
        if len(self.bins) <2:
            print "You must have at least one complete bin (bin array needs at least 2 endpoints) or this will fail terribly\n\n\n"
            return

        print 'max ', np.max(data)
        print 'min ', np.min(data)
        print 'num ', len(data)

        if self.dat_range[0] != self.dat_range[1]:
            x_pos = np.extract(data <= self.dat_range[1], x_pos)
            weight = np.extract(data <= self.dat_range[1], weight)
            data = np.extract(data <= self.dat_range[1], data)
            self.x_pos = np.extract(data >= self.dat_range[0], x_pos)
            self.weight = np.extract(data >= self.dat_range[0], weight)
            self.data = np.extract(data >= self.dat_range[0], data)

        print data
        print 'max ', np.max(self.data)
        print 'min ', np.min(self.data)
        print 'num ', len(self.data)
        
        self.bin_mean = []
        self.bin_median = []
        self.bin_stdev = []
        self.bin_66 = [ [],[] ]
        self.bin_95 = [ [],[] ]
        self.bin_99 = [ [],[] ]
        self.bin_ctr = []

        self.calc_binstats()
    
        self.bin_mean = np.array(self.bin_mean)
        self.bin_median =  np.array(self.bin_median)
        self.bin_stdev =  np.array(self.bin_stdev)
        self.bin_66 = np.array(self.bin_66)
        self.bin_95 = np.array(self.bin_95)
        self.bin_99 = np.array(self.bin_99)
        self.bin_ctr = np.array(self.bin_ctr)
        return


    def calc_binstats(self):
        
        for curr_num in range(len(self.bins)-1):
            curr_data = np.extract(self.x_pos > self.bins[curr_num], self.data)
            curr_weight = np.extract(self.x_pos > self.bins[curr_num], self.weight)
            
            curr_x_pos = np.extract(self.x_pos > self.bins[curr_num], self.x_pos)
            curr_data = np.extract(curr_x_pos <= self.bins[curr_num+1], curr_data)
            curr_weight = np.extract(curr_x_pos <= self.bins[curr_num+1], curr_weight)
            self.bin_ctr.append((self.bins[curr_num]+self.bins[curr_num+1])/2.0)

            self.do_bin(curr_data, curr_weight, self.err_type)

        return
        
    def do_bin(self, curr_data, curr_weight, err_type):
        
        # calculate bin statistics
        if len(curr_data)>5:
            self.bin_mean.append(np.average(curr_data, weights = curr_weight))
            self.bin_stdev.append(np.sqrt(1.0/np.sum(curr_weight)))
            self.bin_median.append(np.median(curr_data))
        else:
            self.bin_mean.append(-999)
            self.bin_stdev.append(-999)
            self.bin_median.append(-999)
        
        if err_type == 'median':
            # now calculate the 1,2,3
            top_bin = np.extract(curr_data >= self.bin_median[-1],curr_data)
            bot_bin = np.extract(curr_data <= self.bin_median[-1],curr_data)

            top_bin = np.sort(top_bin)
            bot_bin = np.sort(bot_bin)
            bot_bin = bot_bin[::-1]
            if len(top_bin) > 3:
                top_66 = top_bin[np.round((0.6827 * len(top_bin)) -1)]-np.median(curr_data)
                top_95 = top_bin[np.round((0.9545 * len(top_bin)) -1)]-np.median(curr_data)
                top_99 = top_bin[np.round((0.9973 * len(top_bin)) -1)]-np.median(curr_data)
            else:
                top_66 = np.nan
                top_95 = np.nan
                top_99 = np.nan
                
            if len(bot_bin) > 3:
                bot_66 = np.median(curr_data)-bot_bin[np.round((0.6827 * len(bot_bin)) -1)] 
                bot_95 = np.median(curr_data)-bot_bin[np.round((0.9545 * len(bot_bin)) -1)]
                bot_99 = np.median(curr_data)-bot_bin[np.round((0.9973 * len(bot_bin)) -1)]
            else:
                bot_66 = np.nan
                bot_95 = np.nan
                bot_99 = np.nan
            
        elif err_type == 'mean':
            # now calculate the 1,2,3
            top_bin = np.extract(curr_data >= self.bin_mean[-1],curr_data)
            bot_bin = np.extract(curr_data <= self.bin_mean[-1],curr_data)
            
            top_bin = np.sort(top_bin)
            bot_bin = np.sort(bot_bin)
            bot_bin = bot_bin[::-1]
            if len(top_bin) > 3:
                top_66 = top_bin[np.round((0.6827 * len(top_bin)) -1)]-np.mean(curr_data)
                top_95 = top_bin[np.round((0.9545 * len(top_bin)) -1)]-np.mean(curr_data)
                top_99 = top_bin[np.round((0.9973 * len(top_bin)) -1)]-np.mean(curr_data)
            else:
                top_66 = np.mean(curr_data)
                top_95 = np.mean(curr_data)
                top_99 = np.mean(curr_data)

            if len(bot_bin) > 3:
                bot_66 = np.mean(curr_data)-bot_bin[np.round((0.6827 * len(bot_bin)) -1)] 
                bot_95 = np.mean(curr_data)-bot_bin[np.round((0.9545 * len(bot_bin)) -1)]
                bot_99 = np.mean(curr_data)-bot_bin[np.round((0.9973 * len(bot_bin)) -1)]
            else:
                bot_66 = np.mean(curr_data)
                bot_95 = np.mean(curr_data)
                bot_99 = np.mean(curr_data)
            

        self.bin_66[0].append(bot_66)
        self.bin_66[1].append(top_66)
        self.bin_95[0].append(bot_95)
        self.bin_95[1].append(top_95)
        self.bin_99[0].append(bot_99)
        self.bin_99[1].append(top_99)

        return
    

    
    
