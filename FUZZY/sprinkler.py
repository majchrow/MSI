import random

import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from matplotlib.animation import FuncAnimation


class Sprinkler:
    def __init__(self, timeout=10000):
        self.day = 0
        self.hydration = 0
        self.temperature = 0
        self.reserves = 0
        random.seed(42)
        self.fig, (self.ax0, self.ax1, self.ax2, self.ax3, self.ax_agg) = plt.subplots(nrows=5, figsize=(8, 12))
        self.fig.tight_layout()
        for ax in (self.ax0, self.ax1, self.ax2, self.ax3, self.ax_agg):
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.get_xaxis().tick_bottom()
            ax.get_yaxis().tick_left()
        self.a = FuncAnimation(self.fig, self.run_one_iteration, interval=timeout)
        plt.show()

    @staticmethod
    def custom_trapmf(x, y, min, max):
        a, b, c, d = y
        return fuzz.trapmf(x, [a, b, max, max]) + fuzz.trapmf(x, [min, min, c, d])

    def run_one_iteration(self, i):
        self.day = random.randint(0, 24)
        self.hydration = random.randint(0, 100)
        self.temperature = random.randint(-10, 30)
        self.reserves = random.randint(0, 100)

        self.ax0.clear()
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        self.ax_agg.clear()

        x_day = np.arange(0, 24, 1)
        x_hydration = np.arange(0, 100, 1)
        x_temperature = np.arange(-10, 30, 1)
        x_reserves = np.arange(0, 100, 1)
        x_watering = np.arange(0, 100, 1)

        day_morning = fuzz.trimf(x_day, [6, 9, 12])
        day_noon = fuzz.trimf(x_day, [8, 12, 16])
        day_evening = fuzz.trimf(x_day, [14, 18, 22])
        day_night = self.custom_trapmf(x_day, [20, 22, 6, 8], 0, 24)

        hydration_empty = fuzz.trimf(x_hydration, [0, 0, 10])
        hydration_low = fuzz.trapmf(x_hydration, [10, 20, 40, 50])
        hydration_medium = fuzz.trapmf(x_hydration, [35, 45, 65, 75])
        hydration_high = fuzz.trapmf(x_hydration, [60, 70, 90, 100])

        temperature_low = fuzz.trimf(x_temperature, [-10, -10, 5])
        temperature_neutral = fuzz.trimf(x_temperature, [0, 15, 30])
        temperature_high = fuzz.trimf(x_temperature, [10, 30, 30])

        reserves_critical = fuzz.trimf(x_reserves, [0, 0, 10])
        reserves_low = fuzz.trapmf(x_reserves, [10, 20, 40, 50])
        reserves_medium = fuzz.trapmf(x_reserves, [35, 45, 65, 75])
        reserves_high = fuzz.trapmf(x_reserves, [60, 70, 90, 100])

        watering_empty = fuzz.trimf(x_watering, [0, 0, 10])
        watering_low = fuzz.trapmf(x_watering, [10, 20, 40, 50])
        watering_medium = fuzz.trapmf(x_watering, [35, 45, 65, 75])
        watering_high = fuzz.trapmf(x_watering, [60, 70, 90, 100])

        self.ax0.plot(x_day, day_morning, 'b', linewidth=1.5, label='Poranek')
        self.ax0.plot(x_day, day_noon, 'g', linewidth=1.5, label='Południe')
        self.ax0.plot(x_day, day_evening, 'r', linewidth=1.5, label='Wieczór')
        self.ax0.plot(x_day, day_night, 'k', linewidth=1.5, label='Noc')
        self.ax0.set_title('Pora dnia')
        self.ax0.legend()
        day_aggregated = np.fmax(
            day_morning,
            np.fmax(
                day_noon,
                np.fmax(
                    day_evening,
                    day_night
                )
            )
        )
        y = fuzz.interp_membership(x_day, day_aggregated, self.day)
        self.ax0.vlines(self.day, 0, y, color="c")

        self.ax1.plot(x_hydration, hydration_empty, 'k', linewidth=1.5, label='Brak')
        self.ax1.plot(x_hydration, hydration_low, 'b', linewidth=1.5, label='Małe')
        self.ax1.plot(x_hydration, hydration_medium, 'g', linewidth=1.5, label='Średnie')
        self.ax1.plot(x_hydration, hydration_high, 'r', linewidth=1.5, label='Duże')
        self.ax1.set_title('Nawodnienie gleby')
        self.ax1.legend()
        hydration_aggregated = np.fmax(
            hydration_empty,
            np.fmax(
                hydration_low,
                np.fmax(
                    hydration_medium,
                    hydration_high
                )
            )
        )
        y = fuzz.interp_membership(x_hydration, hydration_aggregated, self.hydration)
        self.ax1.vlines(self.hydration, 0, y, color="c")

        self.ax2.plot(x_temperature, temperature_low, 'b', linewidth=1.5, label='Zimno')
        self.ax2.plot(x_temperature, temperature_neutral, 'g', linewidth=1.5, label='Umiarkowanie')
        self.ax2.plot(x_temperature, temperature_high, 'r', linewidth=1.5, label='Gorąco')
        self.ax2.set_title('Temperatura powietrza')
        self.ax2.legend()
        temperature_aggregated = np.fmax(
            temperature_low,
            np.fmax(
                temperature_neutral,
                temperature_high
            )
        )
        y = fuzz.interp_membership(x_temperature, temperature_aggregated, self.temperature)
        self.ax2.vlines(self.temperature, 0, y, color="c")

        self.ax3.plot(x_hydration, hydration_empty, 'k', linewidth=1.5, label='Krytyczny')
        self.ax3.plot(x_hydration, hydration_low, 'b', linewidth=1.5, label='Mały')
        self.ax3.plot(x_hydration, hydration_medium, 'g', linewidth=1.5, label='Średni')
        self.ax3.plot(x_hydration, hydration_high, 'r', linewidth=1.5, label='Duży')
        self.ax3.set_title('Poziom rezerw wody')
        self.ax3.legend()
        reserves_aggregated = np.fmax(
            reserves_critical,
            np.fmax(
                reserves_low,
                np.fmax(
                    reserves_medium,
                    reserves_high
                )
            )
        )
        y = fuzz.interp_membership(x_reserves, reserves_aggregated, self.reserves)
        self.ax3.vlines(self.reserves, 0, y, color="c")

        day_morning_level = fuzz.interp_membership(x_day, day_morning, self.day)
        day_noon_level = fuzz.interp_membership(x_day, day_noon, self.day)
        day_evening_level = fuzz.interp_membership(x_day, day_evening, self.day)
        day_night_level = fuzz.interp_membership(x_day, day_night, self.day)

        hydration_empty_level = fuzz.interp_membership(x_hydration, hydration_empty, self.hydration)
        hydration_low_level = fuzz.interp_membership(x_hydration, hydration_low, self.hydration)
        hydration_medium_level = fuzz.interp_membership(x_hydration, hydration_medium, self.hydration)
        hydration_high_level = fuzz.interp_membership(x_hydration, hydration_high, self.hydration)

        temperature_low_level = fuzz.interp_membership(x_temperature, temperature_low, self.temperature)
        temperature_neutral_level = fuzz.interp_membership(x_temperature, temperature_neutral, self.temperature)
        temperature_high_level = fuzz.interp_membership(x_temperature, temperature_high, self.temperature)

        reserves_critical_level = fuzz.interp_membership(x_reserves, reserves_critical, self.reserves)
        reserves_low_level = fuzz.interp_membership(x_reserves, reserves_low, self.reserves)
        reserves_medium_level = fuzz.interp_membership(x_reserves, reserves_medium, self.reserves)
        reserves_high_level = fuzz.interp_membership(x_reserves, reserves_high, self.reserves)

        results = []
        rule1 = day_noon_level
        results.append(np.fmin(rule1, watering_low))

        rule2 = np.fmax(day_morning_level, day_evening_level)
        results.append(np.fmin(rule2, watering_medium))

        rule3 = day_night_level
        results.append(np.fmin(rule3, watering_high))

        rule4 = temperature_low_level
        results.append(np.fmin(rule4, watering_low))

        rule5 = temperature_neutral_level
        results.append(np.fmin(rule5, watering_medium))

        rule6 = temperature_high_level
        results.append(np.fmin(rule6, watering_high))

        rule7 = hydration_empty_level
        results.append(np.fmin(rule7, watering_high))

        rule8 = hydration_low_level
        results.append(np.fmin(rule8, watering_medium))

        rule9 = np.fmax(hydration_medium_level, hydration_high_level)
        results.append(np.fmin(rule9, watering_low))

        rule10 = reserves_critical_level
        results.append(np.fmin(rule10, watering_empty))

        rule11 = reserves_low_level
        results.append(np.fmin(rule11, watering_low))

        rule12 = reserves_medium_level
        results.append(np.fmin(rule12, watering_medium))

        rule13 = reserves_high_level
        results.append(np.fmin(rule13, watering_high))

        rule14 = np.fmin(day_noon_level, np.fmax(hydration_medium_level, hydration_high_level))
        results.append(np.fmin(rule14, watering_empty))

        rule15 = np.fmin(np.fmax(reserves_low_level, np.fmax(reserves_medium_level, reserves_high_level)),
                         np.fmax(hydration_medium_level, hydration_high_level))
        results.append(np.fmin(rule15, watering_empty))

        rule16 = np.fmin(day_night_level, reserves_low_level)
        results.append(np.fmin(rule16, watering_medium))

        rule17 = np.fmin(temperature_neutral_level, reserves_medium_level)
        results.append(np.fmin(rule17, watering_low))

        rule18 = np.fmin(
            np.fmax(np.fmax(day_noon_level, day_morning_level), day_evening_level),
            np.fmax(hydration_high_level, hydration_medium_level)
        )
        results.append(np.fmin(rule18, watering_empty))

        aggregated = results[0]
        for value in results[1:]:
            aggregated = np.fmax(aggregated, value)

        min_of_max = fuzz.defuzz(x_watering, aggregated, 'som')
        y = fuzz.interp_membership(x_watering, aggregated, min_of_max)
        self.ax_agg.plot(x_hydration, hydration_empty, 'k', linewidth=0.5, label='Brak', linestyle='--')
        self.ax_agg.plot(x_hydration, hydration_low, 'b', linewidth=0.5, label='Małe', linestyle='--')
        self.ax_agg.plot(x_hydration, hydration_medium, 'g', linewidth=0.5, label='Średnie', linestyle='--')
        self.ax_agg.plot(x_hydration, hydration_high, 'm', linewidth=0.5, label='Duże', linestyle='--')
        self.ax_agg.plot(x_watering, aggregated, 'r', linewidth=1.5, label='Output')
        self.ax_agg.vlines(min_of_max, 0, y, color="c")
        self.ax_agg.set_title('Nawadnianie')
        self.ax_agg.legend()
