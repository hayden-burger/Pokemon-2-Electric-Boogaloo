# -*- coding: utf-8 -*-
"""
Run Distribution testing

Created on Tue May 14 13:40:04 2024
@author: corin
"""

import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

def generate_data(n):
    '''generates normal data of size n'''
    data = np.random.normal(loc=1,scale=1,size=n)
    return data

###Kolmogorov-Smirnov Tests###################################################
# continuous distributions only, more powerful at identifiying differences at 
# center of distributions (not tails)

def run_KS_norm(data):
    '''Currently 'norm', change for other distributions'''
    # Step 2: Fit data to a normal distribution
    mu, std = stats.norm.fit(data)
    # Step 3: Perform KS test
    D, p_value = stats.kstest(data, 'norm', args=(mu, std))
    # Step 4: Plotting
    # Sort data for CDF plotting
    sorted_data = np.sort(data)
    # Empirical CDF
    yvals = np.arange(len(sorted_data)) / float(len(sorted_data) - 1)
    # Theoretical CDF using fitted parameters
    theoretical_cdf = stats.norm.cdf(sorted_data, mu, std)
    #plot
    plt.figure(figsize=(10, 6))
    plt.step(sorted_data, yvals, label='Empirical CDF', where='post')
    plt.plot(sorted_data, theoretical_cdf, label='Theoretical CDF', color='r')
    plt.title('KS Test Comparison: Empirical CDF vs. Theoretical CDF')
    plt.xlabel('Data points')
    plt.ylabel('CDF')
    plt.legend()
    plt.grid(True)
    plt.show()
    # Print KS test result
    print("KS statistic:", D)
    print("P-value:", p_value)

    #Histogram
    plt.figure(figsize=(10, 6))  # Set the figure size (optional)
    plt.hist(data, bins=15, alpha=0.75, color='blue',density=True)  # Bins define how many bars in the histogram
    plt.title('Histogram of Data')  # Title of the histogram
    plt.xlabel('Values')  # Label for the x-axis
    plt.ylabel('Frequency')  # Label for the y-axis
    
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = stats.norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2)
    return

def run_KS_triang(data):
    # Step 2: Fit data to a normal distribution
    c,mu,std = stats.triang.fit(data)
    # Step 3: Perform KS test
    D, p_value = stats.kstest(data, 'triang', args=(c,mu,std))
    print("c:",c)
    print("location:",mu)
    print("shape:",std)
    # Step 4: Plotting
    # Sort data for CDF plotting
    sorted_data = np.sort(data)
    # Empirical CDF
    yvals = np.arange(len(sorted_data)) / float(len(sorted_data) - 1)
    # Theoretical CDF using fitted parameters
    theoretical_cdf = stats.triang.cdf(sorted_data, c,mu,std)
    
    plt.figure(figsize=(10, 6))
    plt.step(sorted_data, yvals, label='Empirical CDF', where='post')
    plt.plot(sorted_data, theoretical_cdf, label='Theoretical CDF', color='r')
    plt.title('KS Test Comparison: Empirical CDF vs. Theoretical CDF')
    plt.xlabel('Data points')
    plt.ylabel('CDF')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    #Histogram
    plt.figure(figsize=(10, 6))  # Set the figure size (optional)
    plt.hist(data, bins=15, alpha=0.75, color='blue',density=True)  # Bins define how many bars in the histogram
    plt.title('Histogram of Data: c=%.3f,loc=%.3f,scale=%.3f' % (c,mu,std))  # Title of the histogram
    plt.xlabel('Values')  # Label for the x-axis
    plt.ylabel('Frequency')  # Label for the y-axis
    
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = stats.triang.pdf(x,c,mu,std)
    plt.plot(x, p, 'k', linewidth=2)
    
    # Print KS test result
    print("KS statistic:", D)
    print("P-value:", p_value)
    return

