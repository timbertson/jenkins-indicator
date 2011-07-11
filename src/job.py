class Job(object):
	tick = u'\u2713'
	cross = u'\u2718'

	def __init__(self, json_obj, icons):
		self.json = json_obj
		self.icons = icons
		def copy(*keys):
			for key in keys:
				setattr(self, key, json_obj[key])
		copy('name', 'color', 'url')
	
	def __repr__(self):
		return "<Job: %r>" % (self.json)

	def is_successful(self):
		return self.color.startswith('blue')

	def menu_item(self, action):
		from indicator import MenuItem
		return MenuItem(self.description(), icon=self.icons[self.color], action=action)

	def description(self):
		if(self.is_successful()):
			return "%s %s" % (self.tick, self.name)
		else:
			return "%s %s (%s)" % (self.cross, self.name, self.color)

