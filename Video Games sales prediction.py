#!/usr/bin/env python
# coding: utf-8

# Aim:
# 
# A)To estimate the overall sales by applying four Regression Algorithms(Multiple, Support Vector Machine, Decision tree, Random Forest) on the data and find out the accuracy respectively.
# 
# B)Perform EDA and find out output to the following,
# 
# 1)Plot a bargraph for the values of mean of 
# Sales bought out by North America, Europe, Japan,other regions and find out the region with highest sales
# 
# 2)Find out the game that has had the highest sales in the year 2006.
# 
# 3)Name the top 10 Publishers that are currently gaining the maximum profit?
# 
# 4)Estimate the year which has had the maximum number of sales world-wide
# 
# 5)Plot a graph and pick the Genres of Video Games that has been a great attention for people
# 
# 6)Plot a graph to represent the number of games released per decade
# 
# C)Compare the accuracies and conclude the best model(among the four) for the dataset picked.
# 
# Description of the Dataset:
# 
# The dataset worked on is about Video games. As it is a well known fact that in today's world, the gaming industry has shown tremendous growth with sales and is in high demand. 
# 
# The chosen dataset contains the following features
# 
# •Rank - Ranking of overall sales
# 
# •Name - The games name
# 
# •Platform - Platform of the games release (i.e. PC,PS4, etc.)
# 	
# •Year - Year in which the game released
# 	
# •Genre - Genre of the game
# 	
# •Publisher - Publisher of the game
# 
# •NA_Sales - Sales in North America (in millions)
# 
# •EU_Sales - Sales in Europe (in millions)
# 	
# •JP_Sales - Sales in Japan (in millions)
# 
# •Other_Sales - Sales in the rest of the world (in millions)
# 	
# •Global_Sales - Total worldwide sales.(Target Variable)

# In[1]:


#Importing Libraries
import pandas as pd
pd.set_option('max_rows',100000)
pd.options.mode.chained_assignment=None
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


#Importing the dataset
df=pd.read_csv('Video_games.csv')
df.head(3)


# In[3]:


#Number of rows and columns of the dataset
df.shape


# **Exploratory Data Analysis**

# In[4]:


df.describe()


# In[5]:


df.info()


# In[6]:


#Mean of the following features

North_America_Sales=df['NA_Sales'].mean()
Europe_Sales=df['EU_Sales'].mean()
Japan_Sales=df['JP_Sales'].mean()
Other_Country_sales=df['Other_Sales'].mean()


# 1) Plot a graph of the values for mean of Sales bought out by North America, Europe, Japan,other regions and find out the region with highest sales
# 

# In[7]:


#Bar Graph
labels=['North_America_Sales','Europe_Sales','Japan_Sales','Other_Country_sales']
values=[North_America_Sales,Europe_Sales,Japan_Sales,Other_Country_sales]
plt.bar(labels,values,color='maroon',width=0.4)
plt.xlabel('Sales in the countries')
plt.ylabel('Sales in dollars')
plt.title('Sales across different regions of the world')


# From the above plotted Bar graph, it is well understood that North America stands on top where in the maximum sales has been covered.

# 2)Find out the game that has had the highest sales in the year 2006.

# In[8]:


df_2006=df[df['Year']==2006]
Max_game=df_2006.loc[df_2006['Global_Sales'].idxmax()]
print(Max_game['Name'],"has had the maximum Global Sales in the year 2006")


# 3)Name the top 10 Publishers that are currently gaining the maximum profit? 

# In[9]:


top_publishers=pd.DataFrame(df.groupby('Publisher')[['Global_Sales']].sum().sort_values(by=['Global_Sales'],ascending=False))
top_publishers.head(10)


# 4)Estimate the year which has had the maximum number of sales world-wide

# In[10]:


#Number of game releases per year 

plt.figure(figsize=(8,6))
plt.title("Number of release per Year")
sns.distplot(df['Year'],color='Blue')


# In the Year 2009, there has been maximum sales of Video Games

# 5)Plot a graph and pick the Genres of Video Games that has been a great attention for people

# In[11]:


#Sales vs Year 
plt.figure(figsize=(10,8))
df.groupby(['Genre'])['Global_Sales'].sum().plot(kind='pie')


# From the above graph, we can conclude that, Sports and Action kind of Video Games have been in a great attention for people

# 6)Plot a graph to represent the number of games released per decade

# In[12]:


years = ["1980_1990", "1990_2000", "2000_2010", "2010_2020"]
df['decade']=pd.cut(df['Year'],labels=years,bins=4)
df['decade'].value_counts().plot(kind='barh')


# The decade 2000 to 2010 has bought a great attention to people for Video Games

# **Feature Engineering**

# In[13]:


#Feature Selection
#Removing Rank, Name and Year column as it does not have any significance over the dependent variable
df.drop(['Rank','Name','Year','decade'],axis='columns',inplace=True)
df.head()


# In[14]:


#Dealing with missing values
df.isnull().sum()


# In[15]:


#Removing the null values, since the missing values are very comparatively less
df=df.dropna()


# In[16]:


#Dataframe with no null values
df.isnull().sum()


# In[17]:


df.head(3)


# In[18]:


#Dealing with categorical Variables
df_category=df[['Platform','Genre','Publisher','Global_Sales']]
df_category.head(3)


# In[19]:


#Implementing Chi2 test for feature selection to find out the significance on target variable
#First Applying Label Encoder

