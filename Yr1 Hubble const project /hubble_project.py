#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 20:43:49 2022

@author: zainmughal

~~all of my old code is kept and collated at the bottom (not in order)~~
"""

import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
import scipy as sp 
import scipy.optimize 

params={'figure.figsize': [15, 10]}
plt.rcParams.update(params)

Halpha_data=np.array(pd.read_csv(r'/Volumes/Zain_mughal/Halpha_spectral_data.csv',delimiter=',',skiprows=3)) #this imports the spectral data set,skipping out the top comments and observation numbers 
obvs_num=np.loadtxt('/Volumes/Zain_mughal/Halpha_spectral_data.csv',delimiter=',',skiprows=2,max_rows=1) # this will create a 1D array of the observation numebrs from the top of the spectral data in the order given
noisy_obvs_num=np.loadtxt('/Volumes/Zain_mughal/Halpha_spectral_data.csv',delimiter=',',skiprows=2) # this is not needed, but i found it easier to work with it this way, it is the same as teh Halpha_data variable but has the observation numbers at the top

Distance_Mpc=np.loadtxt('/Volumes/Zain_mughal/Distance_Mpc.txt',delimiter='\t',skiprows=2) #loads in the distance data, all 3 columns
distances = Distance_Mpc[:,1] # extracts only the distances values from teh distance_Mpc data set

def fit_func(x,a,mu,sig,m,c): # fucntion defioned to return the fitted values later on, (college, I. (2022). computing worksheet 2 example solutions. [online] blackboard/jupyter. Available at: https://bb.imperial.ac.uk/bbcswebdav/pid-2659689-dt-content-rid-13319862_1/xid-13319862_1 [Accessed 19 Nov. 2022].)
    gaus = a*np.exp(-((x-mu)**2)/(2*sig**2)) #gaussian curve formula    
    peak_value = np.max(gaus)  # this retrieves the peak values of the gaussian fit, this will be used later as the frequency values
    for i in range(len(gaus)):
        if gaus[i]==peak_value:
            global x_max_gaus # global allows me to access it at any point in the program
            x_max_gaus= px[i] # saves the corresponding x values of the peak 
    line = m*x+c 
    return gaus + line

clean_distances = Distance_Mpc # copy the data set before cleaning the values to avoid errors
to_delete=[]  # assigns empty list to be used later as the bad observation numbers

cuts = 0 # very important variable used later, makes sure indexes are still in range and has to be reset before use
for i in range(30):
    cuts= len(to_delete)
    valid_response=int(Distance_Mpc[:,2][i]) # saves the 0 or 1 values, if observation is accurate or not
    if valid_response==0: # if the observation needs to be discared due to faulty readings, this will delete (clean) the data 
        clean_distances = np.delete(clean_distances,i-cuts,0) # overwrites the data set with new cleaned data every iteration
        to_delete.append(Distance_Mpc[:,0][i])  # records all the bad observations, will later be used to clean other data
        observation_num = int(Distance_Mpc[:,0][i]) # records current bad observation 
        step = 0 
        for j in range(60):
            if int(obvs_num[j])==int(observation_num): # checks if the bad observations are present in the wider spectral data
                clean_data = np.delete(Halpha_data,j,axis=1) # if bad observations are present, it will delete and save the new 'clean' spectral data in a new variable
         
obvs_num = np.unique(obvs_num) # this has repeated observation values, so this function will remove repeats
obvs_num = np.sort(obvs_num) # sorts the observation numbers in ascending order
cuts=0 
for k in range(25):
    for l in range(5):
        if int(obvs_num[k])==int(to_delete[l]): #checks if bad observations are still present and will delete them if so 
            obvs_num = np.delete(obvs_num,k,0)
ordered_c_data = np.empty([1001,50]) # make an empty array to store filtered spectral data in 
index = 0 # as the spectral data has adjacent grouped values, and not all will be recorded, need to allow for some to be skipped
for i in range(len(obvs_num)):     
    for j in range(60):
        if int(obvs_num[i])==int(noisy_obvs_num[:,j][0]): #checks for all good observations in the broad data set, and saves the good ones in the new clean variable
            ordered_c_data[:,index] = noisy_obvs_num[:,j]
            index+=1 # for every save this has to increment so frequecny and spectra are considered
ordered_c_data = np.delete(ordered_c_data,0,0) # deletes the row of observation values as is not needed
ostring=[]         

ordered_clean_distances = np.empty([25,3]) # empty array created
for i in range(25):
    for j in range(25):
        if obvs_num[i]==clean_distances[:,0][j]: #checks for good distances and recoreds those in order, as obvs_num is ordered so index i will be in order
            ordered_clean_distances[i,:]=clean_distances[j,:]            

# constants and empty arrays defined before the for loop
velocities = []
frequncies =[]
c_l = 2.9979e8
lambda_e = 656.28e-9
freq_frac_error=[]
vel_error=[]
step=0 
for i in range(25):    
    px=ordered_c_data[:,step] # takes the frequecny colums from large data set, steps is used as each observation is 2 columns away
    py=ordered_c_data[:,step+1] # takes spectra columns 
    px=np.multiply(px,(1e-12)) # convert from Hz to THz
    plt.grid()
    plt.xlabel('frequency (THz)')
    plt.ylabel('intensity (arbitrary units)')
    title_string= str('observation '+str(obvs_num[i])+' graph') # gives the title of graph with the observation number
    plt.title(title_string)
    m,c=np.polyfit(px,py,deg=1) # cacluates the gradient and y intercepts of the dataset
    plt.plot(px,py,'*',color='green') # scatter plot of the raw spectra and freqeuncy values
    y_mean = np.mean(py) # use the y_mean for better initial guess value
    initial_guess=[y_mean,100,1000,m,c] # guess value to bes passed into curvefit function, obtained by reading and analising graph values
    po,po_cov=sp.optimize.curve_fit(fit_func,px,py,initial_guess,maxfev=100000)  # had to increase the amount of trials, as i had a wide range for initial guess 
    freq_error=po_cov[1,1]**0.5   #the absolute error in x (frequency) is the [1,1] value of the covariance matrix returned from curvefit
    freq_pe_error=freq_error/po[1]    # converts absolute error into fractional
    freq_frac_error.append(freq_pe_error) # adds the fractional frequency error to list to be used later  
    plt.plot(px,fit_func(px,po[0],po[1],po[2],po[3],po[4]),label='Fit results',color='red') # plots the fitted curve from the coefficients calculated from curvefit
    plt.legend()
    global x_max_gaus
    frequency =x_max_gaus *(1e12) # convert back to Hz
    frequncies.append(frequency) # make list of freqeuncies to make table and check values later, not needed
    lambda_o = c_l/frequency  # using c=f*lambda
    wavelength_ratio = lambda_o/lambda_e #rearranging equation 
    v = c_l * ((((wavelength_ratio)**2)-1)/(((wavelength_ratio)**2)+1)) # velocity calucations, forulma rearranged for V
    velocities.append(v) # makes list of v values to be plotted later
    step+=2 # the index value to be used as x and y index from teh Halpha data need to increment in 2's as one observation is 2 columns
    plt.show()
    
v_check=np.empty([25,4]) # empty array, this is for checking my own data and values 
for i in range(25):
    v_check[:,0][i]=int(obvs_num[i]) 
    v_check[:,1][i]=int(frequncies[i])
    v_check[:,2][i]=int(velocities[i])
    v_check[:,3][i]=ordered_clean_distances[:,1][i]
velocities_kms = np.array(velocities)  # make new km/s velocities and convert normal list to numpy array so can perform mathmatical function onto it easily 
velocities_kms = velocities_kms/1000  #  convert m/s to km/s
freq_frac_error=np.array(freq_frac_error) #np array is easier to perform maths on 
vel_error=2*freq_frac_error*velocities_kms  # the error in velocity is 2 times the error in frequency, times this by velocities to get an array of absolute velocity errors
final_fit,final_fit_cov=np.polyfit(ordered_clean_distances[:,1],velocities_kms,1,w=1/vel_error,cov=True) # gets gradient and y intercept values, the gradient is equivelent to hubble's constant 
y1 = final_fit[0] * ordered_clean_distances[:,1] + final_fit[1]  #y = m*x +c  fitted line as a plt.plot makes a weird looking graph for me although my data is ordered and correct 
plt.errorbar(ordered_clean_distances[:,1],velocities_kms,fmt='*')#,yerr=vel_error,capsize=1) # error values for velocities, i cannot plot this as one of grpahs is not curvefitted properly and produces a huge error  
plt.plot(ordered_clean_distances[:,1],y1) # plots the linear y=mx+c line calculated 3 lines up
hubbles_string = str('hubbles constant (gradient) is, '+str(f"{final_fit[0]:.3}")+" ± "+str(f"{(np.sqrt(final_fit_cov[0,0])):.2}")+' Km/s Mpc')
print(hubbles_string)
plt.text(200,30000,hubbles_string,fontsize = 'xx-large') # prints the obtained Hubble's constant (gradient) value on the graph plot 
plt.xlabel('Distance (Mpc)',fontsize='x-large')
plt.ylabel('Redshift (Km/s)',fontsize='x-large')
plt.grid()
plt.title('graph of redshifted velocities against distances of observed galaxies',fontsize='xx-large')
plt.savefig('/Volumes/Zain_mughal/hubble project final plot.png')
plt.show()




r'''
~~ old commented cod, not in order~~


#Halpha_data = np.loadtxt("/Volumes/Zain_mughal/computing/computing_hubble_project/Data/Halpha_spectral_data.csv",skiprows=4, delimiter=',')
#Halpha_data = np.array((np.loadtxt('/Volumes/Zain_mughal/Halpha_spectral_data.csv',dtype=object,skiprows=4,delimiter=',')))
#
#Halpha_data=np.array(pd.read_csv(r'/Volumes/Zain_mughal/Halpha_spectral_data.csv',delimiter=',',skiprows=3))
#Distance_Mpc=np.loadtxt('/Volumes/Zain_mughal/Distance_Mpc.txt',delimiter='\t',skiprows=2)
#obvs_num=pd.read_csv(r'/Halpha_spectral_data.csv',delimiter=',',skiprows=2,nrows=1)


#obvs_num = np.array(Halpha_data_obvs_num.loc[])
#obvs_num=pd.DataFrame(obvs_num)
#print(Halpha_data_obvs_num)~
#print(obvs_num[0   


        #print('to delete should append : ',Distance_Mpc[:,0][i])

            #print(obvs_num[k],'and',to_delete[l],'and',k)


#valid_response=int(Distance_Mpc[:,2][i])



for i in range(30):
    
    #print('valid', valid_response)
    if valid_response == 0:
        observation_num = int(Distance_Mpc[:,0][i])
        #print('observation num: ',observation_num)
        step = 0 
        #print('the valid loop works')
        for j in range(60):
            #print('the j loop works')
            #print('j value: ',j)
            #print(obvs_num[j],'/n',observation_num)
            if int(obvs_num[j])==int(observation_num):
                #print('he dies')
                #print(obvs_num[j],'and the observed killer ',observation_num,'and j is: ',j)
          
                clean_data = np.delete(Halpha_data,j,axis=1 )
                
                
                #print(Halpha_data)
                #deleted=[]
                #print(Halpha_data_obvs_num[j][0])
#print(Distance_Mpc)


 
#print('clean distances are: ',clean_distances)
#print(len(clean_distances)

    #print('x: ',px,'\ny: ',py)

    #plt.scatter(px,py)  


 #peaks=scipy.signal.find_peaks(py,prominence=30)
 #print('peaks',peaks)
 #y_error=[]

 
 for j in range(len(py)):
     y_error.append(np.std(py))
     po,po_cov=sp.curve_fit(fit_func,px,py)
     #plt.plot(px,fit_func(px,po[0],po[1],po[2],po[3],po[4]),label='Fit results',color='green')

 #plt.plot(px,c+m*px,'-',color='blue')
 #print('The slope and intercept of the regression is,', m,c)
 #residuals_y = py - (m*px + c)
 #plt.plot(px,py-residuals_y,color='red')


  # print('peerror',freq_pe_error)
  # print('frefracerr',freq_frac_error)
  #       print(po[1])
  
  
  print('po cov ',po_cov)
  print("The signal parameters are")
  print(" Gaussian amplitude = %.1f +/- %.1f" %(po[0],np.sqrt(po_cov[0,0])))

  print(" mu = %.1f +/- %.1f"%(po[1],np.sqrt(po_cov[1,1])))
  
  print(" Gaussian width (sigma) = %.1f +/- %.1f"%(po[2],np.sqrt(po_cov[2,2])))
  print("and the background estimate is")
  print(" m = %.2f +/- %.2f"%(po[3],np.sqrt(po_cov[3,3])))
  print(" c = %.0f +/- %.0f"%(po[4],np.sqrt(po_cov[4,4])))
  
#print(x_max_gaus)
#print(x_max_gaus)
#initial_guess=[px,a,mu,sig,m,c]


  #print(lambda_o)
  #print('lambda 0 values: ',lambda_o)
 # velocity = c_l * (((lambda_o)**2)-((lambda_e)**2))/((((lambda_o)**2)+((lambda_e)**2)))
  #velocities.append(velocity)
  #plt.errorbar(px,py,yerr=y_error, fmt='o',label="Input Data",capsize=2)
  
  #print(wavelength_ratio)
  #print('this is lambda o: ',lambda_o,'and lambda e :',lambda_e)
  #print('this is wavelength ratio :',wavelenght_ratio )
  
  #print('v_check is: ',v_check)

# freq_mean = np.mean(frequncies)
# pe_freq = frequency_error/freq_mean

#print('freq std is: ',pe_freq)


#print('d: ',clean_distances[:,0],'\n v: ',velocities)
#print(len(ordered_c_data[:,0]),len(velocities))
# plt.scatter(ordered_clean_distances[:,1],velocities_kms) # plots the disntance against velocity graph as V=H_0 * D

    #print(v_check[:,0][i],obvs_num[i] )    


# uncertainty=pe_freq*4*m1

#print('hubbles constannt unc: ',pe_freq*m1*4)



step=0 
for i in range(60):
    current_graph_array=[[],[]]
    np.array(current_graph_array)
    for j in range(1000):
        px=Halpha_data[step]
        py=Halpha_data[step+1]
        current_graph_array[0].append(px)
        current_graph_array[1].append(py)
    step+=2
    print('hello',current_graph_array)
    #plt.plot(current_graph_array[0],current_graph_array[1])
    #plt.show() 
'''
