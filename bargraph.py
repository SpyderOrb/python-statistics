import matplotlib.pyplot as plt
import pandas as pd
# import interval_series

interval_csv = pd.read_csv('interval_series.csv')
x = interval_csv.head()
print(x)

interval_csv.groupby('Xi').count().plot.bar()



plt.show()