#!/usr/bin/python
from __future__ import division
import sys
import time
import math
import numpy as np
import scipy as scp
import cmath as cm

def main_seq(ratio2,mult0,mult1,mult2,pickup0,pickup1,pickup2,incct,feederct1,feederct2,\
             tximp,inc_cbtime,inc_highsetpickup,inc_checkBox,\
             fdr1_cbtime,fdr1_highsetpickup,fdr1_checkBox,\
             fdr2_cbtime,fdr2_highsetpickup,fdr2_checkBox,
             inc_curve,fdr1_curve,fdr2_curve):

    resolution=0.01
    Tx_percentage_impedance=tximp
    Tx_impedance_angle=85
    Tx_impedance=complex(cm.rect(Tx_percentage_impedance,math.radians(Tx_impedance_angle)))
    V_base=11000
    MVA_base=20000000 #20MVA transformer
    Z_base=math.pow(V_base,2)/MVA_base

    Z_transformer=Z_base*Tx_impedance/100.0

    Z_loop_impedance=abs(Z_transformer)*ratio2

    Z_loop_impedance_angle=41
    Z_loop=complex(cm.rect(Z_loop_impedance,math.radians(Z_loop_impedance_angle)))


    '''
    Initial conditions
    '''
    i=0
    m=0.5

    ratio=abs(Z_loop/Z_transformer)


    '''
    Declare lists and initialize
    '''
    m_store=[]
    del m_store[:]


    margin_store=[]
    margin_store2=[]
    margin_store3=[]
    margin_store4=[]
    margin_store5=[]
    margin_store6=[]

    ########################################################################

    class CB_Relay(object):
        """This class attempts to define all the parameters surrounding an inverse time overcurrent relay"""

        #----------------------------------------------------------------------
        def __init__(self,TimeMultiplier=0.25,ctratio=400.0,pickup=1.0,curvetype='NI',percent_travel=0.0,\
                     cb_open_time=0.06, highsetpickup=10.0,highset=False):
            """Constructor"""
            self.TimeMultiplier=TimeMultiplier
            self.pickup=pickup
            self.ctratio=ctratio
            self.curvetype=curvetype
            self.percent_travel=percent_travel
            self.tripped=False
            self.pulse_counter=0 #how many pulses of fault current
            self.cb_open_time=cb_open_time  #time in milliseconds
            self.highset=highset
            self.highsetpickup=highsetpickup           
            self.current=[]
            self.current_fdr1_open=[]
            self.current_fdr2_open=[]
            self.time3=[]
            self.time_fdr1_open=[]
            self.time_fdr2_open=[]
            
            
            
            

        def time_to_operate(self,I=2000):
            
            curvetypes=dict(NI=(0.00001399354,0.00010458841,0.99999866576,0.0,0.0),\
                            SI=(0.00001399354,0.00010458841,0.99999866576,0.0,0.0),\
                            VI=(1.0,13.5,1.0,0.0,0.0),\
                            EI=(2.0,80.0,1.0,0.0,0.0),\
                            )
            
            self.I=I
            
            a,b,c,d,e=curvetypes.get(unicode(self.curvetype))

            multiple=(self.I/(self.pickup*self.ctratio))            

            if (self.highset==True and self.I>(self.highsetpickup*self.ctratio)):
                self.time=0.02
            elif self.I>(self.pickup*self.ctratio):
                self.time = self.TimeMultiplier * (d + (b / (math.pow(multiple,a) - c))) + e        
            else:
                self.time=50
                
            return self.time*(1-self.percent_travel)

            
    ###################################################################################################
    '''Instantiation of the feeder objects'''
    '''
    Inc_CT=incct*pickup0
    Inc_TM=mult0

    Fdr_CT1=feederct1*pickup1
    Fdr_TM1=mult1
    
    Fdr_CT2=feederct2*pickup2
    Fdr_TM2=mult2    
   '''
    incomer=CB_Relay(mult0,incct,pickup0,inc_curve,0,inc_cbtime,inc_highsetpickup,inc_checkBox)  #Instantiation of Incomer object
    feederone=CB_Relay(mult1,feederct1,pickup1,fdr1_curve,0,fdr1_cbtime,fdr1_highsetpickup,fdr1_checkBox)  #Instantiation of feederone object
    feedertwo=CB_Relay(mult2,feederct2,pickup2,fdr2_curve,0,fdr2_cbtime,fdr2_highsetpickup,fdr2_checkBox)  #Instantiation of feedertwo object    

    '''Fault calculation functions'''

    def I_total_fault_current_loop(m):
        Z_parallel=1/((1/(Z_loop*m))+(1/((1-m)*Z_loop)))
        I=abs(V_base/math.sqrt(3)/(Z_transformer+Z_parallel))
        return(I)

    #I think we need to develop this to amend what is return based on whether feeder one or feeder two is open.

    def I_total_fault_current_radial(m):
        if feederone.tripped and feedertwo.tripped:
            Z_radial=Z_transformer        
        elif feederone.tripped:
            Z_radial=Z_loop*(1-m)
        elif feedertwo.tripped:
            Z_radial=Z_loop*m
        else:
            pass
        I=abs(V_base/math.sqrt(3)/(Z_transformer+Z_radial))
        return(I)

    #Calculate the currents for the incomer and both feeders 

    for m in np.arange(0.01,1.00,resolution):

        m_store.append(m)
    #First loop -stage 1
        incomer.percent_travel=(0)
        feederone.percent_travel=(0)
        feedertwo.percent_travel=(0)

    #Parallel    
        incomer.current.append(I_total_fault_current_loop(m)) # storage of current values for graphing.
        feederone.current.append(I_total_fault_current_loop(m)*(1-m)) # m is the relative distance from feeder one
        feedertwo.current.append(I_total_fault_current_loop(m)*(m)) # m is te the relative distance from feeder one


        incomer.time3.append(incomer.time_to_operate(I_total_fault_current_loop(m)))
        feederone.time3.append(feederone.time_to_operate(I_total_fault_current_loop(m)*(1-m)))     
        feedertwo.time3.append(feedertwo.time_to_operate(I_total_fault_current_loop(m)*(m))) 

        #Feeder One open
        feederone.tripped=True
        feedertwo.tripped=False

        incomer.current_fdr1_open.append(I_total_fault_current_radial(m))
        feedertwo.current_fdr1_open.append(I_total_fault_current_radial(m)) # m is te the relative distance from feeder one

        incomer.time_fdr1_open.append(incomer.time_to_operate(I_total_fault_current_radial(m))) 
        feedertwo.time_fdr1_open.append(feedertwo.time_to_operate(I_total_fault_current_radial(m))) 

        #Feeder Two Open
        feederone.tripped=False
        feedertwo.tripped=True

        incomer.current_fdr2_open.append(I_total_fault_current_radial(m))
        feederone.current_fdr2_open.append(I_total_fault_current_radial(m)) # m is the relative distance from feeder one

        incomer.time_fdr2_open.append(incomer.time_to_operate(I_total_fault_current_radial(m))) 
        feederone.time_fdr2_open.append(feederone.time_to_operate(I_total_fault_current_radial(m)))

    #    return(incomer_current,incomer_time,m_store)

    #Sequential clearance calc

    for i in xrange(len(m_store)):

        feederone.tripped=0
        feedertwo.tripped=0
        incomer.tripped=0


        if (incomer.time3[i]+incomer.cb_open_time)<min(feederone.time3[i],feedertwo.time3[i]):
            incomer.tripped=1
        elif (feederone.time3[i]+feederone.cb_open_time)<feedertwo.time3[i]:
            feederone.tripped=1
        elif (feedertwo.time3[i]+feedertwo.cb_open_time)<feederone.time3[i]:
            feedertwo.tripped=1
        elif abs(feederone.time3[i]-feedertwo.time3[i])==0:
            feederone.tripped,feedertwo.tripped=1,1
        elif feederone.time3[i]<feedertwo.time3[i]:
            feederone.tripped=1
        elif feedertwo.time3[i]<feederone.time3[i]:
            feedertwo.tripped=1
            
        if incomer.tripped==1:
            margin_store.append(0)
            margin_store2.append((incomer.time3[i]+incomer.cb_open_time)/feederone.time3[i]) #Might need to develop this a bit
            margin_store3.append(1)
            margin_store4.append(0)
            margin_store5.append(0)
            margin_store6.append(0)
            
        elif (feederone.tripped==1 and feedertwo.tripped==0):
            incomer.percent_travel=(feederone.time3[i]+feederone.cb_open_time)/incomer.time3[i]
            feedertwo.percent_travel=(feederone.time3[i]+feederone.cb_open_time)/feedertwo.time3[i]
            feedertwo.percent_travel=min(feedertwo.percent_travel,1.0)
            margin_store.append(incomer.percent_travel)
            margin_store2.append(feedertwo.percent_travel)
            margin_store3.append(incomer.time_fdr1_open[i]*(1-incomer.percent_travel))
            margin_store4.append(feedertwo.time_fdr1_open[i]*(1-feedertwo.percent_travel))
            margin_store5.append((incomer.time_fdr1_open[i]*(1-incomer.percent_travel))-(feedertwo.time_fdr1_open[i]*(1-feedertwo.percent_travel)))
            margin_store6.append(incomer.time3[i]-feederone.time3[i])
            
        elif (feedertwo.tripped==1 and feederone.tripped==0):
            incomer.percent_travel=(feedertwo.time3[i]+feedertwo.cb_open_time)/incomer.time3[i]
            feederone.percent_travel=(feedertwo.time3[i]+feedertwo.cb_open_time)/feederone.time3[i]
            feederone.percent_travel=min(feederone.percent_travel,1.0)
            margin_store.append(incomer.percent_travel)
            margin_store2.append(feederone.percent_travel)
            margin_store3.append(incomer.time_fdr2_open[i]*(1-incomer.percent_travel))
            margin_store4.append(feederone.time_fdr2_open[i]*(1-feederone.percent_travel))
            margin_store5.append((incomer.time_fdr2_open[i]*(1-incomer.percent_travel))-(feederone.time_fdr2_open[i]*(1-feederone.percent_travel)))
            margin_store6.append(incomer.time3[i]-feedertwo.time3[i])
            
        elif (feedertwo.tripped==1 and feederone.tripped==1):
            incomer.percent_travel=max((feederone.time3[i]+(feederone.cb_open_time)),(feedertwo.time3[i]+(feedertwo.cb_open_time))) /incomer.time3[i]
            #incomer.percent_travel=min((feederone.time3[i]),(feedertwo.time3[i])) /incomer.time3[i]
            margin_store.append(incomer.percent_travel)
            margin_store2.append(1)
            margin_store3.append(incomer.time3[i]*(1-incomer.percent_travel))
            margin_store4.append(0)
            margin_store5.append(incomer.time3[i]*(1-incomer.percent_travel))
            
            incomer.percent_travel=min((feederone.time3[i]),(feedertwo.time3[i])) /incomer.time3[i] #Test
            margin_store6.append(incomer.time3[i]*(1-incomer.percent_travel))
            
            
        else:
            print feederone.tripped,feedertwo.tripped,incomer.tripped
            margin_store.append(20)
            margin_store2.append(20)
            margin_store3.append(20)
            margin_store4.append(20)
            margin_store5.append(20)
            margin_store6.append(0)

