import numpy as np 
import pandas as pd

"""
    File constructs a pandas dataframe of empirical cumulative distributions from 
    multiple decades of river, sea and rainfall observations at different temporal 
    resolutions. 
    
    Process datasets to measure daily values with a date format of yyyy/mm/dd.
    
    Datasets for each variable are different length therefore final datset will be 
    river_dates /intersect sea_dates /intersect rain_dates.
"""

if __name__=="__main__":

    # Load river data 
    data = pd.read_csv("C:\\Users\\u2094706\\Downloads\\27092_gdf.csv")
    river = pd.DataFrame(columns=['river'],index=data.iloc[:,0])
    river['river'] = data['value'].values
    # reformat river dates 
    river.index = [i.replace('-','/') for i in river.index]
    
    # Load rain data
    data = pd.read_csv("C:\\Users\\u2094706\\Downloads\\27092_cdr.csv",header=None)
    rain = pd.DataFrame(columns=['rain'],index=data.iloc[:,0])
    rain['rain'] = data.iloc[:,1].values
    # reformat rain dates
    rain.index = [i.replace('-','/') for i in rain.index]
    
    # Load tide data 
    t_data = pd.read_csv("Filtered_tidal_data.csv")
    t_data.head()
    # Extract daily maxima for tide data 
    dates = [i[:10] for i in t_data ['Date'].unique()]
    t_data ['Date'] = dates
    unique_dates = sorted([i for i in set(dates)])
    tide = pd.DataFrame(index=unique_dates,columns=['elevation'])
    for i in unique_dates:
        dt = t_data[t_data['Date']==i]
        if len(dt)>=24:
            tide.loc[i,'elevation'] = np.max(dt[' "Data value"'].values)
            
    # Combine datasets 
    data = pd.concat([rain,tide,river],axis=1).dropna()
    # Save dataset of original observations
    data.to_csv("Whitby_river_rain_sea_92_17.csv") 
    
    
    # Empirical CDF dataset
    def ecdf(data):
        """ Compute ECDF """
        x = np.sort(data)
        n = x.size
        y = np.arange(1, n+1) / n
        return(x,y)
   
    rain_cdf = ecdf(data['rain'])[1]
    elev_cdf = ecdf(data['elevation'])[1]
    river_cdf = ecdf(data['river'])[1]
    cdfs = [rain_cdf, elev_cdf, river_cdf]
    cdf_df = data.copy()
    
    for i in range(len(cdf_df.columns)):
        cdf_df.sort_values(cdf_df.columns[i],ascending=True,inplace=True)
        cdf_df.iloc[:,i] = cdfs[i]
    cdf_df.sort_index(inplace=True)

    # Save cdf dataset 
    cdf_df.to_csv("Whitby_river_rain_sea_92_17_cdf.csv")
    