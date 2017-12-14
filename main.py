import sys, glob, json # used to iterate over files
import pandas as pd
	
# Allows users to select an analysis or change data sources
def mainMenu():
	menu = {'1': 'Select a different room',
			'2': 'Get User information',
			'3': 'Most Popular Emoji',
			'4': 'Print current room and DataFrame',
			'5': 'Exit'}

	while True:
		options = menu.keys()
		options.sort()
		for entry in options:
			print entry, menu[entry]

		selection = raw_input("Please select: ")

		if selection == '1':
			selectRoom()
			mainMenu()

		elif selection == '2':
			selectRoom()
			getUserInfo(df)

		elif selection == '3':
			print 'Most Popular Emoji'

		elif selection == '4':
			print room, df	

		elif selection == '5':
			sys.exit(0)

		else:
			print 'Unknown'

def setup():
	global folder, room, df, userLookup
	folder 	= 'Viget Slack export Aug 7 2017'
	room 	= 'Crokinole'

	df = pd.DataFrame()

	users_json 	= open(folder + '/users.json', 'r').read()
	userLookup = pd.read_json(users_json, orient = 'records')[['id','name']]

	# import message files
	path = folder + "/" + room + '/*.json'
	for filename in glob.glob(path):
		new_df = pd.read_json(filename, orient='records')
		df = df.append(new_df, ignore_index = True)

	pd.merge(df, userLookup, how='left', left_on='user', right_on='id')

	return df

def getRoomInfo():
	"""print list of unique usernames and count of sent messages"""

	'''
	Between {startDate} and {endDate}, {activeUsers} users sent {totalMessages} messages
	Most active users:
		1. {userName} ({messageCount} messages)
		2. {userName} ({messageCount} messages)
		3. {userName} ({messageCount} messages)
	'''
	# startDate = min timestamp
	# endDate = max timestamp
	# activeUsers = df['user'].unique().count()
	# totalMessage = df['text'].unique().count()

	print df.groupby('user')['text'].count().sort_values(ascending=False)

def getUserLookup():
	"""create a two-column user lookup table (id, name)"""
	global users
	users = pd.read_json(users_json, orient = 'records')[['id','name']]

def getUserInfo():
	"""print user information"""
	name = raw_input("Input username (first.last)")
	for name in sorted(df.name.unique()):
		print name
		print getPopularEmoji(df[df.name == name]).sort_values(by='count', ascending=False)

def compareMFUsage():
	"""use uploaded .csv to compare male / female behavior"""

def getPopularEmoji():
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
	# Check if it's an exported Slack folder
	while True:
		try:
			global folder, userLookup
			folder 			= raw_input("Slack export folder name: ")
			channels_json 	= open(folder + '/channels.json', 'r').read()
			users_json 		= open(folder + '/users.json', 'r').read()
			break
		except IOError:
			print('Could not find correct files in that folder. Please try again.')

	userLookup = pd.read_json(users_json, orient = 'records')[['id','name']]
	selectRoom()

def selectRoom():
	global room, df
	room = raw_input("Slack room name: ")

	df = pd.DataFrame()

	# import message files
	path = folder + "/" + room + '/*.json'
	for filename in glob.glob(path):
		new_df = pd.read_json(filename, orient='records')
		df = df.append(new_df, ignore_index = True)

	print df

if __name__ == '__main__':
	# global variables: folder, channels_json, users_json, df, room
	selectExportFolder()
	mainMenu()
