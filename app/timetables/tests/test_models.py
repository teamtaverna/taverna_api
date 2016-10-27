from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

from app.timetables.factories import (
    CourseFactory, DishFactory, EventFactory, MealFactory, MenuItemFactory,
    TimetableFactory, VendorFactory, WeekdayFactory
)

from app.timetables.models import (
    Event, Weekday, Meal, Course, Timetable, Dish, MenuItem, Vendor
)


class WeekdayTest(TestCase):
    """Tests the Weekday model."""

    def setUp(self):
        WeekdayFactory()

    def test_duplicate_weekday_name_cannot_be_saved(self):
        day = Weekday(name='Monday')

        self.assertRaises(ValidationError, day.save)


class MealTest(TestCase):
    """Tests the Meal model."""

    def setUp(self):
        self.meal = MealFactory()

    def test_duplicate_meal_name_cannot_be_saved(self):
        meal = Meal(
            name='breakfast',
            start_time=self.meal.start_time,
            end_time=self.meal.end_time
        )

        self.assertRaises(ValidationError, meal.save)

    def test_meal_end_time_less_than_start_time_cannot_be_saved(self):
        meal = Meal(
            name='lunch',
            start_time=self.meal.end_time,
            end_time=self.meal.start_time
        )

        self.assertRaises(ValidationError, meal.save)

    def test_meal_end_time_same_with_start_time_cannot_be_saved(self):
        meal = Meal(
            name='lunch',
            start_time=self.meal.start_time,
            end_time=self.meal.start_time
        )

        self.assertRaises(ValidationError, meal.save)


class CourseTest(TestCase):
    """Tests the Course model."""

    def setUp(self):
        CourseFactory()

    def test_duplicate_course_name_cannot_be_saved(self):
        course = Course(
            name='appetizer',
            sequence_order=2
        )

        self.assertRaises(ValidationError, course.save)


class TimetableTest(TestCase):
    """Tests the Timetable model."""

    def setUp(self):
        self.timetable = TimetableFactory()
        self.another_timetable = Timetable(
            name='timetable',
            code='FT7871',
            api_key='TF78993jTA',
            cycle_length=self.timetable.cycle_length,
            current_cycle_day=self.timetable.current_cycle_day,
            cycle_day_updated=self.timetable.cycle_day_updated,
            description=self.timetable.description
        )

    def test_duplicate_timetable_name_cannot_be_saved(self):
        self.another_timetable.name = 'fellows timetable'

        self.assertRaises(ValidationError, self.another_timetable.save)

    def test_duplicate_timetable_code_cannot_be_saved(self):
        self.another_timetable.code = self.timetable.code

        self.assertRaises(ValidationError, self.another_timetable.save)

    def test_duplicate_api_key_cannot_be_saved(self):
        self.another_timetable.api_key = self.timetable.api_key

        self.assertRaises(ValidationError, self.another_timetable.save)

    def test_current_cycle_day_greater_than_cycle_length_cannot_be_saved(self):
        self.another_timetable.current_cycle_day = self.timetable.cycle_length + 1

        self.assertRaises(ValidationError, self.another_timetable.save)

    def test_cycle_length_and_current_cycle_day_of_zero_cant_be_saved(self):
        # test for cycle_length == 0
        self.another_timetable.cycle_length = 0
        self.assertRaises(ValidationError, self.another_timetable.save)

        # test for current_cycle_day == 0
        self.another_timetable.current_cycle_day = self.another_timetable.cycle_length
        self.another_timetable.cycle_length = self.timetable.cycle_length

        self.assertRaises(ValidationError, self.another_timetable.save)

    def test_cycle_length_and_current_cycle_day_of_negative_value_cant_be_saved(self):
        # test for cycle_length < 0
        self.another_timetable.cycle_length = -3
        self.assertRaises(ValidationError, self.another_timetable.save)

        # test for current_cycle_day < 0
        self.another_timetable.current_cycle_day = self.another_timetable.cycle_length
        self.another_timetable.cycle_length = self.timetable.cycle_length

        self.assertRaises(ValidationError, self.another_timetable.save)


class DishTest(TestCase):
    """Tests the Dish model."""

    def setUp(self):
        self.dish = DishFactory()

    def test_duplicate_dish_name_cannot_be_saved(self):
        dish = Dish(
            name='Coconut Rice',
            description=self.dish.description
        )

        self.assertRaises(ValidationError, dish.save)


class MenuItemTest(TestCase):
    """Tests the MenuItem model."""

    def setUp(self):
        self.menu_item = MenuItemFactory()
        self.another_menu_item = MenuItem(
            timetable=self.menu_item.timetable,
            cycle_day=self.menu_item.cycle_day,
            meal=self.menu_item.meal,
            course=self.menu_item.course,
            dish=self.menu_item.dish
        )

    def test_duplicates_of_all_cannot_be_saved(self):
        self.assertRaises(ValidationError, self.another_menu_item.save)

    def test_zero_cycle_day_value_cannot_be_saved(self):
        self.another_menu_item.cycle_day = 0

        self.assertRaises(ValidationError, self.another_menu_item.save)


class EventTest(TestCase):
    """Tests the Event model."""

    def setUp(self):
        self.event = EventFactory()
        self.another_event = Event(
            name=self.event.name,
            timetable=self.event.timetable,
            action=self.event.action,
            start_date=self.event.start_date,
            end_date=self.event.end_date
        )

    def test_event_uniqueness(self):
        self.assertRaises(IntegrityError, self.another_event.save)

    def test_event_end_time_less_than_start_time_cannot_be_saved(self):
        self.another_event.start_date = self.event.end_date
        self.another_event.end_date = self.event.start_date

        self.assertRaises(ValidationError, self.another_event.save)

    def test_event_end_time_same_with_start_time_cannot_be_saved(self):
        self.another_event.end_date = self.event.start_date

        self.assertRaises(ValidationError, self.another_event.save)


class VendorTest(TestCase):
    """Test the Vendor model."""

    def setUp(self):
        self.vendor = VendorFactory()
        self.another_vendor = Vendor(
            name='mama Taverna',
            start_date=self.vendor.start_date,
            end_date=self.vendor.end_date
        )

    def test_enforcement_of_uniqueness_of_vendor_name(self):
        self.assertRaises(ValidationError, self.another_vendor.save)

    def test_enforcement_of_vendor_start_date_being_less_than_its_end_date(self):
        # test for start_date == end_date
        self.another_vendor.end_date = self.vendor.start_date
        self.assertRaises(ValidationError, self.another_vendor.save)

        # test for start_date >= end_date
        self.another_vendor.start_date = self.vendor.end_date
        self.assertRaises(ValidationError, self.another_vendor.save)
