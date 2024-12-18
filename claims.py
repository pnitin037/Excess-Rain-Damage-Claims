import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from datetime import date, timedelta

# function for excess rain detections
def excess_rain(dt):
        k = 0
        lt = []
        for i,row in dt.iterrows():
             if i == 0:
                continue
             else:
                if( ( dt.iloc[i,1] == ( dt.iloc[i-1,1] + timedelta(days=1) ) ) & (dt['Rainfall_mm'].iloc[i] > 60)):
                        k += 1
                else:
                        lt.append(k)
                        k=0
           
        return lt

# function for claims calculation
def claim_cal(dt):
        total = 0
        tp = excess_rain(dt)
        total = 0
        # excess rain between 11-30
        lt = [x for x in tp if 10<x<31]
        total = total + sum(lt)*100
        # excess rain between 31-50
        lt = [x for x in tp if 30<x<51]
        total = total + sum(lt)*200
        # excess rain greater than 50
        lt = [x for x in tp if x>50]
        total = total + sum(lt)*300
        return total

# importing data 
data = pd.read_excel('InRisk_Labs_Assignment.xlsx')
df = pd.DataFrame(data)

# Checking whether there is an outlier in data using box plot
plt.boxplot(df['Rainfall_mm'])
plt.title("Boxplot for Rainfall")
plt.ylabel("Rainfall")
# plt.yscale('log')
plt.show() 

# Clearly we can see there are two outliers in the data 

# Calculate Q1, Q3, and IQR
Q1 = df['Rainfall_mm'].quantile(0.25)
Q3 = df['Rainfall_mm'].quantile(0.75)
IQR = Q3 - Q1

# Define bounds for outliers
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Filter out outliers
df_outlier = df[(df['Rainfall_mm'] < lower_bound) | (df['Rainfall_mm'] > upper_bound)]
# print(df_outlier)

# In the data we have two outlier which we have stored in df_outlier
# Now we are removing outlier in the data

df = df[(df['Rainfall_mm'] >= lower_bound) & (df['Rainfall_mm'] <= upper_bound)]


# getting data according to region.

reg_a = df[df['Region'] == 'Region_A' ] 
reg_a = reg_a.reset_index(drop=True)
reg_b = df[df['Region'] == 'Region_B' ] 
reg_b = reg_b.reset_index(drop=True)
reg_c = df[df['Region'] == 'Region_C' ] 
reg_c = reg_c.reset_index(drop=True)
reg_d = df[df['Region'] == 'Region_D' ] 
reg_d = reg_d.reset_index(drop=True)
reg_e = df[df['Region'] == 'Region_E' ] 
reg_e = reg_e.reset_index(drop=True)

# now find the total claim amount region wise.


# Region A
claims_A = claim_cal(reg_a)
print(claims_A)
# there is no excess rain for consecutively for more than 10 days in region A.

# Region B
claims_B = claim_cal(reg_b)
print(claims_B)
# there is no excess rain for consecutively for more than 10 days in region B.

# Region C
claims_C = claim_cal(reg_c)
print(claims_C)
# there is no excess rain for consecutively for more than 10 days in region C.

# Region D
claims_D = claim_cal(reg_d)
print(claims_D)
# there is no excess rain for consecutively for more than 10 days in region D.

# Region E
claims_E = claim_cal(reg_e)
print(claims_E)
# there is no excess rain for consecutively for more than 10 days in region E.

