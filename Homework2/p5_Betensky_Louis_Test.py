import datetime
import os
import tempfile
import unittest
import importlib.util


MODULE_PATH = os.path.join(
    os.path.dirname(__file__),
    "p5_Betensky_Louis.py",
)

spec = importlib.util.spec_from_file_location("weather_station_module", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
read_observations = module.read_observations
station_statistics = module.station_statistics
write_statistics = module.write_statistics


class TestWeatherStationData(unittest.TestCase):
    def test_read_observations_multiple_stations_sorted(self):
        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8", newline="") as file:
            file.write("B,08:00:00 AM 01/02/2024,12.0\n")
            file.write("A,09:30:00 PM 01/03/2024,7.5\n")
            file.write("A,07:45:00 AM 01/01/2024,5.0\n")
            file.write("C,11:15:00 PM 01/10/2024,-3.0\n")
            temp_path = file.name

        try:
            observations, errors = read_observations(temp_path)

            self.assertEqual(errors, [])
            self.assertEqual(observations["A"], [(datetime.datetime(2024, 1, 1, 7, 45), 5.0), (datetime.datetime(2024, 1, 3, 21, 30), 7.5)])
            self.assertEqual(observations["B"], [(datetime.datetime(2024, 1, 2, 8, 0), 12.0)])
            self.assertEqual(observations["C"], [(datetime.datetime(2024, 1, 10, 23, 15), -3.0)])
        finally:
            os.unlink(temp_path)

    def test_negative_temperatures_are_valid(self):
        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8", newline="") as file:
            file.write("North,12:00:00 AM 01/01/2024,-100.0\n")
            file.write("South,02:30:00 PM 05/01/2024,-1.5\n")
            temp_path = file.name

        try:
            observations, errors = read_observations(temp_path)

            self.assertEqual(errors, [])
            self.assertIn("North", observations)
            self.assertIn("South", observations)
            self.assertEqual(observations["North"], [(datetime.datetime(2024, 1, 1, 0, 0), -100.0)])
            self.assertEqual(observations["South"], [(datetime.datetime(2024, 5, 1, 14, 30), -1.5)])
        finally:
            os.unlink(temp_path)

    def test_duplicate_observations_are_recorded_as_errors(self):
        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8", newline="") as file:
            file.write("A,10:00:00 AM 01/01/2024,10.0\n")
            file.write("A,10:00:00 AM 01/01/2024,11.0\n")
            temp_path = file.name

        try:
            observations, errors = read_observations(temp_path)

            self.assertEqual(observations["A"], [(datetime.datetime(2024, 1, 1, 10, 0), 10.0)])
            self.assertEqual(len(errors), 1)
            self.assertIn("Duplicate data combo", errors[0][1])
        finally:
            os.unlink(temp_path)

    def test_invalid_temperature_range_is_rejected(self):
        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8", newline="") as file:
            file.write("A,10:00:00 AM 01/01/2024,-100.1\n")
            file.write("B,10:00:00 AM 01/01/2024,150.1\n")
            temp_path = file.name

        try:
            observations, errors = read_observations(temp_path)

            self.assertEqual(observations, {})
            self.assertEqual(len(errors), 2)
            self.assertTrue(all("Bad temperature" in message for _, message in errors))
        finally:
            os.unlink(temp_path)

    def test_station_statistics_are_calculated_correctly(self):
        observations = {
            "A": [(datetime.datetime(2024, 1, 1, 10, 0), 10.0), (datetime.datetime(2024, 1, 2, 10, 0), 20.0), (datetime.datetime(2024, 1, 3, 10, 0), 30.0)],
            "B": [(datetime.datetime(2024, 1, 1, 10, 0), -5.0), (datetime.datetime(2024, 1, 2, 10, 0), 5.0)],
        }

        stats = station_statistics(observations)

        self.assertAlmostEqual(stats["A"]["min"], 10.0)
        self.assertAlmostEqual(stats["A"]["max"], 30.0)
        self.assertAlmostEqual(stats["A"]["mean"], 20.0)
        self.assertAlmostEqual(stats["B"]["min"], -5.0)
        self.assertAlmostEqual(stats["B"]["max"], 5.0)
        self.assertAlmostEqual(stats["B"]["mean"], 0.0)

    def test_write_statistics_sorts_stations_and_formats_values(self):
        stats = {
            "B": {"min": -5.0, "max": 5.0, "mean": 0.0},
            "A": {"min": 10.0, "max": 30.0, "mean": 20.0},
        }

        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8", newline="") as file:
            temp_path = file.name

        try:
            write_statistics(temp_path, stats)

            with open(temp_path, "r", encoding="utf-8") as file:
                content = file.read().strip().splitlines()

            self.assertEqual(content, ["A,10.0,30.0,20.0", "B,-5.0,5.0,0.0"])
        finally:
            os.unlink(temp_path)

    def test_missing_file_returns_error(self):
        missing_path = os.path.join(tempfile.gettempdir(), "definitely_missing_weather_file.csv")

        if os.path.exists(missing_path):
            os.remove(missing_path)

        observations, errors = read_observations(missing_path)

        self.assertEqual(observations, {})
        self.assertEqual(len(errors), 1)
        self.assertIn("File not found", errors[0][1])


if __name__ == "__main__":
    unittest.main()