#We need to get these numbers to the graphs into the application.

#    return (m_store,incomer_current,incomer_current_fdr1_open,incomer_current_fdr2_open,ratio2)

    return (m_store,margin_store,margin_store2,margin_store3,margin_store4,margin_store5,margin_store6,ratio2,incomer.time3,incomer.time_fdr1_open,incomer.time_fdr2_open,\
            feederone.time3,feederone.time_fdr1_open,feederone.time_fdr2_open,\
            feedertwo.time3,feedertwo.time_fdr1_open,feedertwo.time_fdr2_open,\
            incomer.current,incomer.current_fdr1_open,incomer.current_fdr2_open,
            feederone.current,feederone.current_fdr1_open,feederone.current_fdr2_open,
            feedertwo.current,feedertwo.current_fdr1_open,feedertwo.current_fdr2_open,\
            )

#main_seq(3)

#main_seq(4)

'''
#Plot the ITOC curves
inc_time=[]
inc_current=[]
fdr_time=[]
fdr_current=[]
incomer.percent_travel=0.0
feederone.percent_travel=0.0

for i in np.logspace(0,5,100):
    if incomer.time_to_operate(I=i)<50:
        inc_time.append(incomer.time_to_operate(I=i))
        inc_current.append(i)
    if incomer.time_to_operate(I=i)<50:
        fdr_time.append(feederone.time_to_operate(I=i))
        fdr_current.append(i)

plotx, ploty = [], []
plotx = abs(V_base/math.sqrt(3)/(Z_transformer)), abs(V_base/math.sqrt(3)/(Z_transformer))
ploty = incomer.time_to_operate(I=plotx[0]),feederone.time_to_operate(I=plotx[1])
plotdiff = incomer.time_to_operate(I=plotx[0])- feederone.time_to_operate(I=plotx[1])

'''
