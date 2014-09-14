from __future__ import division
import  matplotlib.pyplot as plt
import numpy as np
import sys
from scipy.stats import gaussian_kde
import random
import scipy as sc

def get_kdens(summands):
    """ Finds the kernel density function across a sample of parts
    of partitions for a given total (N) and number of parts (S) """
    
    density = gaussian_kde(summands)
    n = len(summands)
    xs = np.linspace(float(min(summands)),float(max(summands)),n)
    density.covariance_factor = lambda : .4
    density._compute_covariance()
    D = [xs,density(xs)]
    return D



radDATA = open('/Users/lisalocey/Desktop/XRADs/RADdataEcon.txt','r')

fs = 12
color = str()

Nlist = []
Slist = []
Evarlist = [] 
ESimplist = []
ENeelist = []
EHeiplist = []
EQlist = []
klist = []
Shanlist = []

BPlist = []
SimpDomlist = []

SinglesList = []
tenlist = []
onelist = []
ptonelist = []
ptzonelist = []

BP1list = []
BP2list = []
BP3list = []
BP4list = []
BP5list = []
NmaxList = []

ct = 0
klist = []
for data in radDATA:
    
    data_list = data.split()
    #print 'datalist', data_list
    name, kind, N, S, Evar, ESimp, ENee, EHeip, EQ, EPielou, BP, SimpDom, perc_ones, s_ten, s_one, s_ptone, s_ptzone, BP1, BP2, BP3, BP4, BP5, Nmax = data_list
    
    print 'community',ct,name
    
    N = float(N)
    S = float(S)
    
    Nlist.append(N)
    Slist.append(S)
    
    Evarlist.append(float(Evar))
    ESimplist.append(float(ESimp))
    ENeelist.append(float(ENee))
    Shanlist.append(float(EPielou))
    
    BPlist.append(float(BP))
    SimpDomlist.append(float(SimpDom))
    
    EHeiplist.append(float(EHeip))
    EQlist.append(float(EQ))
    tenlist.append(float(s_ten))
    onelist.append(float(s_one))
    ptonelist.append(float(s_ptone))
    ptzonelist.append(float(s_ptzone))
    SinglesList.append(float(perc_ones))
    
    BP1list.append(float(BP1))
    BP2list.append(float(BP2))
    BP3list.append(float(BP3))
    BP4list.append(float(BP4))
    BP5list.append(float(BP5))
    NmaxList.append(float(Nmax))
    
    if kind == 'micro':
        color = 'm'
    elif kind == 'macro':
        color = 'gray'
    elif kind == 'econ':
        color = 'c'
    
    klist.append(color)
    
    ct+=1
    #if ct >= 1000: break
    

def kdensMetrics():
    
    metrics = [['Evar', Evarlist], ['Simpson\'s Diversity, 1-D', SimpDomlist], ['Simpsons\' evenness', ESimplist], ['Berger-Parker', BPlist]]

    fig = plt.figure()
    for index, i in enumerate(metrics):
    
        ax = fig.add_subplot(2,2,index+1)

        metric = i[0]
        metlist = i[1]

        microlist = []
        macrolist = []
        econlist = []
        
        for i, j in enumerate(metlist):
            if klist[i] == 'm':
                microlist.append(j)
            elif klist[i] == 'c':
                econlist.append(j)
            elif klist[i] == 'gray':
                macrolist.append(j)
        
        print len(microlist), len(macrolist), len(econlist)    
                    
        D = get_kdens(microlist)
        n = len(microlist)
        plt.plot(D[0], D[1], color = 'm', lw=3, alpha = 0.9,
                 label= 'microbial (n='+str(n)+')')
        ymax1 = max(D[1])
    
        
        D = get_kdens(econlist)
        n = len(econlist)
        plt.plot(D[0], D[1], color = 'c', lw=3, alpha = 0.9,
                 label= 'socioeconomic (n='+str(n)+')')
        ymax3 = max(D[1])
        
        
        n = len(macrolist)
        D = get_kdens(macrolist)
        plt.plot(D[0], D[1], color = 'gray', lw=3, alpha = 0.9,
                 label = 'macrobial (n='+str(n)+')')
        ymax2 = max(D[1])
    
        
        if index == 0: 
            plt.legend(bbox_to_anchor=(-0.03, 1.1, 2.47, .2), loc=10, ncol=3,
                               mode="expand",prop={'size':fs-1})    
        
        #for text in l.get_texts():
        #    text.set_color('w')
        
        ymax = max(ymax1, ymax2, ymax3) + 0.4*(max(ymax1, ymax2, ymax3))
        plt.ylim(0.0, ymax)
        plt.ylabel("Probability density",fontsize=fs)
        plt.xlabel(metric, fontsize=fs)
        plt.tick_params(axis='both', which='major', labelsize=fs-3)

    plt.subplots_adjust(wspace=0.4, hspace=0.4)
    plt.savefig('/Users/lisalocey/Desktop/XRADs/econFigs/MetricsKdens.png',
    dpi=600)
    plt.close()
    print 'kdens fig for metrics: done'   
    
    return
    
    
