import pandas as pd
from sklearn.preprocessing import RobustScaler
from sklearn.decomposition import FactorAnalysis
from sklearn.impute import KNNImputer
import numpy as np
from sklearn.utils.extmath import randomized_svd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

#read in trimmed data, make sure to set tract to be string
df = pd.read_csv('../data/trimmed_data.csv', dtype={'Census tract 2010 ID':str})
df = df.set_index(['Census tract 2010 ID','County Name','State/Territory'])

#drop underinvestment since it's mostly null
df = df.drop('Underinvestment',axis=1)

numeric_features = df.drop(['Low_Income','Disadvantaged'],axis=1).columns
categorical_features = df[['Low_Income','Disadvantaged']].columns

#scale and impute data
X = df.copy()
numeric_transformer = Pipeline(steps=[
    ('imputer', KNNImputer(n_neighbors=10)),
    ('scaling', RobustScaler())
])
categorical_transformer = Pipeline(steps=[
    ('encoder', OneHotEncoder(handle_unknown='ignore', drop='first'))])

#combine preprocessers and specify columns
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)])
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor)
])

X_scaled = pipeline.fit_transform(X)
#%%
#decide the number of factors using parallel analysis

#define parallel analysis function
def perform_parallel_analysis(data, num_simulations=100, percentile=95):
    _, actual_sing_values, _ = randomized_svd(data, n_components=min(data.shape) - 1)
    random_sing_values = np.zeros((num_simulations, len(actual_sing_values)))

    for i in range(num_simulations):
        random_data = np.random.normal(0, 1, size=data.shape)
        _, sing_values, _ = randomized_svd(random_data, n_components=min(data.shape) - 1)
        random_sing_values[i, :] = sing_values

    sing_value_thresholds = np.percentile(random_sing_values, percentile, axis=0)
    actual_eigenvalues = actual_sing_values ** 2
    thresholds = sing_value_thresholds ** 2
    num_factors = np.sum(actual_eigenvalues > thresholds)
    
    return num_factors

num_factors = perform_parallel_analysis(X_scaled)
print("Number of factors suggested by Parallel Analysis:", num_factors)

#%%
#analyze factor loadings

n_factors =11 #as suggested by parallel analysis above
fa = FactorAnalysis(n_components=n_factors, rotation='varimax')
fa.fit(X_scaled)

#%%
#turn factor loadings into df and view
loadings = fa.components_.T
loadings_df = pd.DataFrame(loadings, columns=['Factor {}'.format(i+1) for i in range(n_factors)], index=df.columns)
print(loadings_df)

#plot loadings
plt.rcParams['figure.dpi'] = 300
plt.figure(figsize=(12, 10)) 
#create heatmap without annotations
sns.heatmap(loadings_df, cmap='coolwarm', center=0, robust=True)
#add annotations
for (i, j), value in np.ndenumerate(loadings_df.values):
    plt.text(j + 0.5, i + 0.5, f"{value:.2f}", 
             ha='center', va='center', 
             fontsize=10)
plt.title('Factor Loadings')
plt.tight_layout()
plt.savefig('../images/factor_loadings.png')

#%%
#clustering with k means

#transform data
X_factor_scores = fa.transform(X_scaled)

#investigate elbow plot to determine k
inertia = []
for k in range(1, 30):  # Change the range as needed
    kmeans = KMeans(n_clusters=k, random_state=123)
    kmeans.fit(X_factor_scores)
    inertia.append(kmeans.inertia_)

# Plot the Elbow Curve
plt.figure(figsize=(8, 6))
plt.plot(range(1, 30), inertia, marker='o')  # Change the range as needed
plt.title('Elbow Method For Optimal k')
plt.xlabel('Number of clusters')
plt.ylabel('Inertia')
plt.tight_layout()
plt.show()

#it looks like the graph has an elbow around k=11

#%%
#pick k of 5 
kmeans = KMeans(n_clusters=11, random_state=123)
kmeans.fit(X_factor_scores)

#add labels to df
labels = kmeans.labels_
df['Cluster'] = labels

#plot the clusters using the first two factors to visualize
plt.figure(figsize=(8, 6))
plt.scatter(X_factor_scores[:, 0], X_factor_scores[:, 1], c=labels, cmap='viridis') 
centers = kmeans.cluster_centers_
plt.scatter(centers[:, 0], centers[:, 1], c='red', s=100, alpha=0.75)  # Plot the centroids
plt.title('Clusters and Centroids')
plt.tight_layout()
plt.savefig('../images/clusters.png')

#export to csv for later use in qgis
df.reset_index().to_csv('../data/clustered_data.csv', index=False)
