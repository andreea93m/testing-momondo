import unittest
import time
import datetime
from datetime import date
from selenium import webdriver

class DatePicker(object):

	def __init__(self, datepicker):
		super(DatePicker, self).__init__()
		self.datepicker = datepicker
		
	def getDate(self):
		""" Returns the currently selected date from the calendar (the highlighted one).
		"""
		current = self.datepicker.find_element_by_class_name("ui-datepicker-current-day")

		day = int(current.find_element_by_xpath(".//*").get_attribute('innerHTML'))
		month = int(current.get_attribute('data-month'))+1
		year = int(current.get_attribute('data-year'))

		current_date = date(year, month, day)
		current_date = datetime.datetime.strptime(str(current_date), '%Y-%m-%d').strftime('%m/%d/%Y')
		current_date = datetime.datetime.strptime(current_date, '%m/%d/%Y').date()

		return current_date

	def getCalendarMonth(self):
		return int(self.datepicker.find_element_by_xpath('//td[@class=" "]').get_attribute('data-month')) + 1

	def goNextMonth(self):
		self.datepicker.find_element_by_xpath('//a[@title="Next"]').click()

	def goPrevMonth(self):
		self.datepicker.find_element_by_xpath('//a[@title="Prev"]').click()

	def selectInvalidDay(self, day):
		self.datepicker.find_element_by_xpath('//span[@class="ui-state-default"][text()="%s"]' % day).click()

	def selectDay(self, day):
		self.datepicker.find_element_by_xpath('//a[text()="%s"]' % day).click()

	def close(self):
		self.datepicker.find_element_by_xpath('//button[text()="close"]').click()