#Platform column
df_category['Platform']=df_category['Platform'].astype('category')
df_category['Platform']=df_category['Platform'].cat.codes

#Genre column
df_category['Genre']=df_category['Genre'].astype('category')
df_category['Genre']=df_category['Genre'].cat.codes

#Publisher column
df_category['Publisher']=df_category['Publisher'].astype('category')
df_category['Publisher']=df_category['Publisher'].cat.codes


# In[20]:


df_category.head(3)


# In[21]:


#Splitting the variables
A=df_category[['Platform','Genre','Publisher']]
b=df_category['Global_Sales']
b=b.astype('int')


# In[22]:


from sklearn.model_selection import train_test_split
A_train,A_test,b_train,b_test=train_test_split(A,b,test_size=0.3,random_state=1)


# In[23]:


from sklearn.feature_selection import chi2
f_p_values=chi2(A_train,b_train)


# In[24]:


f_p_values


# In[25]:


f_values=pd.Series(f_p_values[0])
f_values.index=A_train.columns
f_values.sort_values(ascending=False)


# In[26]:


p_values=pd.Series(f_p_values[1])
p_values.index=A_train.columns
p_values.sort_values()


# Considering the F score and p value, we can understand the relation of the categorical variable over the dependent variable. 
# That is Publisher>Platform>Genre.
# So, we can drop the Genre feature as it does not have much influence on the target variable. 

# In[27]:


df.drop(['Genre'],axis='columns',inplace=True)
df.head(3)


# In[28]:


df.shape


# **Dealing with  categorical variables

# In[29]:


#Platform feature
df['Platform'].value_counts()


# In[30]:


top_10_Platform=[x for x in df['Platform'].value_counts().sort_values(ascending=False).head(10).index]
top_10_Platform


# In[31]:


for i in top_10_Platform:
  df[i]=np.where(df['Platform']==i,1,0)


# In[32]:


df.head(3)


# In[33]:


df=df.drop(['Platform'],axis='columns')


# In[34]:


df['Publisher'].value_counts()


# In[35]:


top_10_Publisher=[x for x in df['Publisher'].value_counts().sort_values(ascending=False).head(10).index]
top_10_Publisher


# In[36]:


for i in top_10_Publisher:
  df[i]=np.where(df['Publisher']==i,1,0)


# In[37]:


df=df.drop(['Publisher'],axis=1)


# In[38]:


df_last=df['Global_Sales']


# In[39]:


df.drop(['Global_Sales'],axis='columns',inplace=True)


# In[40]:


df=pd.concat([df,df_last],axis=1)


# In[41]:


df.head(3)


# In[42]:


X=df.iloc[:,:-1]
y=df.iloc[:,-1]


# In[43]:


from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3,random_state=1)
y=y.astype('int')


# In[44]:


from sklearn.linear_model import LinearRegression
mr=LinearRegression()
mr.fit(X_train,y_train)


# In[46]:


mr_pred=mr.predict(X_test)


# In[47]:


from sklearn.metrics import r2_score
mr_score=r2_score(y_test,mr_pred)
mr_score=float(int(mr_score*(10**2))/10**2)
mr_score=mr_score*100
print("The score of Multiple Regression is",mr_score,"%")


# In[48]:


#Support Vector Regression
from sklearn.svm import SVR
svr = SVR()
svr.fit(X_train, y_train)


# In[50]:


svr_pred=svr.predict(X_test)


# In[51]:


from sklearn.metrics import r2_score
svr_score=r2_score(y_test,svr_pred)
svr_score=float(int(svr_score*(10**2))/10**2)
svr_score=svr_score*100
print("The score of Support Vector Regressor is",svr_score,"%")


# In[52]:


#Decision Tree Regressor
from sklearn.tree import DecisionTreeRegressor
dtr= DecisionTreeRegressor()
dtr.fit(X_train, y_train)


# In[53]:


dtr_pred=dtr.predict(X_test)


# In[54]:


from sklearn.metrics import r2_score
dtr_score=r2_score(y_test,dtr_pred)
dtr_score=float(int(dtr_score*(10**2))/10**2)
dtr_score=dtr_score*100
print("The score of Decision Tree is",dtr_score,"%")


# In[55]:


#Random Forest
from sklearn.ensemble import RandomForestRegressor
rfr = RandomForestRegressor()
rfr.fit(X_train, y_train)


# In[56]:


rfr_pred=rfr.predict(X_test)


# In[57]:


from sklearn.metrics import r2_score
rfr_score=r2_score(y_test,rfr_pred)
rfr_score=float(int(rfr_score*(10**2))/10**2)
rfr_score=rfr_score*100
print("The score of Random Forest Regressor is",rfr_score,"%")


# In[58]:


model=['Multiple Regression','Support Vector Regressor','Decision Tree','Random Forest']
accuracy=[mr_score,svr_score,dtr_score,rfr_score]
plt.figure(figsize=(6,4))
c = ['red', 'violet', 'blue', 'orange']
plt.barh(model,accuracy,align='center',color=c)
plt.xlabel("Accuracy")
plt.ylabel("Regression Models")
plt.title("Regression Model Scores")


# **Conclusion**
# 
# Among the tested four regression algorithms, the best fit algorithm is Multiple Regression followed by Random Forest. 
# 
# We have accquired almost 99% via Multiple Regression and 98% via Random Forest 
