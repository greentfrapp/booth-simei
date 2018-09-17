import os
import json
import numpy as np

import notes
import car_data

hdb_units = {
	'155': 12 * 11,
	'156': 8 * 11,
	'157': 8 * 11,
	'158': 8 * 4,
	'159': 8 * 4,
	'160': 8 * 11,
	'161': 8 * 4,
	'162': 8 * 11,
	'163': 8 * 11,
	'164': 8 * 11,
	'165': 12 * 11,
	'166': 'NA',
}

hdb_prices = {
	'155': str(np.mean([374])).split('.')[0],
	'156': str(np.mean([415, 427])).split('.')[0],
	'157': str(np.mean([440, 496])).split('.')[0],
	'158': str(np.mean([505, 510])).split('.')[0],
	'159': str(np.mean([402])).split('.')[0],
	'160': str(np.mean([396])).split('.')[0],
	'161': str(np.mean([411, 438])).split('.')[0],
	'162': str(np.mean([568, 465])).split('.')[0],
	'163': str(np.mean([438, 456])).split('.')[0],
	'164': str(np.mean([471])).split('.')[0],
	'165': str(np.mean([457])).split('.')[0],
	'166': 'NA',
}

dbss_units = {
	'168': 'NA',
	'167A': 6 * 12,
	'167B': 4 * 12,
	'167C': 4 * 12,
	'167D': 4 * 12,
	'168A': 4 * 12,
	'168B': 4 * 12,
	'168C': 4 * 12,
	'168D': 6 * 12,
}

dbss_prices = {
	'168': 'NA',
	'167A': str(np.mean([613, 599])).split('.')[0],
	'167B': str(np.mean([613, 599])).split('.')[0],
	'167C': str(np.mean([613, 599])).split('.')[0],
	'167D': str(np.mean([613, 599])).split('.')[0],
	'168A': str(np.mean([613, 599])).split('.')[0],
	'168B': str(np.mean([613, 599])).split('.')[0],
	'168C': str(np.mean([613, 599])).split('.')[0],
	'168D': str(np.mean([613, 599])).split('.')[0],
}

condo_names = {
	'changi_rise': 'Changi Rise',
	'melville_park': 'Melville Park',
	'savannah': 'Savannah Condopark',
	'sunhaven': 'Sunhaven',
	'tropicana': 'Tropicana',
}

condo_units = {
	'changi_rise': 598,
	'melville_park': 1232,
	'savannah': 648,
	'sunhaven': 295,
	'tropicana': 40,
}

condo_prices = {
	'changi_rise': str(np.mean([697, 898])).split('.')[0],
	'melville_park': str(np.mean([691, 896])).split('.')[0],
	'savannah': str(np.mean([763, 978])).split('.')[0],
	'sunhaven': str(np.mean([739, 1101])).split('.')[0],
	'tropicana': str(np.mean([765, 936])).split('.')[0],
}

main_dir = 'geojson'

folders = {}

for folder in os.listdir(main_dir):
	if os.path.isdir('{}/{}'.format(main_dir, folder)) and folder not in ['jln_pelatok_park', 'meragi_road_park']:
		folders[folder] = []
		for filename in os.listdir('{}/{}'.format(main_dir, folder)):
			if '.json' in filename:
				with open('{}/{}/{}'.format(main_dir, folder, filename), 'r') as file:
					folders[folder].append(json.load(file))

