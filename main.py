"""Example usage of the practice_data_sets package."""

from practice_data_sets import load_weather_data, describe_weather_data


def main():
    """
    Entry point for the script.
    """


    weather_df = load_weather_data()
    describe_weather_data(weather_df)


if __name__ == "__main__":
    main()
