#!/usr/bin/env python
from lxml import html
import requests
import sys

def getDetail(part):
	print part[:7]

def getDetails(barcode):
	page = requests.get('http://www.digikey.com/product-detail/en/0/0/' + barcode[:7])
	tree = html.fromstring(page.text)


	part = {}

	part['ProductNumber'] = tree.xpath("//meta[@name='WT.pn_sku']/@content")
	part['MfgProductNumber'] = tree.xpath("//meta[@itemprop='name']/@content")
	part['Description'] = tree.xpath("//td[@itemprop='description']/text()")
	part['Datasheet'] = tree.xpath("//a[@class='lnkDatasheet']/@href")
	part['ProductPhoto'] = tree.xpath("//a[@class='lnkProductPhoto']/@href")

	print part


while True:
	code = raw_input('Please scan barcode, or press q to quit.\r\nPartGrabber> ')
	if code == 'q': sys.exit()
	elif len(code) > 7: getDetails(code)
