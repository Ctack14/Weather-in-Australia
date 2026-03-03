import os
from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns
import logging
from multiprocessing import Pool

logger = logging.getLogger(__name__)

class DataVisualizer:
    """Visualizes weather data"""

    def __init__(self, df, output_dir = None):
        self.df = df
        self.sample_df = df.sample(n=2000)  # Sample a subset of the data for visualization

        # Set the output directory for saving plots. If not provided, it defaults to a "data/images" directory relative to this file.
        if output_dir is None:
            self.output_dir = Path(__file__).parent / "data" / "images"
        else:
            self.output_dir = Path(output_dir)




    def display_average_max_temperature_by_location(self):
        """
        Displays a bar plot of the average temperature by location.
        """

        print(self.sample_df["MaxTemp"].dtype)
        print(self.sample_df["MaxTemp"].head(10))

        avg_temp_by_location = self.sample_df.groupby("Location")["MaxTemp"].mean().reset_index()

        # Create a wider figure so the x-axis (locations) has more horizontal space
        fig, ax = plt.subplots(figsize=(14, 6))

        sns.barplot(x="Location", y="MaxTemp", data=avg_temp_by_location, ax=ax)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90)  # Rotate x-ticks for better readability
        ax.set_title("Average Max Temperature by Location")
        ax.set_xlabel("Location")
        ax.set_ylabel("Average Max Temperature")

        plt.tight_layout()
        plt.show()


    def display_distribution_for_location(self, locations: list, type: str):
        """
        Displays a histogram of the distribution for each specific location in the list based on the type (temperature or rainfall).

        Args:
            locations (list) - A list of locations for which to display the distribution.
            type (str) - The type of distribution to display ("temperature" or "rainfall").
        """

        type = type.lower()
        location_set = set(locations)  # Faster lookup and compatability between set and NumPy array

        # splits the data into groups based on location for multiprocessing
        groups = [group for location, group in self.sample_df.groupby("Location") if location in location_set]
        tasks = [(group, type, self.output_dir) for group in groups]

        logger.info(f"Plotting {type} distributions for locations: " + ", ".join(locations))

        with Pool(processes=os.cpu_count()) as pool:
            pool.map(_plot_distribution, tasks)



    def display_rainfall_vs_temperature(self):
        """
        Displays a scatter plot of rainfall vs. temperature.
        """

        sns.scatterplot(x=self.sample_df["MaxTemp"],
                        y=self.sample_df["Rainfall"])
        plt.title("Rainfall vs. Max Temperature")
        plt.xlabel("Max Temperature")
        plt.ylabel("Rainfall")
        plt.show()


    def display_wind_speed_vs_temp_change(self):
        """
        Displays a regression plotplot of wind speed based on how much the size of temperature difference of max and min temperature.
        """

        sns.regplot(x=self.sample_df["MaxTemp"] - self.sample_df["MinTemp"],
                    y=self.sample_df["WindGustSpeed"],
                    scatter_kws={"color": "blue", "alpha": 0.5},
                    line_kws={"color": "red", "linewidth": 2, "alpha": 1.0})

        plt.title("Wind Gust Speed vs. Temperature Change")
        plt.xlabel("Temperature Change (MaxTemp - MinTemp)")
        plt.ylabel("Wind Gust Speed")
        plt.show()


    def display_evaporation_vs_sunshine(self):
        """
        Displays a regression plot of evaporation based on sunshine hours.
        """

        sns.regplot(x=self.sample_df["Sunshine"],
                    y=self.sample_df["Evaporation"],
                    scatter_kws={"color": "blue", "alpha": 0.5},
                    line_kws={"color": "red", "linewidth": 2, "alpha": 1.0})

        plt.title("Evaporation vs. Sunshine Hours")
        plt.xlabel("Sunshine Hours")
        plt.ylabel("Evaporation")
        plt.show()


def _plot_distribution(args: tuple):
    """
    Helper function to plot a distribution for a single location. This is used for multiprocessing.

    args (tuple): A tuple containing:
            - group (pd.DataFrame): The location's temperature data.
            - dist_type (str): The distribution type ("temperature" or "rainfall").
            - output_dir (str): The directory where the plot will be saved.
    """

    group, dist_type, output_dir = args
    location = group["Location"].iloc[0]
    if group.empty:
        logger.info(f"No data available for location: {location}")
        return

    filename = f"{location}_{dist_type}_distribution.png"
    filepath = os.path.join(output_dir, filename)

    match dist_type:
        case "temperature":
            column = "MaxTemp"
        case "rainfall":
            column = "Rainfall"
        case _:
            logger.error(f"Unknown distribution type: {dist_type}")
            return

    plt.figure(figsize=(10, 6))
    sns.histplot(group[column], bins=30, kde=True)
    plt.title(f"{dist_type} Distribution for {location}")
    if dist_type == "Temperature":
        plt.xlabel(f"Max {dist_type}")
    else:
        plt.xlabel(dist_type)
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(filepath)
    plt.close()