import sys, glob, json # used to iterate over files
import pandas as pd
	
# Allows users to select an analysis or change data sources
def mainMenu():
	menu = {'1': 'Select a different room',
			'2': 'Get User information',
			'3': 'Most Popular Emoji',
			'4': 'Exit'}

	while True:
		options = menu.keys()
		options.sort()
		for entry in options:
			print entry, menu[entry]

		selection = raw_input("Please select: ")

		if selection == '1':
			selectExportFolder()
		elif selection == '2':
			df = selectRoom()
			getUserInfo(df)
		elif selection == '3':
			print 'Most Popular Emoji'
		elif selection == '4':
			break
		else:
			print 'Unknown'

def getUserInfo(df):
	"""print list of most popular emojis associated with each user"""
	name = raw_input("Input username (first.last)")
	for name in sorted(df.name.unique()):
		print name
		print getPopularEmoji(df[df.name == name]).sort_values(by='count', ascending=False)

def getPopularEmoji(df):
	"""print list of most popular emojis associated with each user"""
	d = {}
	reactions = df.reactions.dropna()
	for reaction in reactions:
		emoji = reaction[0]['name']
		if d.has_key(emoji):
			d[emoji] += reaction[0]['count']
		else:
			d[emoji] = reaction[0]['count']

	return pd.DataFrame(d.items(), columns = ['emoji', 'count'])

def selectExportFolder():
	# tests if it's a real exported slack folder
	while True:
		try:
			global folder, channels_json, users_json
			folder 			= raw_input("Slack export folder name: ")
			channels_json 	= open(folder + '/channels.json', 'r').read()
			users_json 		= open(folder + '/users.json', 'r').read()
			break
		except IOError:
			print('Could not find correct files in that folder. Please try again.')

def selectRoom():
	room = raw_input("Slack room name: ")

	df = pd.DataFrame()

	# import message files
	path = folder + "/" + room + '/*.json'
	for filename in glob.glob(path):
		new_df = pd.read_json(filename, orient='records')
		df = df.append(new_df, ignore_index = True)

	users = pd.read_json(users_json)
	user_lookup = users[['id','name']]

	return df

if __name__ == '__main__':
	# global variables: folder, channels_json, users_json

	selectExportFolder()
	mainMenu()
