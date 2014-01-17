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


from bs4 import BeautifulSoup
from lxml import html
from pprint import pprint
import requests
import sys

def getDetail(part):
	print part[:7]

def getHyperlinks(html):
	return [(a.text, a['href']) for a in html.findAll("a")]

def getDetails(barcode):
	quantity = barcode[7:16]
	page = requests.get('http://www.digikey.com/product-detail/en/0/0/' + barcode[:7])
		
	part = dict()		# Holds details related to the part
	pricing = dict()	# Holds pricing for the part

	soup = BeautifulSoup(page.text)  #open("test.html")

	# Parse pricing data from html
	table = soup.find("table",{"id":"pricing"})
	for row in table.findAll("tr"):
		tds = row.findAll(text=True)
		if len(tds) > 1:
			if tds[0] != "Price Break": pricing[tds[0]] = tds[1] #print tds[0], tds[1]

	# Parse product details from html
	part['ProductNumber'] = soup.find("meta",{"name":"WT.pn_sku"})['content']
	part['MfgProductNumber'] = soup.find("meta",{"itemprop":"name"})['content']
	
	# Grab the dynamic details table data
	table = soup.find("table",{"class":"product-additional-info"})
	for row in table.table.findAll("tr"):
		part[row.th(text=True)[0]] = getHyperlinks(row.td) or row.td(text=True)
	
	print '------------------------------------------------'
	print 'Pricing data:'
	pprint(pricing)
	print '------------------------------------------------'
	print 'Part data:'
	pprint(part)
	print '------------------------------------------------'
	print 'Qty in bag: ' , quantity

while True:
	code = raw_input('Please scan barcode, or press q to quit.\r\nPartGrabber> ')
	if code == 'q': sys.exit()
	elif len(code) > 7: getDetails(code)
	else: getDetails("0607274000000010146541") # Used for testing..