def run_KS_beta(data):
    # Step 2: Fit data to a normal distribution
    a,b,mu,std = stats.beta.fit(data)
    # Step 3: Perform KS test
    D, p_value = stats.kstest(data, 'beta', args=(a,b,mu,std))
    # Step 4: Plotting
    # Sort data for CDF plotting
    sorted_data = np.sort(data)
    # Empirical CDF
    yvals = np.arange(len(sorted_data)) / float(len(sorted_data) - 1)
    # Theoretical CDF using fitted parameters
    theoretical_cdf = stats.beta.cdf(sorted_data, a,b)
    
    plt.figure(figsize=(10, 6))
    plt.step(sorted_data, yvals, label='Empirical CDF', where='post')
    plt.plot(sorted_data, theoretical_cdf, label='Theoretical CDF', color='r')
    plt.title('KS Test Comparison: Empirical CDF vs. Theoretical CDF')
    plt.xlabel('Data points')
    plt.ylabel('CDF')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    #Histogram
    plt.figure(figsize=(10, 6))  # Set the figure size (optional)
    plt.hist(data, bins=15, alpha=0.75, color='blue',density=True)  # Bins define how many bars in the histogram
    plt.title('Histogram of Data')  # Title of the histogram
    plt.xlabel('Values')  # Label for the x-axis
    plt.ylabel('Frequency')  # Label for the y-axis
    
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = stats.beta.pdf(x, a,b,mu,std)
    plt.plot(x, p, 'k', linewidth=2)
    
    # Print KS test result
    print("KS statistic:", D)
    print("P-value:", p_value)
    return
    
def run_KS_unif(data):
    # Step 2: Fit data to a normal distribution
    mu,std = stats.uniform.fit(data)
    # Step 3: Perform KS test
    D, p_value = stats.kstest(data, 'uniform', args=(mu,std))
    # Step 4: Plotting
    # Sort data for CDF plotting
    sorted_data = np.sort(data)
    # Empirical CDF
    yvals = np.arange(len(sorted_data)) / float(len(sorted_data) - 1)
    # Theoretical CDF using fitted parameters
    theoretical_cdf = stats.uniform.cdf(sorted_data, mu,std)
    
    plt.figure(figsize=(10, 6))
    plt.step(sorted_data, yvals, label='Empirical CDF', where='post')
    plt.plot(sorted_data, theoretical_cdf, label='Theoretical CDF', color='r')
    plt.title('KS Test Comparison: Empirical CDF vs. Theoretical CDF')
    plt.xlabel('Data points')
    plt.ylabel('CDF')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    #Histogram
    plt.figure(figsize=(10, 6))  # Set the figure size (optional)
    plt.hist(data, bins=15, alpha=0.75, color='blue',density=True)  # Bins define how many bars in the histogram
    plt.title('Histogram of Data')  # Title of the histogram
    plt.xlabel('Values')  # Label for the x-axis
    plt.ylabel('Frequency')  # Label for the y-axis
    
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = stats.uniform.pdf(x,mu,std)
    plt.plot(x, p, 'k', linewidth=2)
    
    # Print KS test result
    print("KS statistic:", D)
    print("P-value:", p_value)
    return

def run_KS_expon(data):
    # Step 2: Fit data to a normal distribution
    mu,std = stats.expon.fit(data)
    # Step 3: Perform KS test
    D, p_value = stats.kstest(data, 'expon', args=(mu,std))
    # Step 4: Plotting
    # Sort data for CDF plotting
    sorted_data = np.sort(data)
    # Empirical CDF
    yvals = np.arange(len(sorted_data)) / float(len(sorted_data) - 1)
    # Theoretical CDF using fitted parameters
    theoretical_cdf = stats.expon.cdf(sorted_data,mu,std)
    
    plt.figure(figsize=(10, 6))
    plt.step(sorted_data, yvals, label='Empirical CDF', where='post')
    plt.plot(sorted_data, theoretical_cdf, label='Theoretical CDF', color='r')
    plt.title('KS Test Comparison: Empirical CDF vs. Theoretical CDF')
    plt.xlabel('Data points')
    plt.ylabel('CDF')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    #Histogram
    plt.figure(figsize=(10, 6))  # Set the figure size (optional)
    plt.hist(data, bins=15, alpha=0.75, color='blue',density=True)  # Bins define how many bars in the histogram
    plt.title('Histogram of Data')  # Title of the histogram
    plt.xlabel('Values')  # Label for the x-axis
    plt.ylabel('Frequency')  # Label for the y-axis
    
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = stats.expon.pdf(x,mu,std)
    plt.plot(x, p, 'k', linewidth=2)
    
    # Print KS test result
    print("KS statistic:", D)
    print("P-value:", p_value)
    return

