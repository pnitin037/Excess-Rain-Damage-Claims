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


def total_claim(c):
        if (c>10 and c<31):
                c = c*100
        elif(c>30 and c<51):
                c = c*200
        elif(c>50):
                c = c*300
        else:
                c = 0
        return c


# importing data 
data = pd.read_excel('InRisk_Labs_Assignment.xlsx')
df = pd.DataFrame(data)

# Checking whether there is an outlier in data using box plot
plt.boxplot(df['Rainfall_mm'])
plt.title("Boxplot for Rainfall")
plt.ylabel("Rainfall")
# plt.yscale('log')
# plt.show() 

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

# Getting data when there is excess rainfall 
dff = df.groupby('Region').agg({"Rainfall_mm" : lambda series: ( series > 60).sum()})


# ---------------------------------------------
# Corrected Version
# ---------------------------------------------

# Region A
claim_a = total_claim(dff.iloc[0,0])
# cc = excess_rain(df[df['Region'] == 'Region_A'].reset_index(drop=True))
# print(sum(cc))
print(claim_a)

# Region B
claim_b = total_claim(dff.iloc[1,0])
print(claim_b)

#  Region C
claim_c = total_claim(dff.iloc[2,0])
print(claim_c)

# Region D
claim_d = total_claim(dff.iloc[3,0])
print(claim_d)

# Region E
claim_e = total_claim(dff.iloc[4,0])
print(claim_e)

