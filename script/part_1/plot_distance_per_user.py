import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
from matplotlib.colors import Normalize

def plot_distance_per_user(df):
    # Group by user and sum the total distance
    total_distance_per_user = df.groupby('Id')['TotalDistance'].sum().reset_index()
    
    # Normalize the TotalDistance values to a range [0, 1] for color mapping
    norm = Normalize(total_distance_per_user['TotalDistance'].min(), total_distance_per_user['TotalDistance'].max())
    
    # Get the viridis colormap
    cmap = mpl.colormaps['viridis_r']
    
    # Map normalized values to colors
    colors = cmap(norm(total_distance_per_user['TotalDistance']))
    
    # Plot the results
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Id', y='TotalDistance', data=total_distance_per_user, palette=colors)
    plt.title('Total Distance per User')
    plt.xlabel('User ID')
    plt.ylabel('Total Distance')
    plt.xticks(rotation=85)
    plt.show()