####Anderson-Darling Tests############################################
##Note, only works for norm, expon, log, weibul_min, or gumbel distributions (continuous dist)
# more powerful than KS test because of increased sensitivity to tails

def run_AD_norm(data):
    # Step 2: Fit data to a normal distribution
    mu, std = stats.norm.fit(data)
    # Step 3: Perform Anderson-Darling test
    result = stats.anderson(data, dist='norm')
    # Step 4: Plotting
    # Plot the histogram of the data
    plt.hist(data, bins=30, density=True, alpha=0.6, color='g')
    # Plot the normal PDF with the fitted parameters
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = stats.norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2)
    title = "Anderson-Darling Fit Results: mu = %.2f, std = %.2f" % (mu, std)
    plt.title(title)
    plt.show()
    
    # Print Anderson-Darling test result
    print("Anderson-Darling statistic:", result.statistic)
    print("Critical values:", result.critical_values)
    print("Significance levels:", result.significance_level)
    print(result.fit_result.message)
    return

def run_AD_expon(data):
    # Step 2: Fit data to a normal distribution
    mu,std = stats.expon.fit(data)
    # Step 3: Perform Anderson-Darling test
    result = stats.anderson(data, dist='expon')
    # Step 4: Plotting
    # Plot the histogram of the data
    plt.hist(data, bins=30, density=True, alpha=0.6, color='g')
    # Plot the normal PDF with the fitted parameters
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = stats.expon.pdf(x, mu,std)
    plt.plot(x, p, 'k', linewidth=2)
    title = "Anderson-Darling Fit Results: mu = %.2f, std = %.2f" % (mu,std)
    plt.title(title)
    plt.show()
    
    # Print Anderson-Darling test result
    print("Anderson-Darling statistic:", result.statistic)
    print("Critical values:", result.critical_values)
    print("Significance levels:", result.significance_level)
    print(result.fit_result.message)
    return

###Chi-Squared###########################################################
# Discrete or binned data
#Must have large sample size (rule of thumb: 50+)

def chi_squared_test(observed_frequencies,expected_frequencies):
    '''Observed and Expected frequencies: lists of discrete/binned values.
    Must be same size.'''
    
    # Step 3: Perform Chi-squared goodness-of-fit test
    chi2_stat, p_value = stats.chisquare(f_obs=observed_frequencies, f_exp=expected_frequencies)
    
    # Step 4: Plotting
    categories = ['Face 1', 'Face 2', 'Face 3', 'Face 4', 'Face 5', 'Face 6']
    plt.bar(categories, observed_frequencies, color='b', alpha=0.7, label='Observed')
    plt.bar(categories, expected_frequencies, color='r', alpha=0.3, label='Expected', width=0.5)
    plt.ylabel('Frequencies')
    plt.title('Chi-squared Test: Observed vs Expected Frequencies')
    plt.legend()
    plt.show()
    
    # Print Chi-squared test result
    print("Chi-squared Statistic:", chi2_stat)
    print("P-value:", p_value)
    return

def dice_example():
    #simulate 600 rolls of fair-sided dice
    observed_freq = np.random.multinomial(600,[1/6]*6)
    #theoretical frequencies assuming each face is equally likely:
    expected_freq = [100]*6
    
    chi_squared_test(observed_freq,expected_freq)
    return
