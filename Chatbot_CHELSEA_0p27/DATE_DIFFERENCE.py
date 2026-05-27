from datetime import datetime, timedelta
import random

class date_difference:

	def get_days_past(self, date):

		#Get how many days have passed from now to input date (input as a string)

		# Restore to a datetime object
		original_date = datetime.strptime(date, "%m/%d/%Y, %H:%M:%S")

		current_date = datetime.now()

		return (current_date - original_date).days

	def get_hours_past(self, date):

		#Get how many hours have passed from now to input date (input as a string)

		# Restore to a datetime object
		original_date = datetime.strptime(date, "%m/%d/%Y, %H:%M:%S")

		current_date = datetime.now()

		return (current_date - original_date).total_seconds() / 3600

	def get_minutes_past(self, date):

		#Get how many minutes have passed from now to input date (input as a string)

		# Restore to a datetime object
		original_date = datetime.strptime(date, "%m/%d/%Y, %H:%M:%S")

		current_date = datetime.now()

		return (current_date - original_date).total_seconds() / 60

	def get_time_range(self, input_date):

		#Given how many days have passed from now to input date (input as a string),
		#output a string corresponding to that range of days (Such as 7 days: 'a week ago')

		days = self.get_days_past(input_date)
		date = datetime.strptime(input_date, "%m/%d/%Y, %H:%M:%S")

		if days == 0:
			
			hours = self.get_hours_past(input_date)

			if hours == 0:

				minutes = self.get_minutes_past(input_date)

				if minutes < 2:
					return random.choice(['less than a couple of minutes ago', 'about a minute ago', 'a moment ago'])
				
				elif minutes < 4:
					return random.choice(['a few minutes ago', 'about three minutes ago', 'just a few minutes ago'])
				
				elif minutes < 10:
					return random.choice(['less than ten minutes ago', 'just a bit ago', 'several minutes ago'])
				
				elif minutes < 15:
					return random.choice(['about ten minutes ago', 'a quarter of an hour ago', 'just about fifteen minutes ago'])
				
				elif minutes < 30:
					return random.choice(['a bit under thirty minutes ago', 'almost half an hour ago', 'just near half an hour ago'])
				
				elif minutes < 45:
					return random.choice(['about three quarters of an hour ago', 'just over thirty minutes ago', 'near a half an hour ago'])
				
				elif minutes < 60:
					return random.choice(['about an hour ago', 'just under an hour ago', 'barely an hour ago'])
			
			if hours < 2:
				return random.choice(['less than a couple of hours ago', 'about an hour ago', 'a short while ago'])
			
			elif hours < 4:
				return random.choice(['a few hours ago', 'about three hours ago', 'just a few hours ago'])
			
			elif hours < 10:
				return random.choice(['less than ten hours ago', 'just some hours ago', 'several hours ago'])
			
			elif hours < 12:
				return random.choice(['about twelve hours ago', 'a half of a day ago', 'close to twelve hours ago'])
			
			elif hours < 24:
				return random.choice(['many hours ago', 'almost a day ago', 'just near a day ago'])

		elif days == 1:
			return random.choice(['a day ago', 'one day ago', 'a single day ago', 'yesterday', date.strftime('%A').lower()])

		elif days == 2:
			return random.choice(['a couple of days ago', 'two days ago', f"last {date.strftime('%A').lower()}"])

		elif days == 3:
			return random.choice(['a few days ago', 'three days ago', f"last {date.strftime('%A').lower()}"])

		elif days < 7:
			return random.choice(['several days ago', 'many days ago', 'less than a week ago', f"last {date.strftime('%A').lower()}"])

		elif days == 7:
			return random.choice(['a week ago', 'one week ago', 'a single week ago'])

		elif days < 14:
			return random.choice(['over a week ago', 'about a week ago', 'more than a week ago'])

		elif days == 14:
			return random.choice(['a couple of weeks ago', 'two weeks ago'])

		elif days < 21:
			return random.choice(['over a couple of weeks ago', 'about two weeks ago', 'more than two weeks ago'])

		elif days == 21:
			return random.choice(['a few weeks ago', 'three weeks ago'])

		elif days < 31:
			return random.choice(['about a month ago', 'almost a month ago', 'close to a month ago'])

		elif days < 61:
			return random.choice(['about two months ago', 'almost two months ago', 'close to two months ago'])

		elif days < 91:
			return random.choice(['about a few months ago', 'almost three months ago', 'close to three months ago'])

		elif days < 365:
			return random.choice(['several months ago', 'more than a few months ago'])

		elif days == 365:
			return random.choice(['exactly a year ago', 'one year ago'])

		elif days < 730:
			return random.choice(['more than a year ago', 'over one year ago'])

		else:
			return random.choice(['a long time ago', 'quite a ways back', 'a pretty long time ago', 'ages ago'])

	def get_month(self, month_string):

		#Convert month name or abbreviation into its numerical counterpart

		if month_string in {'january', 'jan', 'jan.'}:
			return '01'
		
		elif month_string in {'february', 'feb', 'feb.'}:
			return '02'
		
		elif month_string in {'march', 'mar', 'mar.'}:
			return '03'
		
		elif month_string in {'april', 'apr', 'apr.'}:
			return '04'
		
		elif month_string in {'may'}:
			return '05'
		
		elif month_string in {'june', 'jun', 'jun.'}:
			return '06'
		
		elif month_string in {'july', 'jul', 'jul.'}:
			return '07'
		
		elif month_string in {'august', 'aug', 'aug.'}:
			return '08'
		
		elif month_string in {'september', 'sep', 'sep.'}:
			return '09'
		
		elif month_string in {'october', 'oct', 'oct.'}:
			return '10'
		
		elif month_string in {'november', 'nov', 'nov.'}:
			return '11'
		
		elif month_string in {'december', 'dec', 'dec.'}:
			return '12'
		
	def string_to_numerical_days(self, input_string):

		#Convert number as string to actual number

		if input_string in {'one', 'a'}:
			return 1
		
		elif input_string == 'two':
			return 2
		
		elif input_string == 'three':
			return 3
		
		elif input_string == 'four':
			return 4
		
		elif input_string == 'five':
			return 5
		
		elif input_string == 'six':
			return 6
		
		elif input_string == 'seven':
			return 7
		
		elif input_string == 'eight':
			return 8
		
		elif input_string == 'nine':
			return 9
		
		elif input_string == 'ten':
			return 10
		
		elif input_string == 'eleven':
			return 11
		
		elif input_string == 'twelve':
			return 12
		
		elif input_string == 'thirteen':
			return 13
		
		elif input_string == 'fourteen':
			return 14
		
		elif input_string == 'fifteen':
			return 15
		
		elif input_string == 'sixteen':
			return 16
		
		elif input_string == 'seventeen':
			return 17
		
		elif input_string == 'eighteen':
			return 18
		
		elif input_string == 'nineteen':
			return 19
		
		elif input_string == 'twenty':
			return 20
		
		else:
			return None

	def get_date_given_time_frame(self, input_days):

		#Either add to or subtract from current date to get new dats

		start_date = datetime.now()

		if input_days > 0:

			return (start_date + timedelta(days = input_days)).strftime("%m/%d/%Y, %H:%M:%S")

		elif input_days < 0:

			return (start_date - timedelta(days = -input_days)).strftime("%m/%d/%Y, %H:%M:%S")
		
		else:

			return datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

	def match_date(self, input_date):

		#Compare the month and day from now to input_date

		if input_date[0:5] == datetime.now().strftime("%m/%d/%Y, %H:%M:%S")[0:5]:
			return True
		
		else:
			return False