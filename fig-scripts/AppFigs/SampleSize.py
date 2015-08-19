from __future__ import division
#from __future__ import print_function
import  matplotlib.pyplot as plt

import numpy as np
from scipy.stats import gaussian_kde
import random
#import scipy as sc
#from scipy import stats

import os
import sys
#from scipy.stats.distributions import t

import statsmodels.stats.api as sms
import statsmodels.formula.api as smf
#from statsmodels.sandbox.regression.predstd import wls_prediction_std
#from statsmodels.stats.outliers_influence import summary_table
import statsmodels.stats.diagnostic as smd

#import statsmodels.tsa.api as smTsa
import pandas as pd
#import patsy
import linecache

mydir = os.path.expanduser("~/Desktop/Repos/rare-bio/")
mydir2 = os.path.expanduser("~/Desktop/")


"""
    ASSUMPTIONS OF LINEAR REGRESSION
    1. Error in predictor variables is negligible
    2. Variables are measured at the continuous level
    3. The relationship is linear
    4. There are no significant outliers
    5. Independence of observations (no serial correlation in residuals)
    6. Homoscedacticity
    7. Normally distributed residuals (errors)
"""


def get_kdens(summands):
    """ Finds the kernel density function across a sample of parts
    of partitions for a given total (N) and number of parts (S) """

    density = gaussian_kde(summands)
    n = 1000 #len(summands)
    xs = np.linspace(float(min(summands)),float(max(summands)),n)
    density.covariance_factor = lambda : .4
    density._compute_covariance()
    D = [xs,density(xs)]
    return D



