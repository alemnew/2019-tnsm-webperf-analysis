# utility functions for prcessing the Web QoE and QoS dataset 
import pandas as pd
import numpy as np
import math
import Cdf
import sys 
import requests
# Global variables 
dataset = '../dataset/webget-all.csv'

# g_title = "http://www.google.com/mobile/"
# f_title = "http://www.facebook.com/policies"
# u_title = "http://www.youtube.com"

g_title = "Google"
f_title = "Facebook"
u_title = "YouTube"

#return base url from url
def get_base_url(url):
    return(url.rsplit('/')[2])
# create a list of dataset classified basedon URL
def tables_site(data):
    sites = {}
    for w in pd.unique(data['target']): 
        sites[w] = data.loc[data['target'] == w]
    return(sites)

def tables_hourstr(data):
    sites = {}
    for w in pd.unique(data['hourstr']): 
        sites[w] = data.loc[data['hourstr'] == w]
    return(sites)

# round time to date
def round_time_to_day(dtime):
    import datetime;    
    d = datetime.datetime.strptime(dtime, "%Y-%m-%d %H:%M:%S")
    d = d.replace(hour=0, minute=0, second=0)
    dtime = d.strftime('%Y-%m-%d')
    return dtime

# round time to hour
def round_time_to_hour(dtime):
    import datetime;    
    d = datetime.datetime.strptime(dtime, "%Y-%m-%d %H:%M:%S")
    d = d.replace(hour=0, minute=0, second=0)
    dtime = d.strftime('%Y-%m-%d %H')
    return dtime

# round time to month
def round_time_to_month(dtime):
    import datetime;    
    d = datetime.datetime.strptime(dtime, "%Y-%m-%d %H:%M:%S")
    d = d.replace(hour=0, minute=0, second=0)
    dtime = d.strftime('%Y-%m')
    return dtime

# round time to year,
def round_time_to_year(dtime):
    import datetime;    
    d = datetime.datetime.strptime(dtime, "%Y-%m-%d %H:%M:%S")
    d = d.replace(hour=0, minute=0, second=0)
    dtime = d.strftime('%Y')
    return dtime


# get the x value of the cdf
def get_icdf(caigo):
    pp = [0.25, 0.4, 0.5, 0.6,0.75, 0.8, 0.9, 0.95]
    ppf = []
    for p in pp:
        v = Cdf.Cdf.Value(caigo, p)
        ppf.append(v)
    return(ppf)

# create a list of dataset classified basedon probe ID
def tables_unit(data):
    sites = {}
    for w in pd.unique(data['unit_id']): 
        sites[w] = data.loc[data['unit_id'] == w]
    return(sites)

def tables_id(data):
    sites = {}
    for w in pd.unique(data['id']): 
        sites[w] = data.loc[data['id'] == w]
    return(sites)
# create a list of dataset classified basedon date
def tables_date(data):
    sites = {}
    for w in pd.unique(data['dtime']): 
        sites[w] = data.loc[data['dtime'] == w]
    return(sites)

# create a list of dataset classified basedon latitude
def tables_lat(data):
    sites = {}
    for w in pd.unique(data['lat']): 
        sites[w] = data.loc[data['lat'] == w]
    return(sites)

# create a list of dataset classified basedon long
def tables_long(data):
    sites = {}
    for w in pd.unique(data['long']): 
        sites[w] = data.loc[data['long'] == w]
    return(sites)

# create a list of dataset classified basedon IP
def tables_ip(data):
    sites = {}
    for w in pd.unique(data['ip']): 
        sites[w] = data.loc[data['ip'] == w]
    return(sites)

def get_json_resource_from_absolute_uri(url, query_params):
    try: res = requests.get(url, params = query_params)
    except Exception as e: print(e, file=sys.stderr)
    else:
        try: res_json = res.json()
        except Exception as e: print(e, file=sys.stderr)
        else: 
            return res_json
        
def get_asn_from_endpoint(endpoint):
    asn = holder = None
    base_uri = 'https://stat.ripe.net'; url = '%s/data/prefix-overview/data.json'%base_uri
    params = {'resource' : endpoint}
    try: res = get_json_resource_from_absolute_uri(url, params)
    except Exception as e: print(e, file=sys.stderr); return None
    try:
        asns_holders = []
        for item in res['data']['asns']:
            asn = item['asn']; holder = item['holder']
            asns_holders.append((asn, holder))
    except Exception as e: print(e, file=sys.stderr)
    return asns_holders

#used by box plots 
def stop_plot_box(ax, region, shrink_right = False, fs = 18, plt_type = 'fetch_type'):
    ax.set_title("")
    plt.suptitle("")
    ax.grid(False)
    if plt_type == 'fetch_time': 
        ax.set_ylim([100, 10000])
    elif plt_type == 'ttfb_avg':
        ax.set_ylim([10, 1000])
    elif plt_type == 'dns_time':
        ax.set_ylim([1, 501])
    ax.set_yscale('log')
    ax.set_xlabel('', fontsize=fs)
    ax.set_title(region,  fontsize=18)
    major_ticks = np.arange(1, 42, 6)                                              
    minor_ticks = np.arange(1, 42, 1) 
#     ax.set_xticks(minor_ticks, minor=True)                                           
    ax.set_xticks(major_ticks, minor=False)                                           
    labels = ['2014 Jan','2014 Jul', '2015 Jan','2015 Jul',
          '2016 Jan','2016 Jul','2017 Jan']
    ax.set_xticklabels(labels)    

def boxplot_sorted(df, by, column, ax, rot = 0):
    medianprops = dict(linestyle='--', color = 'blue', linewidth=3)
    color = dict(boxes='DarkGreen', whiskers='DarkOrange', medians='DarkBlue', caps='Gray')
    df2 = pd.DataFrame({col:vals[column] for col, vals in df.groupby(by)})
    meds = df2.median()#.sort_values() # for sorting by median 
    return df2[meds.index].boxplot(ax = ax, rot = rot,  vert = True,
                                   medianprops = medianprops, showfliers = False, 
                                   return_type = "axes")