class DatePickerTest(unittest.TestCase):

	def setUp(self):
		""" Before every test, the driver is initialized, we navigate to the website,
			we get the datepicker, which we use to access elements from the calendar,
			and we also get the input for the return date, on which we click to open the calendar.
		"""
		self.driver = webdriver.Chrome()
		self.driver.get("http://www.momondo.co.uk/")
		self.return_datepicker = DatePicker(self.driver.find_element_by_id('ui-datepicker-div'))
		self.return_input = self.driver.find_element_by_css_selector('div.input._date-return')

	def test_select_past_date(self):
		""" Checks that a date from the past cannot be selected as return date.

			Steps:
				1. Open calendar for return date
				2. Store current date
				3. Click previous month button
				4. Select the first invalid date - exactly 1 day before today
				5. Close the calendar
				6. Reopen it to get the selected date
				7. Check that it is the same as the initial one

		"""
		self.return_input.click()
		calendar_date = self.return_datepicker.getDate()
		time.sleep(1)
		self.return_datepicker.goPrevMonth()
		self.return_datepicker.selectInvalidDay((date.today() - datetime.timedelta(1)).day)
		self.return_datepicker.close()
		self.return_input.click()
		self.assertEqual(self.return_datepicker.getDate(), calendar_date)

	def test_go_past_month(self):
		""" Checks that it is not possible to navigate through the calendar to a month from the past.

			Steps:
				1. Open calendar for return date
				2. Click previous month button
				3. Store current month
				4. Click previous month button
				5. Check that we still display the same month as before

		"""
		self.return_input.click()
		time.sleep(1)
		self.return_datepicker.goPrevMonth()
		calendar_month = self.return_datepicker.getCalendarMonth()
		self.return_datepicker.goPrevMonth()
		self.assertEqual(calendar_month, self.return_datepicker.getCalendarMonth())

	def test_iterate_months(self):
		""" Checks that we can correctly iterate through the calendar of the return date picker.

			Steps:
				1. Open calendar for return date
				2. Store current month
				3. Click previous month button
				4. Check that we actually navigated to the previous month
				5. Click next month button
				6. Check that we actually navigated to the next month
				
		"""
		self.return_input.click()
		time.sleep(1)
		calendar_month = self.return_datepicker.getCalendarMonth()
		self.return_datepicker.goPrevMonth()
		self.assertEqual(calendar_month - 1, self.return_datepicker.getCalendarMonth())
		self.return_datepicker.goNextMonth()
		self.assertEqual(calendar_month, self.return_datepicker.getCalendarMonth())

	def test_select_future_date(self):
		""" Checks that we cannot select a date too far in the future (later than 1 year from now) as a return date.

			Steps:
				1. Open calendar for return date
				2. Store current date
				3. Iterate through months by pressing next month button until 1 year from now
				4. Select a date that is 1 year and 1 day from now
				5. Close the calendar
				6. Reopen it
				7. Check that the selected date hasn't changed
				
		"""

		self.return_input.click()
		calendar_date = self.return_datepicker.getDate()

		for i in range(0, 11):
			self.return_datepicker.goNextMonth()
			time.sleep(1)

		self.return_datepicker.selectInvalidDay((date.today() + datetime.timedelta(366)).day)
		self.return_datepicker.close()
		self.return_input.click()
		self.assertEqual(self.return_datepicker.getDate(), calendar_date)

	def test_go_future_month(self):
		""" Checks that it is not possible to navigate through the calendar to a month from the too far future.

			Steps:
				1. Open calendar for return date
				2. Iterate through months by pressing next month button until 1 year from now
				3. Store current month
				4. Press next month button
				5. Check that the displayed month is the same as previously
				
		"""
		self.return_input.click()
		time.sleep(1)

		for i in range(0, 11):
			self.return_datepicker.goNextMonth()
			time.sleep(1)

		calendar_month = self.return_datepicker.getCalendarMonth()
		self.return_datepicker.goNextMonth()
		self.assertEqual(calendar_month, self.return_datepicker.getCalendarMonth())

	def test_displayed_date_same_selected_date(self):
		""" Checks that the return date that I select and the date that is displayed (both in calendar and input field) are the same.
			
			Steps:
				1. Open calendar for return date
				2. Select the day 15 from the default month
				3. Store the displayed return date in the Python date format
				4. Store the current date
				5. Check that the displayed return date is the same as the one from the calendar and the day is 15
				
		"""
		self.return_input.click()
		time.sleep(2)

		self.return_datepicker.selectDay(15)
		time.sleep(3)

		displayed_date = self.return_input.find_element_by_name("ctl00$Content$ctl04$SearchFormv8$SearchFormFlight$InputReturn").get_attribute('value')
		displayed_date = datetime.datetime.strptime(displayed_date, '%m/%d/%Y').date()

		self.return_input.click()
		calendar_date = self.return_datepicker.getDate()

		self.assertEqual(calendar_date, displayed_date)
		self.assertEqual(calendar_date.day, 15)

	def test_return_after_departure(self):
		""" Checks that return date is always after the departure date.
			
			Steps:
				1. Open calendar for departure date
				2. Store the datepicker element
				3. Store the displayed return date in the Python date format
				4. Select the new departure date as a day from the current return date
				5. Store the displayed return date in the Python date format
				6. Check that return date was automatically updated
				7. Reopen calendar for departure date
				8. Select the new departure date as a day before the current return date
				9. Store the displayed return date in the Python date format
				10. Check that return date was not automatically updated, since the
				 condition to have return date after departure date is already satisfied
				
		"""
		self.depart_input = self.driver.find_element_by_css_selector('div.input._date-depart')
		self.depart_input.click()
		time.sleep(1)
		self.depart_datepicker = DatePicker(self.driver.find_element_by_id('ui-datepicker-div'))

		displayed_return_date = self.return_input.find_element_by_name("ctl00$Content$ctl04$SearchFormv8$SearchFormFlight$InputReturn").get_attribute('value')
		displayed_return_date = datetime.datetime.strptime(displayed_return_date, '%m/%d/%Y').date()
		
		self.depart_datepicker.selectDay(displayed_return_date.day + 1)

		current_displayed_return_date = self.return_input.find_element_by_name("ctl00$Content$ctl04$SearchFormv8$SearchFormFlight$InputReturn").get_attribute('value')
		current_displayed_return_date = datetime.datetime.strptime(current_displayed_return_date, '%m/%d/%Y').date()
		time.sleep(3)

		self.assertEqual(current_displayed_return_date, displayed_return_date + datetime.timedelta(1))

		self.depart_input.click()
		self.depart_datepicker.selectDay(current_displayed_return_date.day - 1)

		displayed_return_date = self.return_input.find_element_by_name("ctl00$Content$ctl04$SearchFormv8$SearchFormFlight$InputReturn").get_attribute('value')
		displayed_return_date = datetime.datetime.strptime(displayed_return_date, '%m/%d/%Y').date()

		self.assertEqual(current_displayed_return_date, displayed_return_date)
		time.sleep(2)

	def test_default_return_departure(self):
		""" Checks that default dates are from the next month and the return date is after the departure date.
			
			Steps:
				1. Departure date input
				2. Store the displayed return date in the Python date format
				3. Store the displayed departure date in the Python date format
				4. Check that the departure date and return date are from the same month (next month from now)
				5. Check that return date is after departure date
				
		"""
		self.depart_input = self.driver.find_element_by_css_selector('div.input._date-depart')

		displayed_return_date = self.return_input.find_element_by_name("ctl00$Content$ctl04$SearchFormv8$SearchFormFlight$InputReturn").get_attribute('value')
		displayed_return_date = datetime.datetime.strptime(displayed_return_date, '%m/%d/%Y').date()

		displayed_depart_date = self.depart_input.find_element_by_name("ctl00$Content$ctl04$SearchFormv8$SearchFormFlight$InputDepart").get_attribute('value')
		displayed_depart_date = datetime.datetime.strptime(displayed_depart_date, '%m/%d/%Y').date()

		self.assertEqual(displayed_return_date.month, displayed_depart_date.month)
		self.assertEqual(displayed_return_date.month, date.today().month + 1)

		assert displayed_return_date.day > displayed_depart_date.day

	def tearDown(self):
		""" After every test, the driver is closed."""

		self.driver.close()
		self.driver.quit()

if __name__ == "__main__":
	unittest.main()