for folder in folders:
	if folder == 'hdb':
		for feature in folders[folder]:
			feature['properties']['category'] = 1
			if feature['properties']['building:use'] == 'carpark':
				feature['properties']['type'] = 'Carpark'
			else:
				feature['properties']['type'] = 'HDB'
			if feature['properties']['addr:housenumber'] in ['166', '163']:
				feature['properties']['data'] = car_data.data[feature['properties']['addr:housenumber']]
				feature['properties']['has_car_data'] = True
			feature['properties']['name'] = 'Blk {}'.format(feature['properties']['addr:housenumber'])
			feature['properties']['units'] = hdb_units[feature['properties']['addr:housenumber']]
			feature['properties']['price'] = hdb_prices[feature['properties']['addr:housenumber']]
			if feature['id'] in notes.notes:
				feature['properties']['notes'] = notes.notes[feature['id']]
			else:
				feature['properties']['notes'] = ''
			if feature['id'] in notes.images:
				feature['properties']['images'] = notes.images[feature['id']]
	elif folder == 'parc_lumiere':
		for feature in folders[folder]:
			feature['properties']['category'] = 2
			if feature['properties']['building:use'] == 'carpark':
				feature['properties']['type'] = 'Carpark'
				feature['properties']['data'] = car_data.data['parc_lumiere']
				feature['properties']['has_car_data'] = True
			else:
				feature['properties']['type'] = 'DBSS'
			feature['properties']['name'] = 'Parc Lumiere Blk {}'.format(feature['properties']['addr:housenumber'])
			feature['properties']['units'] = dbss_units[feature['properties']['addr:housenumber']]
			feature['properties']['price'] = dbss_prices[feature['properties']['addr:housenumber']]
			if feature['id'] in notes.notes:
				feature['properties']['notes'] = notes.notes[feature['id']]
			else:
				feature['properties']['notes'] = ''
			if feature['id'] in notes.images:
				feature['properties']['images'] = notes.images[feature['id']]
	elif 'bungalows' in folder:
		for feature in folders[folder]:
			feature['properties']['category'] = 4
			feature['properties']['type'] = 'Semi-detached'
			if feature['id'] in notes.semid_names:
				feature['properties']['name'] = notes.semid_names[feature['id']]
			else:
				feature['properties']['name'] = 'NA'
			feature['properties']['units'] = 1
			feature['properties']['price'] = '~1200'
			if feature['id'] in notes.notes:
				feature['properties']['notes'] = notes.notes[feature['id']]
			else:
				feature['properties']['notes'] = ''
			if feature['id'] in ['way/454258732', 'way/454258730', 'way/454258767', 'way/454258705', 'way/454258743', 'way/454258772', 'way/454258711', 'way/454258749', 'way/454258788', 'way/454258720']:
				feature['properties']['data'] = car_data.data['jln_tiga_ratus']
				feature['properties']['has_car_data'] = True
			elif feature['id'] in ['way/454176576', 'way/454176581', 'way/454176573', 'way/454176572', 'way/454176574', 'way/454176568', 'way/454176578', 'way/454176580']:
				feature['properties']['data'] = car_data.data['jln_pergam']
				feature['properties']['has_car_data'] = True
			if feature['id'] in notes.images:
				feature['properties']['images'] = notes.images[feature['id']]
	elif folder in ['changi_rise', 'melville_park', 'savannah', 'sunhaven', 'tropicana']:
		for feature in folders[folder]:
			feature['properties']['category'] = 3
			feature['properties']['type'] = 'Condominium'
			feature['properties']['name'] = condo_names[folder]
			feature['properties']['units'] = condo_units[folder]
			feature['properties']['price'] = condo_prices[folder]
			if feature['id'] in notes.notes:
				feature['properties']['notes'] = notes.notes[feature['id']]
			else:
				feature['properties']['notes'] = ''
			if feature['id'] in notes.images:
				feature['properties']['images'] = notes.images[feature['id']]
			if folder in ['sunhaven', 'tropicana']:
				feature['properties']['data'] = car_data.data[folder]
				feature['properties']['has_car_data'] = True
	else:
		for feature in folders[folder]:
			feature['properties']['category'] = 0
			if feature['id'] in notes.notes:
				feature['properties']['notes'] = notes.notes[feature['id']]
			else:
				feature['properties']['notes'] = ''

features = []
for folder in folders:
	for feature in folders[folder]:
		features.append(feature)

collection = {
	'type': 'FeatureCollection',
 	'features': features,
}

with open('all_geojson.js', 'w') as file:
	file.write('var blocks = ' + json.dumps(collection))
