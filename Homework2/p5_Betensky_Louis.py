import datetime
import sys


def read_observations(filename):
    """
    Reads the file named by filename and returns:
    (observations, errors)

    observations: dict[str, list[(datetime.datetime, float)]]
        Maps each station to a list of (datetime, temperature) tuples sorted by date.

    errors: list[(int, str)]
        Each tuple contains (line_number, error_message).
        If there are no errors, this list is empty.
    """
    observations = {}
    errors = []
    seen_records = set()

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line_number, raw_line in enumerate(file, start=1):
                text = raw_line.strip()

                if not text:
                    continue

                pieces = [part.strip() for part in text.split(",")]

                if len(pieces) != 3:
                    errors.append((line_number, "Badly formed line: expected station, date, temperature."))
                    continue

                station, date_text, temp_text = pieces

                if not station:
                    errors.append((line_number, "Badly formed line: station cannot be empty."))
                    continue

                if not date_text:
                    errors.append((line_number, "Badly formed line: date cannot be empty."))
                    continue

                try:
                    parsed_date = datetime.datetime.strptime(date_text, "%I:%M:%S %p %m/%d/%Y")
                except ValueError:
                    errors.append((line_number, f"Badly formed line: '{date_text}' is not a valid timestamp in H:MM:SS AM/PM MM/DD/YYYY format."))
                    continue

                if not temp_text:
                    errors.append((line_number, "Badly formed line: temperature cannot be empty."))
                    continue

                try:
                    temperature = float(temp_text)
                except ValueError:
                    errors.append((line_number, f"Bad temperature: '{temp_text}' is not a valid number."))
                    continue

                if not (-100.0 <= temperature <= 150.0):
                    errors.append((line_number, f"Bad temperature: {temperature} is outside the valid range [-100.0, 150.0]."))
                    continue

                record_key = (station, parsed_date)

                if record_key in seen_records:
                    errors.append((line_number, f"Duplicate data combo: station '{station}' already has an observation for {date_text}."))
                    continue

                seen_records.add(record_key)
                observations.setdefault(station, []).append((parsed_date, temperature))

    except FileNotFoundError:
        return {}, [(0, f"File not found: {filename}")]

    for station in observations:
        observations[station].sort(key=lambda item: item[0])

    return observations, errors


def station_statistics(observations):
    """
    Given a dictionary of observations in the form:
    station -> [(date, temperature), ...]

    returns a dictionary of the form:
    station -> {"min": min_temp, "max": max_temp, "mean": mean_temp}
    """
    stats = {}

    for station, records in observations.items():
        temperatures = [temp for _, temp in records]

        if not temperatures:
            stats[station] = {"min": None, "max": None, "mean": None}
            continue

        stats[station] = {
            "min": min(temperatures),
            "max": max(temperatures),
            "mean": sum(temperatures) / len(temperatures)
        }

    return stats


def station_outliers(observations):
    """
    Returns a dictionary mapping each station that has a latest temperature
    greater than its mean temperature to:
    (date, temp, mean)
    """
    stats = station_statistics(observations)

    return {
        station: (records[-1][0], records[-1][1], stats[station]["mean"])
        for station, records in observations.items()
        if records and records[-1][1] > stats[station]["mean"]
    }


def write_statistics(filename, statistics):
    """
    Writes statistics to a file in lexicographic order by station name.
    Numeric values are formatted with exactly one digit after the decimal.
    """
    with open(filename, "w", encoding="utf-8") as file:
        for station in sorted(statistics):
            stats = statistics[station]
            file.write(
                f"{station},{stats['min']:.1f},{stats['max']:.1f},{stats['mean']:.1f}\n"
            )


def main():
    print("Weather Station Analysis")
    print("=======================")
    print("This program reads a weather observation file and writes station statistics.")
    print("Expected input file format: station,time AM/PM MM/DD/YYYY,temperature")
    print("Example line: A,10:30:00 AM 01/15/2024,12.5")
    print("Valid temperatures must be between -100.0 and 150.0 inclusive.")

    if len(sys.argv) != 3:
        print("")
        print("Usage: python p5_Betensky_Louis.py <input_file> <output_file>")
        print("Example: python p5_Betensky_Louis.py observations.csv stats.csv")
        return 1

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    print("")
    print(f"Reading observations from: {input_file}")
    print(f"Writing statistics to: {output_file}")

    try:
        observations, errors = read_observations(input_file)

        if errors:
            print("Errors:")
            for line_number, message in errors:
                print(f"Line {line_number}: {message}")

            if any(line_number == 0 for line_number, _ in errors):
                return 1
        else:
            print("No errors found.")

        stats = station_statistics(observations)
        outliers = station_outliers(observations)

        print("\nStation statistics:")
        for station in sorted(stats):
            s = stats[station]
            print(f"{station}: min={s['min']:.1f}, max={s['max']:.1f}, mean={s['mean']:.1f}")

        print("\nOutlier stations:")
        if outliers:
            for station in sorted(outliers):
                date_val, temp_val, mean_val = outliers[station]
                print(f"{station}: ({date_val.strftime('%I:%M:%S %p %m/%d/%Y')}, {temp_val:.1f}, {mean_val:.1f})")
        else:
            print("None")

        write_statistics(output_file, stats)
        print(f"\nStatistics written to {output_file}")
        return 0
    except OSError as exc:
        print(f"File access error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
