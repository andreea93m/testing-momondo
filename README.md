# testing-momondo

- `$ git clone https://github.com/andreea93m/testing-momondo.git`
- `$ cd testing-momondo`
- `$ pip install selenium`
- `$ python selenium-test.py`

I have chosen to test the Momondo website in Python because there is good documentation for using Python with Selenium and it is easier and faster to write than other languages. The tests focus on selecting the return date when searching for a flight. I have used the unittest Python module.

My source file contains a class DatePickerTest with all the tests and DatePicker, which is used for manipulating the datepicker in an easier and more abstracted way. I aim to test the following conditions regarding the return date:
- it cannot be later than 1 year from now
- it cannot be from the past
- it must be after the departure date
- it should be displayed correctly in all views
- one can iterate through months inside the calendar

Some of these can also be applied to test the departure date. The main action is finding elements either by css selector, id, class name or xpath and clicking on them. All the tests currently pass on my machine. However, the implementation could be improved by being more careful when adding one year to a date, since I do not handle leap years. I should also handle the waiting in a better way, since now it is only added because otherwise commands seem to be executed too fast and, because of that, errors occur, like not finding elements. Depending on the computer, these waiting times might solve the issue or might not. Also, the code is a little confusing when I handle months, since, in some cases, they are numbered from 0 to 11, but in other cases from 1 to 12, depending on how they are obtained.
