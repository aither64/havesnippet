from django import forms
from django.forms import MultiValueField
from snippet.widgets import TimeIntervalWidget, UNITS


class TimeIntervalField(MultiValueField):
	def __init__(self, *args, **kwargs):
		if 'widget' not in kwargs:
			kwargs['widget'] = TimeIntervalWidget

		super(TimeIntervalField, self).__init__(fields=(
			forms.IntegerField(min_value=0, *args),
			forms.ChoiceField(choices=UNITS, *args)
		), *args, **kwargs)

	def compress(self, data_list):
		if data_list:
			if None in data_list:
				return None

			return int(data_list[0]) * int(data_list[1])

		return 60*30