def scatterMetrics():

    metrics = [['Evar', Evarlist], ['Simpsons', ESimplist]]
    metrics = [['Evar', Evarlist], ['Simpsons', ESimplist], ['Shannons', Shanlist], ['Eq', EQlist]]
    metrics = [['Evar', Evarlist], ['Simpson\'s Diversity, 1-D', SimpDomlist], ['Simpsons\' evenness', ESimplist], ['Berger-Parker', BPlist]]

    fig = plt.figure()
    for index, i in enumerate(metrics):
    
        ax = fig.add_subplot(2, 2, index+1)

        metric = i[0]
        metlist = i[1]
        
        nmacs = 0
        nmics = 0
        emacs = 0
        for j, k in enumerate(klist):
            if k == 'm': nmics += 1
            elif k == 'gray': nmacs += 1
            elif k == 'c': emacs += 1
            
            plt.scatter(Nlist[j], metlist[j], color = k, alpha = 0.8, s = 2,
            linewidths = 0.0)
            
        if index+1 == 1:
            plt.scatter([0],[-1], color = 'm', alpha = 0.8, s=10,
                        label= 'microbial (n='+str(nmics)+')')
            
            plt.scatter([0],[-1], color = 'c',alpha=0.8, s=10,
                        label= 'economic (n='+str(emacs)+')')
            
            plt.scatter([0],[-1], color = 'gray',alpha=0.8, s=10,
                        label= 'macrobial (n='+str(nmacs)+')')
            
            plt.legend(bbox_to_anchor=(-0.03, 1.1, 2.47, .2), loc=10, ncol=3,
                                mode="expand",prop={'size':fs-1})
        
        
        plt.ylim(0.0, 1.0)
        plt.xlabel('Total abundance', fontsize=fs)
        plt.ylabel(metric, fontsize=fs)
        plt.tick_params(axis='both', which='major', labelsize=fs-3)
        plt.xscale('log')
        
        """
        ax = fig.add_subplot(2, 2, 2)
    
        for j, k in enumerate(klist):
            if k == 'c': continue
            plt.scatter(Slist[j], metlist[j], color = k, alpha = 0.8, s = 5,
            linewidths = 0.0)

        plt.xlabel('Richness', fontsize=fs)
        plt.ylabel(metric, fontsize=fs)
        plt.tick_params(axis='both', which='major', labelsize=fs-3)
        plt.xlim(10,5000)
        plt.ylim(0.0, 1.0)
        plt.xscale('log')
        """
        print metric,'scatter plot: done'
    
    plt.subplots_adjust(wspace=0.4, hspace=0.4)
    plt.savefig('/Users/lisalocey/Desktop/XRADs/econFigs/'+metric+'_scatter.png',
    dpi=600)
    plt.close()
    
    return
    
    

