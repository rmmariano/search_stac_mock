from urllib.parse import urlencode
from flask import jsonify
from catalog import utils
import requests
import logging
import json
import os

def setProviders():
	# In case of change in provider TYPE,
	# changes must be made to the file "ms3_search.py".
	with open('catalog/config/providers.json') as f:
		data = json.load(f)
		for key, value in data.items():
			os.environ[key] = value['urlr']
		return data
	return ''

def openSearchS2SAFE(provider, url, params):

	bbox = params['bbox']
	startdate = params['start']
	enddate = params['end']
	limit = params['count']
	path = params['path']
	row = params['row']

	query = 'https://scihub.copernicus.eu/apihub/search?format=json'
	query += '&q=platformname:Sentinel-2'
	if startdate != '' and enddate != '':
		query += ' AND beginposition:[{}T00:00:00.000Z TO {}T23:59:59.999Z]'.format(startdate, enddate)
	if params['cloud'] != '':
		query += ' AND cloudcoverpercentage:[0 TO {}]'.format(params['cloud'])
	if params['bbox'] != '':
		w, s, e, n = params['bbox'].split(',')
		footprintPoly = 'POLYGON (({0} {3} 0,{2} {3} 0,{2} {1} 0,{0} {1} 0,{0} {3} 0))'.format(w, s, e, n)
		query += ' AND (footprint:"Intersects({})")'.format(footprintPoly)
	query += '&rows={0}&start=0'.format(limit)
	logging.warning('ms3_search openSearchS2SAFE - provider {} query {}'.format(provider,query))

	try:
		r = requests.get(query, auth=('cartaxo', 'sitim666'), verify=True)
		if not r.status_code // 100 == 2:
			logging.warning('openSearchS2SAFE API returned unexpected response {}:'.format(r.status_code))
			return {}
		r_dict = json.loads(r.text)
	except requests.exceptions.RequestException as exc:
		logging.warning('openSearchS2SAFE error {}:'.format(exc))
		return {}

	totalResults = r_dict['feed']['opensearch:totalResults']
	if 'entry' not in r_dict['feed']:
		logging.warning(json.dumps(r_dict['feed'], indent=4))
		logging.warning('openSearchS2SAFE no entry for this feed:')
		return utils.make_geojson({}, 0, provider)
	
	scenes = r_dict['feed']['entry']
	if not isinstance(scenes, list):
		scenes = [scenes]

	features = list()

	for scene in scenes:
		properties = {}
		logging.warning(json.dumps(scene, indent=4))
		properties['id'] = scene['title']
		properties['dataset'] = 'S2_MSI'
		for data in scene['date']:
			if str(data['name']) == 'beginposition':
				properties['date'] = str(data['content'])[0:10]
		properties['path'] = ''
		properties['row'] = ''
		properties['resolution'] = '10'
		if not isinstance(scene['double'], list):
			scene['double'] = [scene['double']]
		for data in scene['double']:
			if str(data['name']) == 'cloudcoverpercentage':
				properties['cloud'] = data['content']

		properties['title'] = scene['title']
		properties['icon'] = scene['link'][2]['href']
		enclosure = list()
		link_dict = dict()
		link_dict['url'] = scene['link'][0]['href']
		link_dict['band'] = 'ALL'
		link_dict['radiometric_processing'] = ''
		link_dict['type'] = 'SCENE'
		enclosure.append(link_dict)

		properties['enclosure'] = enclosure
		logging.warning(json.dumps(properties, indent=4))

		feature = dict()
		foot = ''
		for data in scene['str']:
			if str(data['name']) == 'footprint':
				foot = data['content']
			if str(data['name']) == 'platformserialidentifier':
				properties['satellite'] = data['content']
			if str(data['name']) == 'instrumentshortname':
				properties['sensor'] = data['content']
		if foot.find('(((') != -1:
			s1 = foot.find('(((') + 3
			s2 = foot.find(')))')
		else:
			s1 = foot.find('((') + 2
			s2 = foot.find('))')
		foot = foot[s1:s2]
		foot = foot.replace(', ',',')
		foot = foot.split(',')
		lons = []
		lats = []
		coordinates = []
		for f in foot:
			tup = f.split(' ')
			lons.append(float(tup[0]))
			lats.append(float(tup[1]))
			coordinates.append([float(tup[0]),float(tup[1])])
		lonmin = min(lons)
		lonmax = max(lons)
		latmin = min(lats)
		latmax = max(lats)
		feature['geometry'] = {}
		feature['geometry']['type'] = 'Polygon'
		feature['geometry']['coordinates'] = [coordinates]
		properties['tl_longitude'] = lonmin
		properties['tl_latitude'] = latmax
		properties['tr_longitude'] = lonmax
		properties['tr_latitude'] = latmax
		properties['bl_longitude'] = lonmin
		properties['bl_latitude'] = latmin
		properties['br_longitude'] = lonmax
		properties['br_latitude'] = latmin
		feature['properties'] = properties
		feature['type'] = 'Feature'
		features.append(feature)
		logging.warning(json.dumps(feature, indent=4))

	return utils.make_geojson(features, totalResults, provider)


