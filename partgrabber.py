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
