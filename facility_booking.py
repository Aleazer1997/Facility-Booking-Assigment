from datetime import datetime, time

class FacilityBookingSystem:
    def __init__(self):
        # Store bookings: {facility_name: [(date, start, end)]}
        self.bookings = {}

        # Facility configuration with time objects
        self.facilities = {
            "Clubhouse": [
                {"start": time(10, 0), "end": time(16, 0), "rate": 100},
                {"start": time(16, 0), "end": time(22, 0), "rate": 500},
            ],
            "Tennis Court": [
                {"start": time(0, 0), "end": time(23, 59, 59), "rate": 50},
            ]
        }

    def _parse_time(self, time_str):
        """Parse time string to time object with validation"""
        try:
            return datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            raise ValueError(f"Invalid time format: {time_str}. Use HH:MM format.")

    def _time_to_minutes(self, time_obj):
        """Convert time object to total minutes for easier calculations"""
        return time_obj.hour * 60 + time_obj.minute

    def calculate_cost(self, facility, start_time, end_time):
        cost = 0
        start_min = self._time_to_minutes(start_time)
        end_min = self._time_to_minutes(end_time)

        for slot in self.facilities[facility]:
            slot_start_min = self._time_to_minutes(slot["start"])
            slot_end_min = self._time_to_minutes(slot["end"])
            
            # Calculate overlap
            overlap_start = max(start_min, slot_start_min)
            overlap_end = min(end_min, slot_end_min)
            
            if overlap_start < overlap_end:
                hours = (overlap_end - overlap_start) / 60
                cost += hours * slot["rate"]
        
        return int(cost)  # Return integer cost

    def is_available(self, facility, date, start_time, end_time):
        if facility not in self.bookings:
            return True
            
        start_min = self._time_to_minutes(start_time)
        end_min = self._time_to_minutes(end_time)

        for (b_date, b_start, b_end) in self.bookings[facility]:
            if b_date == date:
                b_start_min = self._time_to_minutes(b_start)
                b_end_min = self._time_to_minutes(b_end)
                
                # Check for time overlap
                if not (end_min <= b_start_min or start_min >= b_end_min):
                    return False
        return True

    def book_facility(self, facility, date, start_time_str, end_time_str):
        # Validate inputs
        try:
            start_time = self._parse_time(start_time_str)
            end_time = self._parse_time(end_time_str)
        except ValueError as e:
            return str(e)
            
        # Validate time order
        if start_time >= end_time:
            return "Booking Failed: End time must be after start time"
            
        # Check availability
        if not self.is_available(facility, date, start_time, end_time):
            return "Booking Failed, Already Booked"
            
        # Calculate cost and book
        cost = self.calculate_cost(facility, start_time, end_time)
        self.bookings.setdefault(facility, []).append((date, start_time, end_time))
        return f"Booked, Rs. {cost}"


# Main execution
if __name__ == "__main__":
    system = FacilityBookingSystem()
    
    # Example usage from the assignment
    print(system.book_facility("Clubhouse", "26-10-2020", "16:00", "22:00"))
    print(system.book_facility("Tennis Court", "26-10-2020", "16:00", "20:00"))
    print(system.book_facility("Clubhouse", "26-10-2020", "16:00", "22:00"))
    print(system.book_facility("Tennis Court", "26-10-2020", "17:00", "21:00"))