def rarebio(plists, klist):
    
    fig = plt.figure()
            
    percent = 10.0
    xlims = [1.0, 1.0, 0.6, 0.2]
    
    for j, plist in enumerate(plists):
        
        print len(plist)
        ax = fig.add_subplot(2,2,j+1)
        
        microlist = []
        macrolist = []
        econlist = []
        
        for i, k in enumerate(plist):
            if klist[i] == 'm':
                microlist.append(k)
            elif klist[i] == 'c':
                macrolist.append(k)
            elif klist[i] == 'gray':
                econlist.append(k)
            
        D = get_kdens(microlist)
        n = len(microlist)
        plt.plot(D[0], D[1], color = 'm', lw=3, alpha = 0.9,
                 label= 'microbial (n='+str(n)+')')
        ymax1 = max(D[1])
    
        D = get_kdens(econlist)
        n = len(econlist)
        #plt.plot(D[0], D[1], color = 'c', lw=3, alpha = 0.9,
        #         label= 'economic (n='+str(n)+')')
        ymax3 = max(D[1])
        
        n = len(macrolist)
        D = get_kdens(macrolist)
        plt.plot(D[0], D[1], color = 'gray', lw=3, alpha = 0.9,
                 label = 'macrobial (n='+str(n)+')')
        ymax2 = max(D[1])
    
        
        if j == 0: 
            plt.legend(bbox_to_anchor=(-0.03, 1.1, 2.47, .2), loc=10, ncol=3,
                               mode="expand",prop={'size':fs-1})    
        
        
        for text in l.get_texts():
            text.set_color('w')

        
        ymax = max(ymax1, ymax2, ymax3) + 0.4*(max(ymax1, ymax2, ymax3))
        plt.ylim(0.0, ymax)
        xmax = xlims[j]
        plt.xlim(0.0, xmax)
            
        plt.ylabel("Density",fontsize=fs)
        plt.xlabel('Portion groups comprising\n<'+str(percent)+'% abundance',
        fontsize=fs)
        plt.tick_params(axis='both', which='major', labelsize=fs-3)
        percent = 0.1*percent

    plt.subplots_adjust(wspace=0.4, hspace=0.4)
    plt.savefig('/Users/lisalocey/Desktop/XRADs/econFigs/kdens_RareBio.png',
    dpi=600)
    print 'kdens for rare bio: done'
    plt.close()
    
    return


def rareBioScatter(plists, Nlist, Slist, klist):
    
    fig = plt.figure()
    ct = 1
    percent = 10.0
    for plist in plists:
        
        ax = fig.add_subplot(2,2,ct)
        
        nmacs = 0
        nmics = 0
        emacs = 0
        for j, k in enumerate(klist):
            if plist[j] > 0.0:
                if k == 'm': nmics += 1
                elif k == 'gray': nmacs += 1
                elif k == 'c':
                    continue
                    emacs += 1
                
                plt.scatter(Nlist[j], plist[j]*100, color = k, alpha = 0.8, s = 5,
                linewidths = 0.0)
                
        plt.xlabel('Total abundance', fontsize=fs)
        plt.xscale('log')
        plt.ylabel('% taxa comprising\n<'+str(float(percent))+'% of N',
        fontsize=fs)
        plt.tick_params(axis='both', which='major', labelsize=fs-3)
        
        plt.scatter([0],[-1], color = 'm', alpha = 0.8, s=10,
                     label= 'microbial (n='+str(nmics)+')')
        
        #plt.scatter([0],[-1], color = 'c',alpha=0.8, s=10,
        #             label= 'economic (n='+str(emacs)+')')
        
        plt.scatter([0],[-1], color = 'gray',alpha=0.8, s=10,
                     label= 'macrobial. (n='+str(nmacs)+')')
        
        if ct == 1:
           plt.legend(bbox_to_anchor=(-0.03, 1.1, 2.47, .2), loc=10, ncol=3,
                              mode="expand",prop={'size':fs-1})    
        
        
        for text in l.get_texts():
            text.set_color('w')

        
        plt.ylim(0,100)
        ct+= 1
        ax = fig.add_subplot(2,2, ct)
        
        for j, k in enumerate(klist):
            if plist[j] > 0.0:
                if k == 'c': continue
                plt.scatter(Slist[j], plist[j], color = k, alpha = 0.8, s = 5,
                linewidths = 0.0)
                
        plt.ylim(0.0,1.0)
        plt.xlim(10,5000)
        
        plt.xlabel('Richness', fontsize=fs)
        plt.xscale('log')
        plt.ylabel('% taxa comprising\n<'+str(float(percent))+'% of N',
        fontsize=fs)
        plt.tick_params(axis='both', which='major', labelsize=fs-3)
        ct+=1
        percent = percent*0.1
        
    plt.subplots_adjust(wspace=0.4, hspace=0.4)
    plt.savefig('/Users/lisalocey/Desktop/XRADs/econFigs/RareBio_scatter.png',
    dpi=600)
    plt.close()
    print 'Rare bio scatter plots: done'
    
    return



