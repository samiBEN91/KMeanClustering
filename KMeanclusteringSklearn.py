from sklearn.cluster import KMeans
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from matplotlib import pyplot as plt

import numpy as np
df = pd.read_csv("incomesami.csv")
#df.head()
print (df.head()) #voir les 5 premiers lignes
#print (df)
#df.info()

plt.title('Cluster Distribution')
plt.xlabel('Age')
plt.ylabel('Income($)')
#plt.scatter(df['Age'],df['Income($)'])

scaler = MinMaxScaler()

scaler.fit(df[['Income($)']])
df['Income($)'] = scaler.transform(df[['Income($)']])

scaler.fit(df[['Age']])
df['Age'] = scaler.transform(df[['Age']])

km = KMeans(n_clusters=3)
y_predicted = km.fit_predict(df[['Age','Income($)']])
print(y_predicted)
df['cluster']=y_predicted

cluster_centers=km.cluster_centers_


df1 = df[df.cluster==0]
df2 = df[df.cluster==1]
df3 = df[df.cluster==2]
plt.scatter(df1.Age,df1['Income($)'],color='green',marker='o',label='Income($)')
plt.scatter(df2.Age,df2['Income($)'],color='red',marker='o',label='Income($)')
plt.scatter(df3.Age,df3['Income($)'],color='black',marker='o',label='Income($)')
plt.scatter(km.cluster_centers_[:,0],km.cluster_centers_[:,1],color='purple',marker='*',label='centroid')


plt.legend()
plt.show()

sse = []
k_rng = range(1,10)
for k in k_rng:
    km = KMeans(n_clusters=k)
    km.fit(df[['Age','Income($)']])
    sse.append(km.inertia_)


plt.title('Elbow Plot')
plt.xlabel('K')
plt.ylabel('Sum of squared error')
plt.plot(k_rng,sse)
plt.show()
