"""
This script will tabulate the count of actions per browser that access our link shortener. The input file is the log file located at static/log.txt.

To run:
browser_action.py static/log.txt > actions_per_browser.txt

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
		yield cell[0]+"-"+cell[2], 1

	def reducer(self, vroot, occurrences):
		total = sum(occurrences)
		yield vroot, total

if __name__ == '__main__':
    ActionCounter.run()