def RADfits():
    
    macrolist = ['BBS', 'NABC', 'CBC', 'GENTRY', 'MCDB']
    microlist = ['CATLIN', 'CHU', 'LAUB', 'HYDRO', 'FUNGI']
    metricNamelist = ['Geometric series', 'Zipf']
    
    fitDATA = open('/Users/lisalocey/Desktop/XRADs/R2_by_site.txt','r')

    fs = 12
    color = str()

    geomSerieslist = []
    zipfList = []
    klist = []
    
    for data in fitDATA:
        
        data_list = data.split()
        study, site, N, S, geomS, logS, zipf = data_list
        
        if S >= 10 and study in macrolist:
            
            klist.append('gray')
            geomSerieslist.append(float(geomS))
            zipfList.append(float(zipf))
            
        elif S >= 10 and study in microlist:
            
            klist.append('m')
            geomSerieslist.append(float(geomS))
            zipfList.append(float(zipf))
            
        elif S >=10 and study != 'FIA':
            klist.append('c')
            geomSerieslist.append(float(geomS))
            zipfList.append(float(zipf))
            
    fitDATA.close()
    
    metlist = [geomSerieslist, zipfList]
                                                    
    fig = plt.figure()
    for i, metric in enumerate(metricNamelist):
        
        ax = fig.add_subplot(2,2,i+1)
        metricR2s = metlist[i]
        
        print metric
        
        microlist2 = []
        macrolist2 = []
        econlist = []
        
        for i, j in enumerate(metricR2s):
            if metricR2s[i] >= 0.0:
                if klist[i] == 'm':
                    microlist2.append(j)
                elif klist[i] == 'gray':
                    macrolist2.append(j)
                elif klist[i] == 'c':
                    econlist.append(j)
        
        macrolist2 = random.sample(macrolist2, len(microlist2))
        
        n = len(microlist2)         
        D = get_kdens(microlist2)
        ymax1 = max(D[1])
        plt.plot(D[0], D[1], color = 'm', lw=3, alpha = 0.9,
                 label= 'microbial (n='+str(n)+')')
        
        n = len(econlist)         
        D = get_kdens(econlist)
        plt.plot(D[0], D[1], color = 'c', lw=3, alpha = 0.9,
                 label= 'economic (n='+str(n)+')')
        ymax3 = max(D[1])
        
        n = len(macrolist2)
        D = get_kdens(macrolist2)
        ymax2 = max(D[1])
        plt.plot(D[0], D[1], color = 'gray', lw=3, alpha = 0.9, 
                 label = 'macrobial (n='+str(n)+')')
        
        
        ymax = max(ymax1, ymax2, ymax3) + 0.2*(max(ymax1, ymax2, ymax3))
        plt.ylim(0.0, ymax)
        leg = plt.legend(loc=2,prop={'size':fs-2})
        leg.draw_frame(False)
        l = plt.legend()

        #for text in l.get_texts():
        #    text.set_color('w')

        
        plt.ylabel("Density",fontsize=fs)
        plt.xlabel(metric+' R-square', fontsize=fs)
        plt.tick_params(axis='both', which='major', labelsize=fs-3)
        
    plt.subplots_adjust(wspace=0.4, hspace=0.4)
    plt.savefig('/Users/lisalocey/Desktop/XRADs/econFigs/kdensRADfits_0trunc_noFIA.png',
    dpi=600)
    plt.close()
    print 'RAD fits: done'     
    return


