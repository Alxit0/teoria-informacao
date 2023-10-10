import matplotlib.pyplot as plt

histogram_data = {1: 10, 2: 15, 4: 30}

bins = list(histogram_data.keys())
frequencies = list(histogram_data.values())

plt.bar(bins, frequencies, align='center')

plt.xticks()

plt.show()
