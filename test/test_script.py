# test_script.py
import unittest
from script import calculate_actuator_torque

class TestRobotActuator(unittest.TestCase):

    def test_revolute_heavy_payload_safe_mode(self):
        # Scenario: Revolute joint, heavy load, SAFE_MODE active, full battery
        # Calculation: ((6.0 * 9.81 * 0.25) * 1.5 + 2.5) -> 24.5725
        # Override: 24.5725 * 0.5 -> 12.28625
        # Battery Boost: 12.28625 + 1.1 -> 13.38625 -> Rounded to 13.39
        result = calculate_actuator_torque("Revolute", 6.0, 1.2, "SAFE_MODE", 90)
        self.assertEqual(result, 13.39)

    def test_prismatic_normal_payload_low_battery(self):
        # Scenario: Prismatic joint, normal load, no override, critical battery
        # Calculation: (3.0 * 9.81) + 1.2 -> 30.63
        # Override: None (No change)
        # Battery Throttle: 30.63 * 0.8 -> 24.504 -> Rounded to 24.50
        result = calculate_actuator_torque("Prismatic", 3.0, 0.5, "NONE", 15)
        self.assertEqual(result, 24.50)

if __name__ == "__main__":
    unittest.main()
    