def scatterNmax():
    
    metrics = [['Most abundant or\nwealthy entity', NmaxList]]
    
    for i in metrics:
    
        fig = plt.figure()
        ax = fig.add_subplot(2, 2, 1)

        metric = i[0]
        metlist = i[1]
        
        nmacs = 0
        nmics = 0
        emacs = 0
        for j, k in enumerate(klist):
            #plt.scatter(np.log(Nlist[j]), np.log(metlist[j]), color = k, alpha = 0.7, s = 2,
            #linewidths = 0.0)
            
            plt.scatter(Nlist[j], metlist[j], color = k, alpha = 0.7, s = 2,
            linewidths = 0.0)
            
            if k == 'm': nmics += 1
            elif k == 'gray': nmacs += 1
            elif k == 'c': emacs += 1
            
        plt.scatter([0],[-1], color = 'm', alpha = 0.8, s=5,
                     label= 'microbial (n='+str(nmics)+')')
        
        plt.scatter([0],[-1], color = 'c', alpha = 0.8, s=5,
                     label= 'economic (n='+str(emacs)+')')
                     
        plt.scatter([0],[-1], color = 'gray',alpha=0.8, s=5,
                     label= 'macrobial (n='+str(nmacs)+')')
        
        plt.legend(bbox_to_anchor=(-0.03, 1.1, 2.47, .2), loc=10, ncol=3,
                               mode="expand",prop={'size':fs-1})
        
        
        #xmax = np.log(max(Nlist))
        xmax = max(Nlist)
        
        plt.plot([0,xmax],[0,xmax], 'k--', lw=1)
        
        #X = list(np.log(Nlist))
        #Y = list(np.log(metlist))
        #slope, intercept, rval, pval, stderr = sc.stats.linregress(X,Y)
        #z = np.polyfit(X,Y,1)
        #print 'r-squared and slope for scatterNmax:',rval**2, slope
        plt.ylim(9,10**10)
        plt.xlim(9,10**10)
        
        plt.xscale('log')
        plt.yscale('log')
        
        plt.xlabel('Total abundance', fontsize=fs)
        plt.ylabel(metric, fontsize=fs)
        plt.tick_params(axis='both', which='major', labelsize=fs-3)
        
        #p = np.poly1d(z)
        #xp = np.linspace(min(X), max(X), 1000)
        #plt.plot(xp,p(xp),'-',c='k',lw=1)

        
        ax = fig.add_subplot(2, 2, 2)
    
        for j, k in enumerate(klist):
            #plt.scatter(np.log(Slist[j]), np.log(metlist[j]), color = k, alpha = 0.99, s = 2,
            #linewidths = 0.0)
            
            plt.scatter(Slist[j], metlist[j], color = k, alpha = 0.99, s = 2,
            linewidths = 0.0)
            
        #xmax = np.log(max(metlist))
        #plt.plot([0,xmax],[0,xmax], 'k--', lw=1)
        
        #X = list(np.log(Slist))
        #Y = list(np.log(metlist))
        #slope, intercept, rval, pval, stderr = sc.stats.linregress(X,Y)
        #z = np.polyfit(X,Y,1)
        #print 'r-squared and slope for scatterNmax:',rval**2, slope
        #p = np.poly1d(z)
        #xp = np.linspace(min(X), max(X), 1000)
        #plt.plot(xp,p(xp),'-',c='k',lw=1)
        
        plt.xlabel('Richness', fontsize=fs)
        plt.ylabel(metric, fontsize=fs)
        plt.tick_params(axis='both', which='major', labelsize=fs-3)
        
        plt.xscale('log')
        plt.yscale('log')
        
        #plt.xlim(min(np.log(Slist)), max(np.log(Slist)))
        #plt.ylim(min(np.log(metlist)), max(np.log(metlist)))
    
        print metric,'scatter plot: done'    
                
    plt.subplots_adjust(wspace=0.4, hspace=0.4)
    plt.savefig('/Users/lisalocey/Desktop/XRADs/econFigs/Nmax_scatter.png',
    dpi=600)
    plt.close()
        
    return



kdensMetrics()
scatterMetrics()

scatterNmax()

#RADfits()
#Fitscatter()

#plists = [tenlist, onelist]    
#rarebio(plists, klist)
#rareBioScatter(plists, Nlist, Slist, klist)