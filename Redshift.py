# -*- coding: utf-8 -*-
"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Created on Fri May 12 16:03:09 2017
            
Author: Bruno Slaus
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
from Topcat_Exact_Match import exact_match
from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import math
import astropy.units as u

############################################################################
#                    Sliding Parameters:                                   # 
############################################################################
Redshift_Folder          = 'Redshift_Data/'   
Reliability_Match_Folder = 'Matched_Field_Reliability/'
Output_Folder            = 'Output/'  

Exact_Match_Column_1 = 'NUMBER'
Exact_Match_Column_2 = 'NUMBER'


Field_Name_Redshift    = 'North_photoz.fits'
Field_Name_Reliability = 'Matched_REL_Fin.fits'

N_Bins       = 10

#Input fits file columns
Input_ID_Column   = 'Id'               #Radio Source ID
Input_z_Column    = 'Z_BEST'           #Redshift
Input_Flux_Column = 'Total_Flux'       #Flux 
Input_SpIn_Column = 'Alpha'            #Spectral index 

#Output fits file columns
Output_ID_Column   = 'Source_Id'               #Radio Source ID
Output_z_Column    = 'Z_BEST'           #Redshift
Output_Flux_Column = 'Total_Flux_corr'  #Flux 
Output_SpIn_Column = 'Spectral_Index'   #Spectral index 
############################################################################
print('\n******************************')
print('Starting the Redshift.py code.')
print('******************************\n')

Field_1 = Redshift_Folder          + Field_Name_Redshift
Field_2 = Reliability_Match_Folder + Field_Name_Reliability
print('Field_1      = ',Field_1)
print('Field_2      = ',Field_2)



#Matching the two fields
print('\n\n********************\nPART 1: MATCHING THE FIELDS:')
exact_match(
    Field_1,
    Exact_Match_Column_1,
    Field_2,
    Exact_Match_Column_2,
    Output_Folder+'Data_z.fits')

Data_z         = fits.open(Output_Folder+'Data_z.fits')[1].data
Redshift       = Data_z[Input_z_Column]

Redshift_Histo_y, Redshift_Histo_x  = np.histogram(Redshift, bins=N_Bins)
Redshift_Histo_x                    = Redshift_Histo_x[:-1]

fig = plt.figure()
ax = fig.add_axes([0.1,0.1,0.8,0.8])
plt.step(Redshift_Histo_x, Redshift_Histo_y, where='post', color='red')
plt.xlabel('Redshift')
plt.ylabel('N')
plt.title('Histogram_Redshift')
#plt.vlines(Limit, -10, 30, color='red')
plt.savefig('Output/Histogram_Redshift.png')
plt.close() 

#Creating table for easy LF calculations
Col1  = fits.Column(name=Output_ID_Column,   array=Data_z[Input_ID_Column],   format='D')
Col2  = fits.Column(name=Output_z_Column,    array=Data_z[Input_z_Column],    format='D')
Col3  = fits.Column(name=Output_Flux_Column, array=Data_z[Input_Flux_Column], format='D')
Col4  = fits.Column(name=Output_SpIn_Column, array=Data_z[Input_SpIn_Column], format='D')
Columns = fits.ColDefs([Col1, Col2, Col3, Col4])
Fits_File = fits.BinTableHDU.from_columns(Columns)
Fits_File.writeto('Output/Data_LF.fits', overwrite=True)

print('\n******************************')
print('FINISH: Ending the code.')
print('******************************\n')

