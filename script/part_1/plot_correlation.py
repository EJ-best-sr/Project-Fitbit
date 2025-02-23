import seaborn as sns
import matplotlib.pyplot as plt

def plot_corr_amongst_all_columns(df):
    numerical_columns = df.select_dtypes(exclude='object').columns.tolist()
    correlation_matrix = df[numerical_columns].corr()
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(correlation_matrix, cmap = 'viridis', vmin=-1, vmax=1, annot=True, linewidths=0.5 )
    plt.title('Correlation Matrix of All Columns', fontsize=15)
    plt.show()


