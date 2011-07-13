class Job(object):
	tick = u'\u2713'
	cross = u'\u2718'
	dash  = ' - '
	good_colors = ['blue', 'blue_anime']
	disabled_colours = ['grey']
	okay_colors = good_colors + disabled_colours

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
		print repr(self.okay_colors)
		print self.color
		print self.color in self.okay_colors
		return self.color in self.okay_colors

	def is_disabled(self):
		return self.color in self.disabled_colours

	def menu_item(self, action):
		from indicator import MenuItem
		return MenuItem(self.description(), icon=self.icons[self.color], action=action)

	def description(self):
		if(self.is_successful()):
			prefix = self.dash if self.is_disabled() else self.tick
			desc = "%s %s" % (prefix, self.name)
		else:
			return "%s %s (%s)" % (self.cross, self.name, self.color)
		if self.color.endswith("_anime"):
			return desc + " (building)"
		return desc

