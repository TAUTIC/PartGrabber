#!/usr/bin/env python

# The MIT License (MIT)
#
# Copyright (c) 2014 Jayson Tautic
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



from lxml import html
import requests
import sys

def getDetail(part):
	print part[:7]

def getDetails(barcode):
	page = requests.get('http://www.digikey.com/product-detail/en/0/0/' + barcode[:7])
	tree = html.fromstring(page.text)

	part = {}

	part['ProductNumber'] = tree.xpath("//meta[@name='WT.pn_sku']/@content")[0]
	part['MfgProductNumber'] = tree.xpath("//meta[@itemprop='name']/@content")[0]
	part['Description'] = tree.xpath("//td[@itemprop='description']/text()")[0]
	part['Datasheet'] = tree.xpath("//a[@class='lnkDatasheet']/@href")[0]
	part['ProductPhoto'] = tree.xpath("//a[@class='lnkProductPhoto']/@href")[0]
	 
	detailsHeader = []
	detailsData = []

	ths = tree.xpath("//table[@class='product-additional-info']/tr/td[@class='attributes-table-main']/table/tr/th")
	for th in ths:
		detailsHeader.append(th.text)

	tds = tree.xpath("//table[@class='product-additional-info']/tr/td[@class='attributes-table-main']/table/tr/td")
	for td in tds:
		detailsData.append(td.text)

	detailRecord = 0
	for r in detailsHeader:
		part[detailsHeader[detailRecord]] = detailsData[detailRecord]
		detailRecord += 1

	print part


while True:
	code = raw_input('Please scan barcode, or press q to quit.\r\nPartGrabber> ')
	if code == 'q': sys.exit()
	elif len(code) > 7: getDetails(code)
