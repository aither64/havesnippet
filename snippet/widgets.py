from django import forms
from django.forms import widgets

UNITS = (
	(60, "minutes"),
	(60*60, "hours"),
	(60*60*24, "days"),
	(60*60*24*7, "weeks"),
	(60*60*24*30, "months")
)


class TimeIntervalWidget(widgets.MultiWidget):
	def __init__(self, attrs=None, *args, **kwargs):
		super(TimeIntervalWidget, self).__init__(widgets=(
			forms.TextInput(attrs=attrs),
		    forms.Select(attrs=attrs, choices=UNITS)
		), attrs=attrs, *args, **kwargs)

	def decompress(self, value):
		if value is None:
			return [30, None]

		n = int(value)
		u = UNITS[0][0]

		for unit in reversed(UNITS):
			if n >= unit:
				u = unit
				break

		return [round(float(n) / u), u]

