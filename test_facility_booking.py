import unittest
from facility_booking import FacilityBookingSystem

class TestFacilityBookingSystem(unittest.TestCase):
    def setUp(self):
        self.system = FacilityBookingSystem()
    
    def test_clubhouse_booking(self):
        result = self.system.book_facility("Clubhouse", "26-10-2020", "16:00", "22:00")
        self.assertEqual(result, "Booked, Rs. 3000")  # 6 hours × 500 = 3000
    
    def test_tennis_court_booking(self):
        result = self.system.book_facility("Tennis Court", "26-10-2020", "16:00", "20:00")
        self.assertEqual(result, "Booked, Rs. 200")  # 4 hours × 50 = 200
    
    def test_double_booking(self):
        # First booking should succeed
        result1 = self.system.book_facility("Clubhouse", "26-10-2020", "16:00", "22:00")
        self.assertEqual(result1, "Booked, Rs. 3000")
        
        # Second booking should fail
        result2 = self.system.book_facility("Clubhouse", "26-10-2020", "16:00", "22:00")
        self.assertEqual(result2, "Booking Failed, Already Booked")
    
    def test_partial_overlap(self):
        # Book first slot
        result1 = self.system.book_facility("Tennis Court", "26-10-2020", "16:00", "20:00")
        self.assertEqual(result1, "Booked, Rs. 200")
        
        # Try to book overlapping slot
        result2 = self.system.book_facility("Tennis Court", "26-10-2020", "17:00", "21:00")
        self.assertEqual(result2, "Booking Failed, Already Booked")
    
    def test_invalid_time_format(self):
        result = self.system.book_facility("Clubhouse", "26-10-2020", "16:00", "invalid")
        self.assertIn("Invalid time format", result)
    
    def test_end_time_before_start_time(self):
        result = self.system.book_facility("Clubhouse", "26-10-2020", "18:00", "16:00")
        self.assertIn("End time must be after start time", result)

if __name__ == "__main__":
    unittest.main(verbosity=2)