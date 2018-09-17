import csv
import numpy as np

brands = []
carparks = []
data = {}
names = {
	'parc_lumiere': 'Parc Lumiere',
	'166': '166',
	'163': '163',
	'sunhaven': 'Sunhaven',
	'tropicana': 'Tropicana',
	'jln_pergam': 'Jln Pergam',
	'jln_tiga_ratus': 'Jln Tiga Ratus',
}

with open('car_data.csv', 'r') as file:
	reader = csv.reader(file)
	for i, row in enumerate(reader):
		if i == 0:
			for place in row:
				if place != '':
					carparks.append(place)
					data[place] = []
		else:
			brands.append(row[0])
			for j, count in enumerate(row[1:]):
				data[carparks[j]].append(int(count))

for name, full_name in names.items():
	data[name] = [{
		'x': brands[:-1],
		'y': list(100 * np.array(data[full_name][:-1]) / data[full_name][-1]),
		'marker':{
		    'color': ['#f39c12'] * 7 + ['#c0392b'] * 11 + ['#2980b9'] * 2 + ['#2ecc71'],
		  },
		'type': 'bar',
	}]
