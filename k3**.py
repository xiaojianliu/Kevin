# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 15:21:35 2017

@author: hxu
"""
import numpy as np
import csv
import math
import matplotlib.pyplot as plt
def printindex(lon, lat, lons, lats):  #0.3/5==0.06
    distancelist = []
    for a in np.arange(len(lons)):
        distancelist.append(math.sqrt((lon-lons[a])**2+(lat-lats[a])**2))
    mindex = np.argmin(distancelist)
    return mindex

v4=np.load('mean_v0.npy')
u4=np.load('mean_u0.npy')
v5=np.load('mean_v0.npy')
u5=np.load('mean_u0.npy')
lons=np.load('gom3.lonc.npy')
lats=np.load('gom3.latc.npy')
point_data='nes_lon_lat.csv'
days=5
csvfile = file('lona5x.csv', 'wb')
csvfile1 = file('lata5x.csv', 'wb')
#sea_data = np.genfromtxt('sea.csv',dtype=None,names=['x','y','h'],delimiter=',') 
data = np.genfromtxt(point_data,dtype=None,names=['local','lon','lat'],delimiter=',',skip_header=1)    
point_data=[]
num=1#how many point do you want forecast
plt.figure()
FNCL='necscoast_worldvec.dat' 
CL=np.genfromtxt(FNCL,names=['lon','lat'])
plt.plot(CL['lon'],CL['lat'],'b-',linewidth=0.5)
plt.title('forecast %s days forward'%(days))
plt.scatter(data['lon'][0],data['lat'][0],s=2,color='green',label='start_point')
for a in np.arange(3132):#313
    print 'a',a 
    point_id=a*1
    lonp=data['lon'][point_id]
    latp=data['lat'][point_id]
    plt.scatter(lonp,latp,s=2,color='green')
    index=printindex(lonp, latp, lons, lats)
    v_t=v5[index]
    u_t=u5[index]
    dx = 60*60*u_t; dy = 60*60*v_t
    nodes = dict(lon=[lonp], lat=[latp],time=[])
    lon = lonp + dx/(111111*np.cos(latp*np.pi/180))
            
    lat = latp + dy/111111
            #print '%d,lat,lon,layer'%(i+1),lat,lon,layer
    nodes['lon'].append(lon);nodes['lat'].append(lat)
    for b in np.arange(days*24):
        #print 'b',b
        index=printindex(lon, lat, lons, lats)
        v_t=v5[index]
        u_t=u5[index]
        dx = 60*60*u_t; dy = 60*60*v_t
        lon = lon + dx/(111111*np.cos(lat*np.pi/180))
            
        lat = lat + dy/111111
            #print '%d,lat,lon,layer'%(i+1),lat,lon,layer
        nodes['lon'].append(lon);nodes['lat'].append(lat)
    plt.plot([nodes['lon'][0],nodes['lon'][-1]],[nodes['lat'][0],nodes['lat'][-1]],'y-',linewidth=0.5)
    plt.scatter(nodes['lon'][-1],nodes['lat'][-1],s=2,color='red')
    if a==311:
        plt.scatter(nodes['lon'][-1],nodes['lat'][-1],s=2,color='red',label='end_point')
    
    writer = csv.writer(csvfile)
    
    if len(nodes['lon'])<days*24+1:
        for z in np.arange(days*24+1-len(nodes['lon'])):
            nodes['lon'].append(0)
    writer.writerow(nodes['lon'])
    
    
    writer1 = csv.writer(csvfile1)
    
    if len(nodes['lat'])<days*24+1:
        for z in np.arange(days*24+1-len(nodes['lat'])):
            nodes['lat'].append(0)
    writer1.writerow(nodes['lat'])
csvfile.close()  
csvfile1.close()  
plt.legend(loc='best')
plt.savefig('5 days forward',dpi=700)
plt.show