def Fig1():

    #fs = 10 # font size used across figures
    #color = str()
    #OrC = 'open'

    SampSizes = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70 ,75, 80]
    Iterations = 1000

    fig = plt.figure(figsize=(12, 8))

    # MODEL PARAMETERS
    RareNCoeffList = [] # List to hold N coefficients
    RareNCoeffpValList = [] # List to hold N coefficient p-values
    DomNCoeffList = [] # List to hold N coefficients
    DomNCoeffpValList = [] # List to hold N coefficient p-values
    EvenNCoeffList = [] # List to hold N coefficients
    EvenNCoeffpValList = [] # List to hold N coefficient p-values

    RareMicCoeffList = [] # List to hold dummy variable cofficients
    RareMicCoeffpValList = [] # List to hold dummy variable cofficient p-values
    DomMicCoeffList = [] # List to hold dummy variable cofficients
    DomMicCoeffpValList = [] # List to hold dummy variable cofficient p-values
    EvenMicCoeffList = [] # List to hold dummy variable cofficients
    EvenMicCoeffpValList = [] # List to hold dummy variable cofficient p-values

    RareIntCoeffList = [] # List to hold Interaction Coefficients
    RareIntCoeffpValList = [] # List to hold Interaction Coefficient p-values
    DomIntCoeffList = [] # List to hold Interaction Coefficients
    DomIntCoeffpValList = [] # List to hold Interaction Coefficient p-values
    EvenIntCoeffList = [] # List to hold Interaction Coefficients
    EvenIntCoeffpValList = [] # List to hold Interaction Coefficient p-values

    RareR2List = [] # List to hold model R2
    RarepFList = [] # List to hold significance of model R2
    DomR2List = [] # List to hold model R2
    DompFList = [] # List to hold significance of model R2
    EvenR2List = [] # List to hold model R2
    EvenpFList = [] # List to hold significance of model R2

    # ASSUMPTIONS OF LINEAR REGRESSION
    # 1. Error in predictor variables is negligible...presumably yes
    # 2. Variables are measured at the continuous level...yes

    # 3. The relationship is linear
    #RarepLinListHC = []
    RarepLinListRainB = []
    RarepLinListLM = []
    #DompLinListHC = []
    DompLinListRainB = []
    DompLinListLM = []
    #EvenpLinListHC = []
    EvenpLinListRainB = []
    EvenpLinListLM = []

    # 4. There are no significant outliers...need to find tests or measures

    # 5. Independence of observations (no serial correlation in residuals)
    RarepCorrListBG = []
    RarepCorrListF = []
    DompCorrListBG = []
    DompCorrListF = []
    EvenpCorrListBG = []
    EvenpCorrListF = []

    # 6. Homoscedacticity
    RarepHomoHW = []
    RarepHomoHB = []
    DompHomoHW = []
    DompHomoHB = []
    EvenpHomoHW = []
    EvenpHomoHB = []

    # 7. Normally distributed residuals (errors)
    RarepNormListOmni = [] # Omnibus test for normality
    RarepNormListJB = [] # Calculate residual skewness, kurtosis, and do the JB test for normality
    RarepNormListKS = [] # Lillifors test for normality, Kolmogorov Smirnov test with estimated mean and variance
    RarepNormListAD = [] # Anderson-Darling test for normal distribution unknown mean and variance

    DompNormListOmni = [] # Omnibus test for normality
    DompNormListJB = [] # Calculate residual skewness, kurtosis, and do the JB test for normality
    DompNormListKS = [] # Lillifors test for normality, Kolmogorov Smirnov test with estimated mean and variance
    DompNormListAD = [] # Anderson-Darling test for normal distribution unknown mean and variance

    EvenpNormListOmni = [] # Omnibus test for normality
    EvenpNormListJB = [] # Calculate residual skewness, kurtosis, and do the JB test for normality
    EvenpNormListKS = [] # Lillifors test for normality, Kolmogorov Smirnov test with estimated mean and variance
    EvenpNormListAD = [] # Anderson-Darling test for normal distribution unknown mean and variance

    NLIST = []

    for SampSize in SampSizes:

        sRareNCoeffList = [] # List to hold N coefficients
        sRareNCoeffpValList = [] # List to hold N coefficient p-values
        sDomNCoeffList = [] # List to hold N coefficients
        sDomNCoeffpValList = [] # List to hold N coefficient p-values
        sEvenNCoeffList = [] # List to hold N coefficients
        sEvenNCoeffpValList = [] # List to hold N coefficient p-values

        sRareMicCoeffList = [] # List to hold dummy variable cofficients
        sRareMicCoeffpValList = [] # List to hold dummy variable cofficient p-values
        sDomMicCoeffList = [] # List to hold dummy variable cofficients
        sDomMicCoeffpValList = [] # List to hold dummy variable cofficient p-values
        sEvenMicCoeffList = [] # List to hold dummy variable cofficients
        sEvenMicCoeffpValList = [] # List to hold dummy variable cofficient p-values

        sRareIntCoeffList = [] # List to hold Interaction Coefficients
        sRareIntCoeffpValList = [] # List to hold Interaction Coefficient p-values
        sDomIntCoeffList = [] # List to hold Interaction Coefficients
        sDomIntCoeffpValList = [] # List to hold Interaction Coefficient p-values
        sEvenIntCoeffList = [] # List to hold Interaction Coefficients
        sEvenIntCoeffpValList = [] # List to hold Interaction Coefficient p-values

        sRareR2List = [] # List to hold model R2
        sRarepFList = [] # List to hold significance of model R2
        sDomR2List = [] # List to hold model R2
        sDompFList = [] # List to hold significance of model R2
        sEvenR2List = [] # List to hold model R2
        sEvenpFList = [] # List to hold significance of model R2

        # ASSUMPTIONS OF LINEAR REGRESSION
        # 1. Error in predictor variables is negligible...presumably yes
        # 2. Variables are measured at the continuous level...yes

        # 3. The relationship is linear
        #sRarepLinListHC = []
        sRarepLinListRainB = []
        sRarepLinListLM = []
        #sDompLinListHC = []
        sDompLinListRainB = []
        sDompLinListLM = []
        #sEvenpLinListHC = []
        sEvenpLinListRainB = []
        sEvenpLinListLM = []

        # 4. There are no significant outliers...need to find tests or measures

        # 5. Independence of observations (no serial correlation in residuals)
        sRarepCorrListBG = []
        sRarepCorrListF = []
        sDompCorrListBG = []
        sDompCorrListF = []
        sEvenpCorrListBG = []
        sEvenpCorrListF = []

        # 6. Homoscedacticity
        sRarepHomoHW = []
        sRarepHomoHB = []
        sDompHomoHW = []
        sDompHomoHB = []
        sEvenpHomoHW = []
        sEvenpHomoHB = []

        # 7. Normally distributed residuals (errors)
        sRarepNormListOmni = [] # Omnibus test for normality
        sRarepNormListJB = [] # Calculate residual skewness, kurtosis, and do the JB test for normality
        sRarepNormListKS = [] # Lillifors test for normality, Kolmogorov Smirnov test with estimated mean and variance
        sRarepNormListAD = [] # Anderson-Darling test for normal distribution unknown mean and variance

        sDompNormListOmni = [] # Omnibus test for normality
        sDompNormListJB = [] # Calculate residual skewness, kurtosis, and do the JB test for normality
        sDompNormListKS = [] # Lillifors test for normality, Kolmogorov Smirnov test with estimated mean and variance
        sDompNormListAD = [] # Anderson-Darling test for normal distribution unknown mean and variance

        sEvenpNormListOmni = [] # Omnibus test for normality
        sEvenpNormListJB = [] # Calculate residual skewness, kurtosis, and do the JB test for normality
        sEvenpNormListKS = [] # Lillifors test for normality, Kolmogorov Smirnov test with estimated mean and variance
        sEvenpNormListAD = [] # Anderson-Darling test for normal distribution unknown mean and variance


        for iteration in range(Iterations):

            Nlist, Slist, Evarlist, ESimplist, ENeelist, EHeiplist, EQlist = [[], [], [], [], [], [], []]
            klist, Shanlist, BPlist, SimpDomlist, SinglesList, tenlist, onelist = [[], [], [], [], [], [], []]
            NmaxList, rareOnesList, rareRelList, rarePairList, rareSkews, KindList = [[], [], [], [], [], []]
            NSlist = []

            ct = 0
            radDATA = []
            datasets = []
            BadNames = ['.DS_Store', 'EMPclosed', 'BCI', 'AGSOIL', 'SLUDGE', 'FECES']

            mlist = ['micro', 'macro']
            for m in mlist:
                for name in os.listdir(mydir2 +'data/'+m):
                        if name in BadNames: continue
                        #else: print name
                        path = mydir2+'data/'+m+'/'+name+'/'+name+'-SADMetricData.txt'
                        num_lines = sum(1 for line in open(path))
                        datasets.append([name, m, num_lines])

            numMac = 0
            numMic = 0

            radDATA = []

            for d in datasets:

                name, kind, numlines = d
                lines = []

                if numlines > SampSize: lines = random.sample(range(1, numlines+1), SampSize)
                else: lines = random.sample(range(1, numlines+1), 40)

                path = mydir2+'data/'+kind+'/'+name+'/'+name+'-SADMetricData.txt'

                for line in lines:
                    data = linecache.getline(path, line)
                    radDATA.append(data)

                #print name, kind, numlines, len(radDATA)

            for data in radDATA:

                data = data.split()
                if len(data) == 0:
                    print 'no data'
                    continue

                name, kind, N, S, Evar, ESimp, ENee, EHeip, EQ, EPielou, BP, SimpDom, rareRel, rareOnes, skew = data

                N = float(N)
                S = float(S)

                if S < 2: continue # Min species richness

                Nlist.append(float(np.log(N)))
                Slist.append(float(np.log(S)))
                NSlist.append(float(np.log(N/S)))

                Evarlist.append(float(np.log(float(Evar))))
                ESimplist.append(float(np.log(float(ESimp))))
                KindList.append(kind)

                BPlist.append(float(BP))
                NmaxList.append(float(np.log(float(BP)*float(N))))
                EHeiplist.append(float(EHeip))

                rareOnesList.append(float(rareOnes))
                rareRelList.append(float(rareOnes)/S)

                # lines for the log-modulo transformation of skewnness
                skew = float(skew)
                sign = 1
                if skew < 0: sign = -1

                lms = np.log(np.abs(skew) + 1)
                lms = lms * sign
                #if lms > 3: print name, N, S
                rareSkews.append(float(lms))

                if kind == 'macro': numMac += 1
                elif kind == 'micro': numMic += 1

                ct+=1


            #print 'Sample Size:',SampSize, ' Mic:', numMic,'Mac:', numMac

            # Multiple regression for Rarity
            d = pd.DataFrame({'N': list(Nlist)})
            d['Rarity'] = list(rareSkews)
            d['Kind'] = list(KindList)

            RarityResults = smf.ols('Rarity ~ N * Kind', d).fit() # Fit the dummy variable regression model
            #print RarityResults.summary(), '\n'

            # Multiple regression for Dominance
            d = pd.DataFrame({'N': list(Nlist)})
            d['Dominance'] = list(NmaxList)
            d['Kind'] = list(KindList)

            DomResults = smf.ols('Dominance ~ N * Kind', d).fit() # Fit the dummy variable regression model
            #print RarityResults.summary(), '\n'

            # Multiple regression for Evenness
            d = pd.DataFrame({'N': list(Nlist)})
            d['Evenness'] = list(ESimplist)
            d['Kind'] = list(KindList)

            EvenResults = smf.ols('Evenness ~ N * Kind', d).fit() # Fit the dummy variable regression model
            #print RarityResults.summary(), '\n'

            RareResids = RarityResults.resid # residuals of the model
            DomResids = DomResults.resid # residuals of the model
            EvenResids = EvenResults.resid # residuals of the model

            # MODEL RESULTS/FIT
            RareFpval = RarityResults.f_pvalue
            Rarer2 = RarityResults.rsquared # coefficient of determination
            #Adj_r2 = RareResults.rsquared_adj # adjusted
            DomFpval = DomResults.f_pvalue
            Domr2 = DomResults.rsquared # coefficient of determination
            #Adj_r2 = DomResults.rsquared_adj # adjusted
            EvenFpval = EvenResults.f_pvalue
            Evenr2 = EvenResults.rsquared # coefficient of determination
            #Adj_r2 = EvenResuls.rsquared_adj # adjusted

            # MODEL PARAMETERS and p-values
            Rareparams = RarityResults.params
            Rareparams = Rareparams.tolist()
            Rarepvals = RarityResults.pvalues
            Rarepvals = Rarepvals.tolist()

            Domparams = DomResults.params
            Domparams = Domparams.tolist()
            Dompvals = DomResults.pvalues
            Dompvals = Dompvals.tolist()

            Evenparams = EvenResults.params
            Evenparams = Evenparams.tolist()
            Evenpvals = EvenResults.pvalues
            Evenpvals = Evenpvals.tolist()

            sRareMicCoeffList.append(Rareparams[1])
            sRareMicCoeffpValList.append(Rarepvals[1])
            sDomMicCoeffList.append(Domparams[1])
            sDomMicCoeffpValList.append(Dompvals[1])
            sEvenMicCoeffList.append(Evenparams[1])
            sEvenMicCoeffpValList.append(Evenpvals[1])

            sRareNCoeffList.append(Rareparams[2])
            sRareNCoeffpValList.append(Rarepvals[2])
            sDomNCoeffList.append(Domparams[2])
            sDomNCoeffpValList.append(Dompvals[2])
            sEvenNCoeffList.append(Evenparams[2])
            sEvenNCoeffpValList.append(Evenpvals[2])

            sRareIntCoeffList.append(Rareparams[3])
            sRareIntCoeffpValList.append(Rarepvals[3])
            sDomIntCoeffList.append(Domparams[3])
            sDomIntCoeffpValList.append(Dompvals[3])
            sEvenIntCoeffList.append(Evenparams[3])
            sEvenIntCoeffpValList.append(Evenpvals[3])

            sRareR2List.append(Rarer2)
            sRarepFList.append(RareFpval)
            sDomR2List.append(Domr2)
            sDompFList.append(DomFpval)
            sEvenR2List.append(Evenr2)
            sEvenpFList.append(EvenFpval)

            # TESTS OF LINEAR REGRESSION ASSUMPTIONS
            # Error in predictor variables is negligible...Presumably Yes
            # Variables are measured at the continuous level...Definitely Yes

            # TESTS FOR LINEARITY, i.e., WHETHER THE DATA ARE CORRECTLY MODELED AS LINEAR
            #HC = smd.linear_harvey_collier(RarityResults) # Harvey Collier test for linearity. The Null hypothesis is that the regression is correctly modeled as linear.
            #sRarepLinListHC.append(HC)
            #HC = smd.linear_harvey_collier(DomResults) # Harvey Collier test for linearity. The Null hypothesis is that the regression is correctly modeled as linear.
            #sDompLinListHC.append(HC)
            #HC = smd.linear_harvey_collier(EvenResults) # Harvey Collier test for linearity. The Null hypothesis is that the regression is correctly modeled as linear.
            #sEvenpLinListHC.append(HC)

            RB = smd.linear_rainbow(RarityResults) # Rainbow test for linearity. The Null hypothesis is that the regression is correctly modeled as linear.
            sRarepLinListRainB.append(RB[1])
            RB = smd.linear_rainbow(DomResults) # Rainbow test for linearity. The Null hypothesis is that the regression is correctly modeled as linear.
            sDompLinListRainB.append(RB[1])
            RB = smd.linear_rainbow(EvenResults) # Rainbow test for linearity. The Null hypothesis is that the regression is correctly modeled as linear.
            sEvenpLinListRainB.append(RB[1])

            LM = smd.linear_lm(RarityResults.resid, RarityResults.model.exog) # Lagrangian multiplier test for linearity
            sRarepLinListLM.append(LM[1])
            LM = smd.linear_lm(DomResults.resid, DomResults.model.exog) # Lagrangian multiplier test for linearity
            sDompLinListLM.append(LM[1])
            LM = smd.linear_lm(EvenResults.resid, EvenResults.model.exog) # Lagrangian multiplier test for linearity
            sEvenpLinListLM.append(LM[1])

            # INDEPENDENCE OF OBSERVATIONS (no serial correlation in residuals)
            #BGtest = smd.acorr_breush_godfrey(RarityResults, nlags=None, store=False) # Breusch Godfrey Lagrange Multiplier tests for residual autocorrelation
                                # Lagrange multiplier test statistic, p-value for Lagrange multiplier test, fstatistic for F test, pvalue for F test
            BGtest = smd.acorr_ljungbox(RareResids, lags=None, boxpierce=True)
            sRarepCorrListBG.append(BGtest[1])
            sRarepCorrListF.append(BGtest[3])

            #BGtest = smd.acorr_breush_godfrey(DomResults, nlags=None, store=False) # Breusch Godfrey Lagrange Multiplier tests for residual autocorrelation
                                # Lagrange multiplier test statistic, p-value for Lagrange multiplier test, fstatistic for F test, pvalue for F test
            BGtest = smd.acorr_ljungbox(DomResids, lags=None, boxpierce=True)
            sDompCorrListBG.append(BGtest[1])
            sDompCorrListF.append(BGtest[3])

            #BGtest = smd.acorr_breush_godfrey(EvenResults, nlags=None, store=False) # Breusch Godfrey Lagrange Multiplier tests for residual autocorrelation
                                # Lagrange multiplier test statistic, p-value for Lagrange multiplier test, fstatistic for F test, pvalue for F test
            BGtest = smd.acorr_ljungbox(EvenResids, lags=None, boxpierce=True)
            sEvenpCorrListBG.append(BGtest[1])
            sEvenpCorrListF.append(BGtest[3])

            # There are no significant outliers...Need tests or measures/metrics

            # HOMOSCEDASTICITY

            # These tests return:
            # 1. lagrange multiplier statistic,
            # 2. p-value of lagrange multiplier test,
            # 3. f-statistic of the hypothesis that the error variance does not depend on x,
            # 4. p-value for the f-statistic

            HW = sms.het_white(RareResids, RarityResults.model.exog)
            sRarepHomoHW.append(HW[3])
            HW = sms.het_white(DomResids, RarityResults.model.exog)
            sDompHomoHW.append(HW[3])
            HW = sms.het_white(EvenResids, RarityResults.model.exog)
            sEvenpHomoHW.append(HW[3])

            HB = sms.het_breushpagan(RareResids, RarityResults.model.exog)
            sRarepHomoHB.append(HB[3])
            HB = sms.het_breushpagan(DomResids, RarityResults.model.exog)
            sDompHomoHB.append(HB[3])
            HB = sms.het_breushpagan(EvenResids, RarityResults.model.exog)
            sEvenpHomoHB.append(HB[3])

            # 7. NORMALITY OF ERROR TERMS
            O = sms.omni_normtest(RareResids)
            sRarepNormListOmni.append(O[1])
            O = sms.omni_normtest(DomResids)
            sDompNormListOmni.append(O[1])
            O = sms.omni_normtest(EvenResids)
            sEvenpNormListOmni.append(O[1])

            JB = sms.jarque_bera(RareResids)
            sRarepNormListJB.append(JB[1]) # Calculate residual skewness, kurtosis, and do the JB test for normality
            JB = sms.jarque_bera(DomResids)
            sDompNormListJB.append(JB[1]) # Calculate residual skewness, kurtosis, and do the JB test for normality
            JB = sms.jarque_bera(EvenResids)
            sEvenpNormListJB.append(JB[1]) # Calculate residual skewness, kurtosis, and do the JB test for normality

            KS = smd.kstest_normal(RareResids)
            sRarepNormListKS.append(KS[1]) # Lillifors test for normality, Kolmogorov Smirnov test with estimated mean and variance
            KS = smd.kstest_normal(DomResids)
            sDompNormListKS.append(KS[1]) # Lillifors test for normality, Kolmogorov Smirnov test with estimated mean and variance
            KS = smd.kstest_normal(EvenResids)
            sEvenpNormListKS.append(KS[1]) # Lillifors test for normality, Kolmogorov Smirnov test with estimated mean and variance

            AD = smd.normal_ad(RareResids)
            sRarepNormListAD.append(AD[1]) # Anderson-Darling test for normal distribution unknown mean and variance
            AD = smd.normal_ad(DomResids)
            sDompNormListAD.append(AD[1]) # Anderson-Darling test for normal distribution unknown mean and variance
            AD = smd.normal_ad(EvenResids)
            sEvenpNormListAD.append(AD[1]) # Anderson-Darling test for normal distribution unknown mean and variance

            print 'Sample size:',SampSize, 'iteration:',iteration

        NLIST.append(numMic+numMac)

        RareNCoeffList.append(np.mean(sRareNCoeffList))
        RareNCoeffpValList.append(np.mean(sRareNCoeffpValList))
        DomNCoeffList.append(np.mean(sDomNCoeffList))
        DomNCoeffpValList.append(np.mean(sDomNCoeffpValList))
        EvenNCoeffList.append(np.mean(sEvenNCoeffList))
        EvenNCoeffpValList.append(np.mean(sEvenNCoeffpValList))

        RareMicCoeffList.append(np.mean(sRareMicCoeffList))
        RareMicCoeffpValList.append(np.mean(sRareMicCoeffpValList))
        DomMicCoeffList.append(np.mean(sDomMicCoeffList))
        DomMicCoeffpValList.append(np.mean(sDomMicCoeffpValList))
        EvenMicCoeffList.append(np.mean(sEvenMicCoeffList))
        EvenMicCoeffpValList.append(np.mean(sEvenMicCoeffpValList))

        RareIntCoeffList.append(np.mean(sRareIntCoeffList))
        RareIntCoeffpValList.append(np.mean(sRareIntCoeffpValList))
        DomIntCoeffList.append(np.mean(sDomIntCoeffList))
        DomIntCoeffpValList.append(np.mean(sDomIntCoeffpValList))
        EvenIntCoeffList.append(np.mean(sEvenIntCoeffList))
        EvenIntCoeffpValList.append(np.mean(sEvenIntCoeffpValList))

        RareR2List.append(np.mean(sRareR2List))
        RarepFList.append(np.mean(sRarepFList))
        DomR2List.append(np.mean(sDomR2List))
        DompFList.append(np.mean(sDompFList))
        EvenR2List.append(np.mean(sEvenR2List))
        EvenpFList.append(np.mean(sEvenpFList))

        # ASSUMPTIONS OF LINEAR REGRESSION
        # 1. Error in predictor variables is negligible...presumably yes
        # 2. Variables are measured at the continuous level...yes

        # 3. The relationship is linear
        #RarepLinListHC.append(np.mean(sRarepLinListHC))
        RarepLinListRainB.append(np.mean(sRarepLinListRainB))
        RarepLinListLM.append(np.mean(sRarepLinListLM))
        #DompLinListHC.append(np.mean(sDompLinListHC))
        DompLinListRainB.append(np.mean(sDompLinListRainB))
        DompLinListLM.append(np.mean(sDompLinListLM))
        #EvenpLinListHC.append(np.mean(sEvenpLinListHC))
        EvenpLinListRainB.append(np.mean(sEvenpLinListRainB))
        EvenpLinListLM.append(np.mean(sEvenpLinListLM))

        # 4. There are no significant outliers...need to find tests or measures

        # 5. Independence of observations (no serial correlation in residuals)
        RarepCorrListBG.append(np.mean(sRarepCorrListBG))
        RarepCorrListF.append(np.mean(sRarepCorrListF))
        DompCorrListBG.append(np.mean(sDompCorrListBG))
        DompCorrListF.append(np.mean(sDompCorrListF))
        EvenpCorrListBG.append(np.mean(sEvenpCorrListBG))
        EvenpCorrListF.append(np.mean(sEvenpCorrListF))

        # 6. Homoscedacticity
        RarepHomoHW.append(np.mean(sRarepHomoHW))
        RarepHomoHB.append(np.mean(sRarepHomoHB))
        DompHomoHW.append(np.mean(sDompHomoHW))
        DompHomoHB.append(np.mean(sDompHomoHB))
        EvenpHomoHW.append(np.mean(sEvenpHomoHW))
        EvenpHomoHB.append(np.mean(sEvenpHomoHB))

        # 7. Normally distributed residuals (errors)
        RarepNormListOmni.append(np.mean(sRarepNormListOmni))
        RarepNormListJB.append(np.mean(sRarepNormListJB))
        RarepNormListKS.append(np.mean(sRarepNormListKS))
        RarepNormListAD.append(np.mean(sRarepNormListAD))

        DompNormListOmni.append(np.mean(sDompNormListOmni))
        DompNormListJB.append(np.mean(sDompNormListJB))
        DompNormListKS.append(np.mean(sDompNormListKS))
        DompNormListAD.append(np.mean(sDompNormListAD))

        EvenpNormListOmni.append(np.mean(sEvenpNormListOmni))
        EvenpNormListJB.append(np.mean(sEvenpNormListJB))
        EvenpNormListKS.append(np.mean(sEvenpNormListKS))
        EvenpNormListAD.append(np.mean(sEvenpNormListAD))


    fig.add_subplot(3, 3, 1)
    plt.xlim(60,1100)
    plt.ylim(0,1)
    plt.xscale('log')
    # Rarity    R2 vs. Sample Size
    plt.plot(NLIST,RareR2List,  c='0.2', ls='--', label=r'$R^2$')
    plt.ylabel(r'$R^2$', fontsize=14)
    plt.text(18, 0.5, 'Rarity', rotation='vertical', fontsize=20)

    leg = plt.legend(loc=4,prop={'size':14})
    leg.draw_frame(False)


    fig.add_subplot(3, 3, 2)
    plt.xlim(60,1100)
    plt.xscale('log')
    # Rarity    Coeffs vs. Sample Size
    plt.plot(NLIST,RareMicCoeffList, c='r', label='Microbe')
    plt.plot(NLIST,RareNCoeffList,  c='b', label='N')
    plt.plot(NLIST,RareIntCoeffList, c='g', label='Interaction')
    plt.ylabel('Coefficient')

    leg = plt.legend(loc=1,prop={'size':10})
    leg.draw_frame(False)


    fig.add_subplot(3, 3, 3)
    plt.xlim(60,1300)
    plt.ylim(0, 0.6)
    plt.xscale('log')
    # Rarity    p-vals vs. Sample Size

    # 3. The relationship is linear
    #plt.plot(RarepLinListHC, NLIST, c='m', alpha=0.8)
    #plt.plot(NLIST,RarepLinListRainB,  c='m')
    plt.plot(NLIST,RarepLinListLM,  c='m', ls='-', label='linearity')

    # 5. Independence of observations (no serial correlation in residuals)
    #plt.plot(NLIST,RarepCorrListBG,  c='c')
    plt.plot(NLIST,RarepCorrListF,  c='c', ls='-', label='autocorrelation')

    # 6. Homoscedacticity
    plt.plot(NLIST,RarepHomoHW,  c='orange', ls='-', label='homoscedasticity')
    #plt.plot(NLIST,RarepHomoHB,  c='r', ls='-')

    # 7. Normally distributed residuals (errors)
    plt.plot(NLIST,RarepNormListOmni,  c='Lime', ls='-', label='normality')
    #plt.plot(NLIST,RarepNormListJB,  c='Lime', ls='-')
    #plt.plot(NLIST,RarepNormListKS,  c='Lime', ls='--', lw=3)
    #plt.plot(NLIST,RarepNormListAD,  c='Lime', ls='--')

    plt.plot([60, 1100], [0.05, 0.05], c='0.2', ls='--', label=r'$\alpha$'+'='+str(0.05))
    plt.ylabel('p-value')

    leg = plt.legend(loc=1,prop={'size':10})
    leg.draw_frame(False)


    fig.add_subplot(3, 3, 4)
    plt.xscale('log')
    plt.ylim(0,1)
    plt.xlim(60,1100)
    # Dominance     R2 vs. Sample Size
    plt.plot(NLIST, DomR2List, c='0.2', ls='--', label=r'$R^2$')
    plt.ylabel(r'$R^2$', fontsize=14)
    plt.text(18, 0.7, 'Dominance', rotation='vertical', fontsize=20)

    leg = plt.legend(loc=4,prop={'size':14})
    leg.draw_frame(False)

    fig.add_subplot(3, 3, 5)
    plt.xscale('log')
    plt.xlim(60,1100)
    # Dominance     Coeffs vs. Sample Size
    plt.plot(NLIST, DomMicCoeffList, c='r', label='Microbe')
    plt.plot(NLIST, DomNCoeffList,  c='b', label='N')
    plt.plot(NLIST, DomIntCoeffList, c='g', label='Interaction')
    plt.ylabel('Coefficient')

    leg = plt.legend(loc=1,prop={'size':10})
    leg.draw_frame(False)

    fig.add_subplot(3, 3, 6)
    plt.xscale('log')
    #plt.yscale('log')
    plt.xlim(60,1300)
    plt.ylim(0, 0.6)
    # Dominance     p-vals vs. Sample Size

    # 3. The relationship is linear
    #plt.plot(DompLinListHC, NLIST, c='m', alpha=0.8)
    #plt.plot(NLIST, DompLinListRainB, c='m')
    plt.plot(NLIST, DompLinListLM, c='m', ls='-', label='linearity')

    # 5. Independence of observations (no serial correlation in residuals)
    #plt.plot(NLIST, DompCorrListBG, c='c')
    plt.plot(NLIST, DompCorrListF, c='c', ls='-', label='autocorrelation')

    # 6. Homoscedacticity
    plt.plot(NLIST, DompHomoHW, c='orange', ls='-', label='homoscedasticity')
    #plt.plot(NLIST, DompHomoHB, c='r',ls='-')

    # 7. Normally distributed residuals (errors)
    plt.plot(NLIST, DompNormListOmni, c='Lime', ls='-', label='normality')
    #plt.plot(NLIST, DompNormListJB, c='Lime', ls='-')
    #plt.plot(NLIST, DompNormListKS, c='Lime', ls='--', lw=3)
    #plt.plot(NLIST, DompNormListAD, c='Lime', ls='--')

    plt.plot([60, 1100], [0.05, 0.05], c='0.2', ls='--', label=r'$\alpha$'+'='+str(0.05))

    #plt.xlabel('Sample size')
    plt.ylabel('p-value')

    leg = plt.legend(loc=1,prop={'size':10})
    leg.draw_frame(False)


    fig.add_subplot(3, 3, 7)
    plt.xscale('log')
    plt.ylim(0,1)
    plt.xlim(60,1100)
    # Evenness      R2 vs. Sample Size
    plt.plot(NLIST, EvenR2List, c='0.2', ls='--', label=r'$R^2$')
    plt.xlabel('Sample size')
    plt.ylabel(r'$R^2$', fontsize=14)
    plt.text(18, 0.7, 'Evenness', rotation='vertical', fontsize=20)

    leg = plt.legend(loc=4,prop={'size':14})
    leg.draw_frame(False)

    fig.add_subplot(3, 3, 8)
    plt.xscale('log')
    plt.xlim(60,1100)
    # Evenness      Coeffs vs. Sample Size
    plt.plot(NLIST, EvenMicCoeffList, c='r', label='Microbe')
    plt.plot(NLIST, EvenNCoeffList,  c='b', label='N')
    plt.plot(NLIST, EvenIntCoeffList, c='g', label='Interaction')
    plt.xlabel('Sample size')
    plt.ylabel('Coefficients')

    leg = plt.legend(loc=1,prop={'size':10})
    leg.draw_frame(False)

    fig.add_subplot(3, 3, 9)
    plt.xscale('log')
    plt.xlim(60,1300)
    plt.ylim(0, 0.6)
    # Evenness      p-vals vs. Sample Size

    # 3. The relationship is linear
    #plt.plot(EvenpLinListHC, NLIST, c='m', alpha=0.8)
    #plt.plot(NLIST, EvenpLinListRainB, c='m')
    plt.plot(NLIST, EvenpLinListLM, c='m', ls='-', label='linearity')

    # 5. Independence of observations (no serial correlation in residuals)
    #plt.plot(NLIST, EvenpCorrListBG, c='c')
    plt.plot(NLIST, EvenpCorrListF, c='c', ls='-', label='autocorrelation')

    # 6. Homoscedacticity
    plt.plot(NLIST, EvenpHomoHW, c='orange', ls='-', label='homoscedasticity')
    #plt.plot(NLIST, EvenpHomoHB, c='r', ls='-')

    # 7. Normally distributed residuals (errors)
    plt.plot(NLIST, EvenpNormListOmni, c='Lime', ls='-', label='normality')
    #plt.plot(NLIST, EvenpNormListJB, c='Lime', alpha=0.9, ls='-')
    #plt.plot(NLIST, EvenpNormListKS, c='Lime', alpha=0.9, ls='--', lw=3)
    #plt.plot(NLIST, EvenpNormListAD, c='Lime', alpha=0.9, ls='--')

    plt.plot([60, 1100], [0.05, 0.05], c='0.2', ls='--', label=r'$\alpha$'+'='+str(0.05))

    plt.xlabel('Sample size')
    plt.ylabel('p-value')

    leg = plt.legend(loc=1,prop={'size':10})
    leg.draw_frame(False)

    #plt.tick_params(axis='both', which='major', labelsize=fs-3)
    plt.subplots_adjust(wspace=0.4, hspace=0.4)
    plt.savefig(mydir+'/figs/ResamplingOverRegression-open_REF.png', dpi=600, bbox_inches = "tight")
    plt.close()
    plt.show()

    return



""" The following lines call figure functions to reproduce figures from the
    Locey and Lennon (2014) manuscript """

Fig1()