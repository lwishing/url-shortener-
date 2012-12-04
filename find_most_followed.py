"""
This script will find the most followed urls from our link shortener. The input file is the log file located at static/log.txt.

To run:
find_most_followed.py static/log.txt > most_followed_urls.txt

To sort:
Open most_followed_urls.txt in Excel, sort by second column, which is the count of redirects.

"""

from mrjob.job import MRJob
import fileinput
import flask
import csv
app = flask.Flask(__name__)
app.debug = True

def csv_readline(line):
    """Given a string CSV line, return a list of strings."""
    for row in csv.reader([line]):
        return row

class ActionCounter(MRJob):
	#data = open('static/log.txt')
	#app.logger.debug(data)
	def mapper(self, line_no, line):        
		cell = csv_readline(line)
		#app.logger.debug(cell[2])
		yield cell[4], 1

	def reducer(self, vroot, occurrences):		
		total = sum(occurrences)
		if vroot != '':
			yield vroot, total		

if __name__ == '__main__':
    ActionCounter.run()
