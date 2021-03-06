class Job(object):
	tick = u'\u2713'
	cross = u'\u2718'
	dash  = ' -  '
	good_colors = ['blue', 'blue_anime']
	disabled_colours = ['grey', 'disabled']
	okay_colors = good_colors + disabled_colours

	def __init__(self, json_obj, icons):
		self.json = json_obj
		self.icons = icons
		def copy(*keys):
			for key in keys:
				try:
					setattr(self, key, json_obj[key])
				except KeyError: pass
		copy('name', 'color', 'url', 'claimed')
	
	def __repr__(self):
		return "<Job: %r>" % (self.json)

	def is_successful(self):
		return self.color in self.okay_colors

	def is_disabled(self):
		return self.color in self.disabled_colours

	def menu_item(self, action):
		from indicator import MenuItem
		return MenuItem(self.description(), icon=self.icons[self.color], action=action)

	def description(self):
		if(self.is_successful()):
			prefix = self.dash if self.is_disabled() else self.tick
		else:
			prefix = self.cross
		desc = "%s %s" % (prefix, self.name)
		if self.color.endswith("_anime"):
			desc += " (building)"
		try:
			desc += " <claimed by %s: %s>" % (self.claimed['user'], self.claimed['reason'])
		except AttributeError:
			pass

		return desc

