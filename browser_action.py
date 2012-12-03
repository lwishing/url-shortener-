from mrjob.job import MRJob
import json
import fileinput
import flask
app = flask.Flask(__name__)
app.debug = True

class ActionCounter(MRJob):
	data = json.load(open('static/log.txt'))
	app.logger.debug(data)
	#def mapper(self, key, line):	
		#yield data['action'], data['user-agent'], 1

	#def reducer(self, action, user_agent, occurrences):
		#yield action, sum(occurrences)
		#yield user_agent, sum(occurrences)

	#def steps(self):
		#return [self.mr(self.get_actions, self.sum_actions),]

if __name__ == '__main__':
    ActionCounter.run()
