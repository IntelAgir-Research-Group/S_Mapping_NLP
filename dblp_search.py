from lxml import etree

DBLP_XML = '../data/dblp-2022-04-01.xml'
YEAR_MIN = 2007
YEAR_MAX = 2022
KEYWORDS = ['authorship']
VENUES = tuple([
	'conf/aaai',
	'conf/ijcai',
	'conf/uai',
	'conf/jelia',
	'conf/aistats',
	'conf/aied',
	'conf/ecai',
	'conf/cpaior',
	'conf/mdai',
	'conf/icaart',
	'conf/pricai',
	'conf/icaart',
	'conf/acl',
	'conf/coling',
	'conf/eacl',
	'conf/naacl',
	'conf/cicling',
	'conf/pacling',
	'conf/ijcnn',
	'conf/esann',
	'conf/cvpr',
	'conf/sspr',
	'conf/icpr',
	'conf/icml',
	'conf/ecml',
	'conf/sigir',
	'conf/ecir',
	'conf/spire',
	'conf/emnlp',
	'conf/conll',
	'conf/ijcnlp',
	'conf/inlg',
])

# Iterate over a large-sized xml file without the need to store it in memory in
# full. Yields every next element. Source:
# https://stackoverflow.com/questions/9856163/using-lxml-and-iterparse-to-parse-a-big-1gb-xml-file
def iterate_xml(xmlfile):
#	try:
	doc = etree.iterparse(xmlfile,events=('start','end'),load_dtd=True)
	_, root = next(doc)
	start_tag = None
	for event, element in doc:
		try:
			if event == 'start' and start_tag is None:
				start_tag = element.tag
			if event == 'end' and element.tag == start_tag:
				yield element
				start_tag = None
				root.clear()
		except:
			print('Error reading elements.')
#	except:
#		print('Error parsing the document.')

if __name__ == "__main__":
    hits = 0


    # Parse all entries in the DBLP database.
    for dblp_entry in iterate_xml(DBLP_XML):
        key = dblp_entry.get('key')

        # The db key should start with any of the venues we are interested in,
        # as well as be within the desired year range.
        if (key.startswith(VENUES) and
            int(dblp_entry.find('year').text) >= YEAR_MIN and
            int(dblp_entry.find('year').text) <= YEAR_MAX):
            # Remove any potential HTML content (such as <i>) from the title.
            title = ''.join(dblp_entry.find('title').itertext())

            # If the title contains any of the keywords (case-sensitive) add to
            # result.
            if any(keyword in title for keyword in KEYWORDS):
                # Merge the names of all authors of the work.
                authors = ' & '.join(''.join(author.itertext()) for author in
                    dblp_entry.findall('author'))

                # Obtain the source (usually in the form of a DOI link).
                ee = dblp_entry.find('ee')
                if ee is not None:
                    ee = ee.text

                # Print the current result to stdout as a csv line.
                print(hits,
                      title.replace(',', ';'),
                      dblp_entry.find('year').text,
                      authors,
                      key,
                      ee,
                      sep=', ')

                hits += 1
