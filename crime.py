#%%
'''
1. Pobierz bazę danych dotyczącą śmiertelnych interwencji policji w USA, a następnie wczytaj ją do obiektu DataFrame.
'''
import pandas as pd
import numpy as np
df = pd.read_csv('fatal-police-shootings-data.csv')

#%%
'''
2. Przekształć tabelę w taki sposób, aby wskazywała zestawienie jednocześnie 
liczby ofiar interwencji według rasy (‘race’) oraz tego, czy wykazywały one 
oznaki choroby psychicznej (‘signs_of_mental_illness’).
'''
df_p1= df.pivot_table(values='name',index=['race','signs_of_mental_illness'], aggfunc='count')



#%%
'''
3. Za pomocą Map, Applymap lub Apply dodaj do tego zestawienia kolumnę wskazującą 
jaki odsetek ofiar interwencji wykazywało oznaki choroby psychicznej dla każdej z ras. 
Odpowiedz, która z nich charakteryzuje się największym odsetkiem znamion choroby psychicznej podczas interwencji.
'''

x = df_p1.groupby(level = 0).sum()

df_p1 = df_p1.join(x, how='outer',lsuffix='part', rsuffix='all')


#%%

df_p1['proc']=100*df_p1['namepart']/df_p1['nameall']
idx = pd.IndexSlice
tmp = df_p1.loc[idx[:,True],:]

print(tmp[['proc']].idxmax())
#%%

'''
Dodaj kolumnę oznaczającą dzień tygodnia, w którym doszło do interwencji.
Zlicz interwencje według odpowiedniego dnia tygodnia. 
Następnie stwórz wykres kolumnowy, tak aby dni tygodnia były uszeregowane od poniedziałku do niedzieli.
'''




df['day'] = pd.to_datetime(df['date'])
df['day'] = df['day'].dt.day_name()

df_day= df.pivot_table(values='id',index=['day'], aggfunc='count')
df_day = df_day.reset_index()

#%%

days =  ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
df_day['day'] = pd.Categorical(df_day['day'], categories=days, ordered=True)
df_day = df_day.sort_values('day')
df_day = df_day.reset_index(drop=True)


import matplotlib.pyplot as plt

df_day.plot.bar(x='day',y='id')



#%%
'''
5. Wczytaj do projektu dane dotyczące populacji w poszczególnych stanach USA
oraz dane dotyczące skrótów poszczególnych stanów. Połącz te bazy danych w taki sposób, 
aby móc policzyć do ilu incydentów w bazie dotyczącej śmiertelnych interwencji 
doszło w przeliczeniu na 1000 mieszkańców każdego ze stanów.
'''

data_pop = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states_by_population', header=0)
data_abb= pd.read_html('https://en.wikipedia.org/wiki/List_of_U.S._state_and_territory_abbreviations', header=0)


df_pop = data_pop[0]

df_pop = df_pop[['State','Population estimate, July 1, 2019[2]']]
df_pop.rename(columns={'State':'state','Population estimate, July 1, 2019[2]':'Population'},inplace=True)


df_abb = data_abb[0]
df_abb = df_abb[['Codes:  ISO ISO 3166 codes (2-letter, 3-letter, and 3-digit codes from ISO 3166-1; 2+2-letter codes from ISO 3166-2)  ANSI 2-letter and 2-digit codes from the ANSI standard INCITS 38:2009 (supersedes FIPS 5-2)  USPS 2-letter codes used by the United States Postal Service  USCG 2-letter codes used by the United States Coast Guard (bold red text shows differences between ANSI and USCG) Abbreviations:  GPO Older variable-length official US Government Printing Office abbreviations  AP Abbreviations from the AP Stylebook (bold red text shows differences between GPO and AP)', 'Codes:  ISO ISO 3166 codes (2-letter, 3-letter, and 3-digit codes from ISO 3166-1; 2+2-letter codes from ISO 3166-2)  ANSI 2-letter and 2-digit codes from the ANSI standard INCITS 38:2009 (supersedes FIPS 5-2)  USPS 2-letter codes used by the United States Postal Service  USCG 2-letter codes used by the United States Coast Guard (bold red text shows differences between ANSI and USCG) Abbreviations:  GPO Older variable-length official US Government Printing Office abbreviations  AP Abbreviations from the AP Stylebook (bold red text shows differences between GPO and AP).3']]


df_abb.columns=['state','Abb']


#%%

df_states = df.pivot_table(values='id',index=['state'], aggfunc='count')
df_states.reset_index(inplace=True)
df_states.rename(columns={'state':'Abb'},inplace=True)
df_pop_abb = df_pop.merge(df_abb, how="inner", on='state' )
df_pop_abb.dropna(inplace=True)
df_states = df_pop_abb.merge(df_states, how="inner", on='Abb')
#%%
def per_1000(x):
    rate = 1000*(x['id']/x['Population'])
    return rate
#%%

df_states['per_1000'] = 1000*(df_states['id']/df_states['Population'])

#df_states['per_1000'] = df_states.apply(lambda x: per_1000(x).axis==1)


   # df['Bonus'] = df.apply(lambda row: bonus(row),axis=1)