def satDevelopmentSeed(provider, url, params):
	bbox = params['bbox']
	startdate = params['start'],
	enddate = params['end']
	cloud = 10
	limit = params['count']
	path = params['path']
	row = params['row']

	query = url + '?collection:landsat-8'
	query += '&eo:cloud_cover:%s' % cloud
	query += '&datetime:%s/%s' % (startdate, enddate)
	query += '&landsat:path:%s' % path
	query += '&landsat:row:%s' % row
	query += '&limit={0}'.format(limit)

	print(query)
	logging.warning('ms3_search satDevelopmentSeed - query {}'.format(query))

	response = requests.get(query)
	response_dict = json.loads(response.text)

	if 'features' in response_dict:
		for feature in response_dict['features']:
			# if not utils.remote_file_exists(feature['assets']['thumbnail']['href']):
			#	 continue
			properties = feature['properties']
			properties['title'] = properties['id']
			properties['icon'] = feature['assets']['thumbnail']['href']

			bbox = feature['bbox']
			properties['tr_longitude'] = bbox[0]
			properties['tr_latitude'] = bbox[1]
			properties['br_longitude'] = bbox[0]
			properties['br_latitude'] = bbox[3]
			properties['bl_longitude'] = bbox[2]
			properties['bl_latitude'] = bbox[3]
			properties['tl_longitude'] = bbox[2]
			properties['tl_latitude'] = bbox[1]

			enclosure = list()
			for key, value in feature['assets'].items():
				link_dict = dict()
				link_dict['url'] = value['href']
				link_dict['band'] = key
				link_dict['radiometric_processing'] = ''
				link_dict['type'] = 'SCENE'
				enclosure.append(link_dict)

			properties['enclosure'] = enclosure

	return response_dict


def developmentSeedStac(provider, url, paramss):
	startdate = paramss['start']
	enddate = paramss['end']
	cloud = 5

	query = ''
	#query = 'collection=landsat-8-l1&'
	if paramss['bbox'] != '':
		wlon, slat, elon, nlat = paramss['bbox'].split(',')
		if provider == 'KEPLER_STAC':
			bbox = 'bbox={},{},{},{}&'.format(wlon, slat, elon, nlat)
		else:
			bbox = 'bbox=[{},{},{},{}]&'.format(wlon, slat, elon, nlat)
		query += bbox
	if startdate != '' and enddate != '':
		datespan = 'time={}T00:00:00Z/{}T23:59:59Z&'.format(startdate,enddate)
		query += datespan
# https://stac.amskepler.com/stac/search?bbox=-180,-90,180,90&time=2018-02-12T23%3A20%3A50Z&limit=10
	query += 'eo:cloud_cover=0/{}&'.format(cloud)
	query += 'limit={}'.format(paramss['count'])

	if provider == 'KEPLER_STAC':
		query = 'https://stac.amskepler.com/stac/search' + '?' + query
	else:
		query = url + '?' + query
# https://sat-api.developmentseed.org/search/stac?datetime=2017&collection=landsat-8&eo:cloud_cover=0/20
	logging.warning('ms3_search developmentSeedStac - provider {} query {}'.format(provider,query))
	response = requests.get(query)
	response_dict = json.loads(response.text)
	logging.warning(json.dumps(response_dict, indent=4))
	features = list()
	if 'features' not in response_dict:
		return utils.make_geojson({}, 0, provider)

	for val in response_dict['features']:
		#logging.warning(json.dumps(val))

		scenes = {}
		scenes['id'] = val['id']
		bbox = val['bbox']
		scenes['icon'] = val['assets']['thumbnail']['href']
		scenes['tr_longitude'] = bbox[0]
		scenes['tr_latitude'] = bbox[1]
		scenes['br_longitude'] = bbox[0]
		scenes['br_latitude'] = bbox[3]
		scenes['bl_longitude'] = bbox[2]
		scenes['bl_latitude'] = bbox[3]
		scenes['tl_longitude'] = bbox[2]
		scenes['tl_latitude'] = bbox[1]
		
		scenes['tr_longitude'] = bbox[2]
		scenes['tr_latitude'] = bbox[3]
		scenes['br_longitude'] = bbox[2]
		scenes['br_latitude'] = bbox[1]
		scenes['bl_longitude'] = bbox[0]
		scenes['bl_latitude'] = bbox[1]
		scenes['tl_longitude'] = bbox[0]
		scenes['tl_latitude'] = bbox[3]

		#for key, value in val.items():
			#logging.warning('ms3_search developmentSeedStac - keyxxx {} - {}'.format(key,value))
		if 'eo:platform' in val['properties']:
			scenes['satellite'] = val['properties']['eo:platform']
		else:
			scenes['satellite'] = 'CBERS-4'
			scenes['path'] = val['properties']['cbers:path']
			scenes['row'] = val['properties']['cbers:row']
		scenes['sensor'] = val['properties']['eo:instrument']
		if 'eo:cloud_cover' in val['properties']:
			scenes['cloud'] = val['properties']['eo:cloud_cover']
		else:
			scenes['cloud'] = -1
		scenes['date'] = val['properties']['datetime'][:10]
		if 'sentinel:product_id' in val['properties']:
			scenes['title'] = val['properties']['sentinel:product_id']
		elif 'landsat:product_id' in val['properties']:
			scenes['title'] = val['properties']['landsat:product_id']
		else:
			scenes['title'] = val['id']

		logging.warning('ms3_search developmentSeedStac - scenes {}'.format(scenes))

		enclosure = list()
		for key, value in val['assets'].items():
			#logging.warning('ms3_search developmentSeedStac - key {} value {}'.format(key,value))
			link_dict = dict()
			link_dict['url'] = value['href']
			link_dict['band'] = key
			link_dict['radiometric_processing'] = 'DN'
			link_dict['type'] = 'SCENE'
			enclosure.append(link_dict)

		scenes['enclosure'] = enclosure
		feature = dict()
		feature['geometry'] = val['geometry']
		feature['properties'] = scenes
		feature['type'] = 'Feature'
		features.append(feature)

	logging.warning(json.dumps(feature, indent=4))
	if 'meta' in response_dict:
		totalResults = response_dict['meta']['found']
	else:
		totalResults = len(response_dict['features'])
	return utils.make_geojson(features, totalResults, provider)
	"""
	return response_dict

	headers = { 'Accept': 'application/geo+json'}
	params = {}
	params['query'] = {'eo:cloud_cover' : {"lt": cloud}}
	params['limit'] = int(paramss['count'])
	if paramss['bbox'] != '':
		bbox = paramss['bbox'].split(',')
		bbox = [float(i) for i in bbox]
		params['bbox'] = bbox
	logging.warning('ms3_search developmentSeedStac - params {}'.format(params))
	r = requests.post(url, params=params, headers = headers)
	logging.warning('ms3_search developmentSeedStac - result {}'.format(r.json()))

	return r.json()
	"""
def developmentSeed(provider, url, params):
	bbox = params['bbox']
	startdate = params['start']
	enddate = params['end']
	cloud = 10
	limit = params['count']
	path = params['path']
	row = params['row']

	if bbox != '':
		wlon, slat, elon, nlat = bbox.split(',')
	else:
		wlon = slat = elon = nlat = ''

	query = url + '?search='
	params = 'satellite_name:landsat-8'
# https://api.developmentseed.org/satellites/?search=satellite_name:landsat-8+
# AND+acquisitionDate:[2018-01-17+TO+2018-03-01]+
# AND+cloud_coverage:[-1+TO+7.0]+
# AND+upperLeftCornerLatitude:[-13.2+TO+1000]+
# AND+lowerRightCornerLatitude:[-1000+TO+-13.1]+
# AND+lowerLeftCornerLongitude:[-1000+TO+-46.3]+
# AND+upperRightCornerLongitude:[-46.4+TO+1000]&limit=299
	if wlon != '':
		qbbox = '+AND+upperLeftCornerLatitude:[{}+TO+1000]+AND+lowerRightCornerLatitude:[-1000+TO+{}]' \
			'+AND+lowerLeftCornerLongitude:[-1000+TO+{}]+AND+upperRightCornerLongitude:[{}+TO+1000]'.format(
				slat, nlat, elon, wlon)
		params += qbbox

	if startdate != '' and enddate != '':
		acquisitionDate = 'acquisitionDate:[%s+TO+%s]' % (startdate, enddate)
		if params != '':
			params += '+AND+'
		params += acquisitionDate
	if cloud != '':
		cloud_coverage = 'cloud_coverage:[-1+TO+%s]' % cloud
		if params != '':
			params += '+AND+'
		params += cloud_coverage

	if path != '':
		path = 'path:[%s+TO+%s]' % (path, path)
		if params != '':
			params += '+AND+'
		params += path

	if row != '':
		row = 'row:[%s+TO+%s]' % (row, row)
		if params != '':
			params += '+AND+'
		params += row

	params += '&limit={0}'.format(limit)
	query += params
	print(query)
	logging.warning('ms3_search developmentSeed - query {}'.format(query))

	response = requests.get(query)
	response_dict = json.loads(response.text)

	features = list()
	if 'results' in response_dict:
		for val in response_dict['results']:
			if not utils.remote_file_exists(val['aws_thumbnail']):
				continue

			identifier = val['product_id']
			if cloud is not None and float(val['cloud_coverage']) > float(cloud):
				continue

			enclosure = list()

			# exists = True
			for url in val['download_links']['aws_s3']:
				# if utils.remote_file_exists(url):
				band = os.path.basename(url).split('_')[-1].split('.')[0]
				link_dict = dict()
				link_dict['provider'] = 'aws_s3'
				link_dict['url'] = url
				link_dict['band'] = band
				link_dict['radiometric_processing'] = ''
				link_dict['type'] = 'SCENE'
				enclosure.append(link_dict)
			#	 else:
			#		 exists = False
			#		 # print('developmentSeed - url is not valid {}'.format(url))
			#		 break
			# if not exists:
			#	 continue

			scenes = {}
			scenes['id'] = identifier
			scenes['satellite'] = 'LC8'
			scenes['sensor'] = 'OLI'
			scenes['cloud'] = val['cloud_coverage']
			scenes['date'] = val['acquisitionDate']
			scenes['pathrow'] = '{0:03d}{1:03d}'.format(
				val['path'], val['row'])
			scenes['path'] = int(val['path'])
			scenes['row'] = int(val['row'])
			scenes['resolution'] = int(
				val['GRID_CELL_SIZE_REFLECTIVE'])

			scenes['title'] = val['scene_id']
			scenes['icon'] = val['aws_thumbnail']
			scenes['tl_longitude'] = float(
				val['upperLeftCornerLongitude'])
			scenes['tl_latitude'] = float(
				val['upperLeftCornerLatitude'])
			scenes['tr_longitude'] = float(
				val['upperRightCornerLongitude'])
			scenes['tr_latitude'] = float(
				val['upperRightCornerLatitude'])
			scenes['bl_longitude'] = float(
				val['lowerLeftCornerLongitude'])
			scenes['bl_latitude'] = float(
				val['lowerLeftCornerLatitude'])
			scenes['br_longitude'] = float(
				val['lowerRightCornerLongitude'])
			scenes['br_latitude'] = float(
				val['lowerRightCornerLatitude'])
			scenes['enclosure'] = enclosure

			feature = dict()
			feature['geometry'] = val['data_geometry']
			feature['properties'] = scenes
			feature['type'] = 'Feature'
			features.append(feature)

	return utils.make_geojson(features, response_dict['meta']['found'], provider)


def opensearch(provider, url, params):
	logging.warning('ms3_search opensearch - provider {} url {}'.format(provider,url))
	logging.warning('ms3_search opensearch - provider {} params {}'.format(provider,urlencode(params)))
	logging.warning('ms3_search opensearch - provider {} {}'.format(provider,url + 'granule.json?&' + urlencode(params)))
	try:
		response = requests.get(url + 'granule.json?&' + urlencode(params))
	except requests.exceptions.RequestException as exc:
		logging.warning('ms3_search opensearch - Error {}'.format(exc))
		resp = jsonify({'code': 500, 'message': 'Internal Server Error'})
		resp.status_code = 500
		resp.headers.add('Access-Control-Allow-Origin', '*')
		return resp

	response = json.loads(response.text)
	response['provider'] = provider
	# TODO: validate quicklook or images download url
	return response

def cubesearch(provider, url, params):
	logging.warning('cubesearch - {}'.format(url + 'granule.json?&' + urlencode(params)))
	response = requests.get(url + 'granule.json?&' + urlencode(params))
	response = json.loads(response.text)
	logging.warning('cubesearch - response {}'.format(response))
	response['provider'] = provider
	# TODO: validate quicklook or images download url
	return response


def search(params):
	logging.warning('search - {}'.format(urlencode(params)))
	results = dict()
	providers = json.loads(params['providers'])
	for key, value in providers.items():
		logging.warning('search - key {} - value {}'.format(key,value))
		if value['type'] == 'cubesearch':
			logging.warning('search - cubesearch - {}'.format(urlencode(params)))
			results[key] = cubesearch(key, value['url'], params)
		elif value['type'] == 'opensearch':
			logging.warning('search - opensearch - {}'.format(urlencode(params)))
			results[key] = opensearch(key, value['urlr'], params)
		elif value['type'] == 'dev_seed':
			results[key] = developmentSeed(key, value['url'], params)
		elif value['type'] == 'dev_stac':
			results[key] = developmentSeedStac(key, value['url'], params)
		elif value['type'] == 'sat_dev_seed':
			results[key] = satDevelopmentSeed(key, value['url'], params)
		elif value['type'] == 's2safe':
			results[key] = openSearchS2SAFE(key, value['url'], params)

	features = list()
	providers = list()
	for key, value in results.items():
		featlist = value['features']
		for feature in featlist:
			feature['properties']['provider'] = key
		features += featlist
		value.pop('features')
		providers.append(value)

	response = dict()
	response['features'] = features
	response['providers'] = providers
	return jsonify(response)
