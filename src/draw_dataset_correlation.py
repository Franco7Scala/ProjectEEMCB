import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd 


base_path = "/Users/francesco/Desktop"
sns.set(style="ticks", color_codes=True)
data = pd.read_csv(base_path + "/dataset_refixed.txt", sep=" ")
print('Sampling...')
data = data.sample(200)
print('Plotting...')
g = sns.pairplot(data, \
				 x_vars=["day_number", "holiday", "hour", "pv_production", "hydro_production", "biomass_production", "wind_production", "consumption", "transits", "oil_price", "gas_price", "carbon_price"], \
                 y_vars=["day_number", "holiday", "hour", "pv_production", "hydro_production", "biomass_production", "wind_production", "consumption", "transits", "oil_price", "gas_price", "carbon_price"])
print('Saving...')
plt.savefig(base_path + "/plotted.pdf", format="pdf")#, dpi=800)
print('Done!')