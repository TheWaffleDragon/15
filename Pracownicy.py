import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#%%
df = pd.read_csv('HRDataset.csv')

print(df.isnull())
sns.heatmap(df.isnull())

#%%
df.drop(['LastPerformanceReview_Date','DaysLateLast30'],axis=1,inplace=True)

#%%
df.dropna(thresh=2,inplace=True)

sns.heatmap(df.isnull())

#%%
df['DOB'] = pd.to_datetime(df['DOB'],format='%m/%d/%y')

df['DateofHire'] = pd.to_datetime(df['DateofHire'],format='%m/%d/%Y')

df['DateofTermination'] = pd.to_datetime(df['DateofTermination'],format='%m/%d/%y')

#%%


'''
1. Czy istnieje zależność pomiędzy tym, kto jest bezpośrednim przełożonym 
(ManagerName, ManagerID) danego pracownika, a oceną wydajności pracy (PerformanceScore)?
'''
sns.set_style('whitegrid')



df_pref = df.pivot_table(index='ManagerName', columns='PerformanceScore', values='EmpID', aggfunc='count')
df_pref = df_pref.fillna(0)

df_sum = df.pivot_table(values='EmpID', index='ManagerName',aggfunc='count')

df_pref['Exceeds'] = df_pref['Exceeds']/df_sum['EmpID']
df_pref['Fully Meets'] = df_pref['Fully Meets']/df_sum['EmpID']
df_pref['Needs Improvement'] = df_pref['Needs Improvement']/df_sum['EmpID']
df_pref['PIP'] = df_pref['PIP']/df_sum['EmpID']


plt.figure(figsize=(15,15))
sns.heatmap(df_pref)

#

#%%


'''
2. Jakie źródła pozyskania pracownika (Recruitment Source) są najlepsze, 
jeśli zależy nam na jak najdłuższym stażu pracowników?
'''
import datetime as dt

def count_seniority(row):

    if pd.isnull(row['DateofTermination']):
        end_date = dt.datetime(2019,9,27)
    else:
        end_date = row['DateofTermination']

    return (end_date - row['DateofHire'])/np.timedelta64(1,'Y')


df['Seniority'] = df.apply(lambda row: count_seniority(row),axis=1)


df_sen = df.pivot_table(values='Seniority', index='RecruitmentSource',aggfunc='mean')
df_sen.sort_values(by = 'Seniority', inplace=True, ascending=False)
print(df_sen.head(1))



#%%
'''
3. Czy stan cywilny (MartialDesc) pracownika koreluje w jakikolwiek 
sposób z zadowoleniem z pracy (EmpSatisfaction)?
'''
df_sat = df.pivot_table(values='EmpSatisfaction', index='MaritalStatusID',aggfunc='mean')


#%%
'''
4. Jak wygląda struktura wieku aktualnie zatrudnionych pracowników?
'''
def age(row):
    
    end_date = dt.datetime(2019,9,27)
    
    x=(end_date - row['DOB'])/np.timedelta64(1,'Y')

    return x

df['Age'] = df.apply(lambda row: age(row),axis=1)


#prowizoryczne czyszczenie dziwnych lat

df['Year'] = df['DOB'].dt.year
df_age = df['Age'].where(df['Year']<2000)
df_age.dropna(inplace=True)


sns.histplot(data = df_age)
print(df_age.describe())

#%%
'''
5.Czy starsi pracownicy pracują nad większą liczbą specjalnych projektów niż młodsi pracownicy?
'''

df_proj = df[['EmpID','SpecialProjectsCount','Age']]
df_proj['Age'] = df['Age'].where(df['Age']>0)
df_proj.dropna(inplace=True)

#sns.scatterplot(x= df_proj['Age'], y=df_proj['SpecialProjectsCount'])
sns.histplot(data = df_proj, x=df_proj['Age'], y= df_proj['SpecialProjectsCount'], bins = 10)

# brak wyraźnej korelacji między wiekiem i liczbą specjalnych projektów 
