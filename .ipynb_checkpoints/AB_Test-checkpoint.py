#!/usr/bin/env python
# coding: utf-8

# ## Scipy

# In[ ]:


Kontrol Grubu A

Grup içindeki kullanıcı sayısı: 7,015
Grup içindeki dönüşüm sayısı: 139
Dönüşüm oranı: %1.98
Alternatif Grup B

Grup içindeki kullanıcı sayısı: 6,987
Grup içindeki dönüşüm sayısı: 314
Dönüşüm oranı: %4.49


# In[16]:


import pandas as pd

test_data = pd.DataFrame(data={'test_group': ['a']*7015 + ['b']*6987,
                               'conversion': [1]*139 + [0]*(7015-139) + [1]*314 + [0]*(6987-314)})

# Her şeyin doğru bir şekilde oluşturulup oluşturulmadığını kontrol edelim:
test_data.groupby('test_group').describe()


# In[17]:


test_data


# In[18]:


from scipy import stats

alpha = 0.05

statistic, pvalue = stats.ttest_ind(test_data[test_data['test_group'] == 'a']['conversion'],
                                    test_data[test_data['test_group'] == 'b']['conversion'], 
                                    alternative='less')

print(f't-statistic: {round(statistic, 2)}, p-value: {round(pvalue, 2)}')

if pvalue < alpha:
    print('The difference is statistically significant, Null Hypothesis is rejected.')
else:
    print('The difference is insignificant, Null Hypothesis cannot rejected.')


# In[19]:


from scipy import stats

alpha = 0.05

observed = pd.crosstab(test_data['test_group'].values, test_data['conversion'].values)
statistic, pvalue, dof, expected_values = stats.chi2_contingency(observed)

print(f't-statistic: {round(statistic, 2)}, p-value: {round(pvalue, 2)}')

if pvalue < alpha:
    print('The difference is statistically significant, Null Hypothesis is rejected.')
else:
    print('The difference is insignificant, Null Hypothesis cannot rejected.')


# In[12]:


pd.crosstab(test_data['test_group'].values, test_data['conversion'].values)


# In[10]:


test_data['test_group'].values


# In[11]:


test_data['conversion'].values


# ## Permutasyon Testi

# In[4]:


from scipy import stats

def statistic(x, y):
    return stats.ttest_ind(x, y).statistic

alpha = 0.05
    
x = test_data[test_data['test_group'] == 'a']['conversion']
y = test_data[test_data['test_group'] == 'b']['conversion']

results = stats.permutation_test((x, y), statistic, n_resamples=100)

print(f'statistic: {round(results.statistic, 2)}, p-value: {round(results.pvalue, 2)}')

if results.pvalue < alpha:
    print('The difference is statistically significant, Null Hypothesis is rejected.')
else:
    print('The difference is insignificant, Null Hypothesis cannot rejected.')


# ## Görselleştirme

# In[5]:


import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(8, 6))
sns.barplot(x=test_data['test_group'], 
            y=test_data['conversion'], 
            errorbar=('ci', 95)) # Confidence Intervals

plt.title('A/B Test Results')
plt.xlabel('Group')
plt.ylabel('Mean')

plt.show()


# In[7]:


import seaborn as sns

plt.figure(figsize=(10, 6))

sns.kdeplot(stats.norm.rvs(size=1000))
sns.kdeplot(stats.norm.rvs(size=1000))

plt.title('Distribution of A/B Groups')
plt.xlabel('Value')
plt.ylabel('Frequency')

plt.legend(['A', 'B'])
plt.show()


# In[8]:


import seaborn as sns

plt.figure(figsize=(10, 6))

sns.histplot(stats.norm.rvs(size=1000))
sns.histplot(stats.norm.rvs(size=1000))

plt.title('Histogram of A/B Groups')
plt.xlabel('Value')
plt.ylabel('Frequency')

plt.legend(['A', 'B'])
plt.show()



# In[9]:


import matplotlib.pyplot as plt
import seaborn as sns

# Verileri karıştırıyoruz çünkü şu anki sıralama dönüşüm değerine göre yapılmış durumda
# Gerçek verileri kullanmış olsaydık, burada tarih ve saat sıralaması yapılması gerekirdi
test_data = test_data.sample(frac=1).reset_index(drop=True)

# Kümülatif ortalamayı hesaplıyoruz - bu, zamanla dönüşüm değişimini gösterir
cumulative_metric_a = test_data[test_data['test_group'] == 'a']['conversion'].expanding().mean().reset_index(drop=True)
cumulative_metric_b = test_data[test_data['test_group'] == 'b']['conversion'].expanding().mean().reset_index(drop=True)

plt.figure(figsize=(10, 6))
plt.plot(cumulative_metric_a, label='A')
plt.plot(cumulative_metric_b, label='B')

plt.title('Cumulative Сonversion Rate Comparison')
plt.xlabel('Time')
plt.ylabel('Cumulative Сonversion Rate')

plt.legend()
plt.show()


# In[20]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Veri çerçevesi oluşturma
test_data = pd.DataFrame(data={
    'test_group': ['a']*7015 + ['b']*6987,
    'conversion': [1]*139 + [0]*(7015-139) + [1]*314 + [0]*(6987-314)
})

# Grafik boyutunu ayarla
plt.figure(figsize=(10, 6))

# KDE grafiği oluşturma
sns.kdeplot(data=test_data[test_data['test_group'] == 'a']['conversion'], label='Group A', color='blue', fill=True, alpha=0.5)
sns.kdeplot(data=test_data[test_data['test_group'] == 'b']['conversion'], label='Group B', color='orange', fill=True, alpha=0.5)

# Başlık ve etiketler
plt.title('KDE Plot of Conversion Rates for A/B Groups')
plt.xlabel('Conversion Rate')
plt.ylabel('Density')
plt.legend()
plt.show()


# In[ ]:




