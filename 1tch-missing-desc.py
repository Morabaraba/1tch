import sys
import csv
import json
from urllib.request import urlopen

archlinux_url_query = 'https://www.archlinux.org/packages/search/json/?q='

lines = [ ['name', 'desc', ] ]

def main(csv_file_path):
	with open(csv_file_path, newline='') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:			
			if row[1] == '<NULL>':				
				json_doc = urlopen(archlinux_url_query + row[0]).read().decode('utf-8')
				meta = json.loads(json_doc)
				results = meta.get('results', [])
				if len( results ) != 0:
					line = [row[0], results[0].get('pkgdesc', '<NULL>')]
					lines.append(line)
					
	with open('pages/missing-desc.csv', 'w', newline='') as outfile:
		writer = csv.writer(outfile)
		writer.writerows(lines)

if __name__ == '__main__':
	main(sys.argv[1])