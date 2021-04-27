import topas2numpy as t2np
import numpy as np
import os, errno, argparse

from scipy.signal import savgol_filter


######################

#convolve 1/smoothing_parameter with function

def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y,box,mode='same')
    return y_smooth

    
#filename still stored as variable, so used as memory prep and preallocation
    

class TOPAS_PDD:
    def __init__(self,file):
        
        self.cyl1 = t2np.BinnedResult(file)
        
        self.depth = np.flip(self.cyl1.dimensions[2].get_bin_centers())
        self.step_size = self.depth[0]-self.depth[1]
        
        self.sum_dose = np.squeeze(self.cyl1.data["Sum"])
        self.counts_in_bin = np.squeeze(self.cyl1.data["Count_in_Bin"])
        self.index_2cm = -int( len(self.depth) * 2 / (self.depth[0]+self.step_size/2))
        self.mid_voxel_ref_depth = self.depth[self.index_2cm]


class TOPAS_combined_PDD:
    def __init__(self,filelist):
        
        self.filelist = filelist
        self.cyl1 = t2np.BinnedResult(filelist[0])
        
        self.depth = np.flip(self.cyl1.dimensions[2].get_bin_centers())
        self.step_size = self.depth[0]-self.depth[1]
        self.index_2cm = -int( len(self.depth) * 2 / (self.depth[0]+self.step_size/2))
        self.mid_voxel_ref_depth = self.depth[self.index_2cm]
        
 

    def combine_PDDs(self):
        
        self.all_pdds = [TOPAS_PDD(x) for x in self.filelist]
        # Iterate and collate data from all objects    
        self.sum_dose = sum([x.sum_dose for x in self.all_pdds])
        self.counts_in_bin = sum([x.counts_in_bin for x in self.all_pdds])
        
        #Create combined pdd, normalised to 2 cm depth
        self.pdd_combined = self.sum_dose/self.sum_dose[self.index_2cm]*100
        
        #Iterate through dictionary and add numpy arrays (element wise addition)
        self.sum_dose_data = np.asarray([self.depth, self.sum_dose, self.counts_in_bin])
        self.pdd_combined_data = np.asarray([self.depth, self.pdd_combined, self.counts_in_bin])
        

            

    def apply_smoothing(self, span=5, poly_order=1):
        
        # Smoothing function convolves over x numbers, which results in issues with (x-1)/2 points near an interface
        # Initialise list without being near discontinuity
        self.smaller_depth = self.depth.T[int((span-1)/2):-int((span-1)/2)]
        self.smaller_counts_in_bin = self.counts_in_bin.T[int((span-1)/2):-int((span-1)/2)]
        
        #How large a period should the function have
        #smoothing_param = int(input("Smoothing Parameter (int): "))
        
        ###########
        #Smooth PDD, renormalise and save to array w/relevant data
        ###########
        self.smoothed_pdd = savgol_filter(self.pdd_combined,2*span+1,poly_order)
        #Renormalising smoothed PDD curve
        self.smoothed_pdd = self.smoothed_pdd/self.smoothed_pdd[self.index_2cm]*100
        self.smoothed_pdd_data = np.asarray([self.depth, self.smoothed_pdd, self.counts_in_bin])

        ###########
        #Smooth Sum Dose, renormalise and save to array w/relevant data  
        ###########
        self.smoothed_sum_dose = savgol_filter(self.sum_dose,2*span-1,poly_order)
        self.smoothed_sum_dose_data = np.asarray([self.depth, self.smoothed_sum_dose, self.counts_in_bin])


        # Reduce list size for PDD
        self.smaller_smoothed_pdd = self.smoothed_pdd.T[int((span-1)/2):-int((span-1)/2)]
        self.smaller_smoothed_pdd_data = np.asarray([self.smaller_depth, self.smaller_smoothed_pdd, self.smaller_counts_in_bin])
        
        # Reduce list size for Sum Dose
        self.smaller_smoothed_sum = self.smoothed_sum_dose.T[int((span-1)/2):-int((span-1)/2)]
        self.smaller_smoothed_sum_data = np.asarray([self.smaller_depth, self.smaller_smoothed_sum, self.smaller_counts_in_bin])


        
        

    def save_and_export(self):
        try:
            os.mkdir('Combined_Results')
            os.chdir('Combined_Results')
            
            self.save_files()
            
        except OSError as e:
            if e.errno == errno.EEXIST:
                print("~~~Check data; directory exists.~~~")
                query = input("Overwrite? (y/n): ")
                if query == "y":
                    os.chdir('Combined_Results')

                    try:
                    	os.remove('*.csv')
                    except:
                    	pass
                    self.save_files()
                    
                else:
                    print("Saving failed...files exist")
                    
    def save_files(self):
        
 		
        
        np.savetxt("sum_dose.csv", self.sum_dose_data.T, delimiter=",")
        
        np.savetxt("pdd_combined.csv", self.pdd_combined_data.T, delimiter=",")
        
        np.savetxt("smoothed_pdd.csv", self.smoothed_pdd_data.T, delimiter=",")
        
        np.savetxt("smoothed_sum_dose.csv", self.smoothed_sum_dose_data.T, delimiter=",")
        
        np.savetxt("cut_down_smoothed_pdd.csv", self.smaller_smoothed_pdd_data.T, delimiter=",")
        
        print ("Great success!")
        
	
   



def main(pdd_directory):
    
    ######################
    
    #Set path to chosen folder for inf
    
    os.chdir("/home/ebutson/TOPAS/kV_CalcBSF/"+pdd_directory)
    
            
    #Create list of file names
    #Could create issue with memory for very large/many files - in which case read and deal with each file individually
    
    global files 
    
    files = [filename for filename in os.listdir() if filename.endswith('.csv')]
    
    global test 
    test = TOPAS_combined_PDD(files)
    test.combine_PDDs()
    print("Combined PDDs...")
    test.apply_smoothing()
    print("Smoothed PDDs...")
    test.save_and_export()


#
if __name__ == "__main__":
    
# =============================================================================
#  Parsing command line argument for directory 
# =============================================================================
 
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir',
                        default='Results/Tests_for_our_kV/200kVp_30cm_3mmBeWindow_1.9mmCuFilter',
                        action='store',
                        dest='result')
    args = parser.parse_args()
    print(args.result)
    
    main(args.result)
