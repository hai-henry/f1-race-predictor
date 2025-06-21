import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def main():
    fastf1.plotting.setup_mpl(
        mpl_timedelta_support=True, misc_mpl_mods=False, color_scheme="fastf1"
    )
    fastf1.Cache.enable_cache("/Users/hai/Desktop/f1_cache")
    session = fastf1.get_session(2024, 12, "R")
    session.load()

    ham_fastest_lap = session.laps.pick_drivers("HAM").pick_fastest()
    ver_fastest_lap = session.laps.pick_drivers("VER").pick_fastest()

    ham_telemetry = ham_fastest_lap.get_car_data().add_distance()
    ver_telemetry = ver_fastest_lap.get_car_data().add_distance()

    mer_color = fastf1.plotting.get_team_color(ham_fastest_lap["Team"], session=session)
    red_color = fastf1.plotting.get_team_color(ver_fastest_lap["Team"], session=session)

    fig, ax = plt.subplots()

    fastest_lap = session.laps.pick_fastest()
    car_data = fastest_lap.get_car_data().add_distance()
    v_min = car_data["Speed"].min()
    v_max = car_data["Speed"].max()

    circuit_info = session.get_circuit_info()
    ax.vlines(
        x=circuit_info.corners["Distance"],
        ymin=v_min - 20,
        ymax=v_max + 20,
        color="grey",
        alpha=0.5,
        linestyles="dotted",
    )

    ax.plot(
        ham_telemetry["Distance"],
        ham_telemetry["Speed"],
        color=mer_color,
        label="HAM",
    )
    ax.plot(
        ver_telemetry["Distance"],
        ver_telemetry["Speed"],
        color=red_color,
        label="VER",
    )

    for _, corner in circuit_info.corners.iterrows():
        txt = f"{corner['Number']}{corner['Letter']}"
        ax.text(
            corner["Distance"],
            v_min - 30,
            txt,
            va="center_baseline",
            ha="center",
            size="small",
        )

    ax.set_xlabel("Distance (m)")
    ax.set_ylabel("Speed (km/h)")
    ax.legend()
    plt.suptitle(f"{session.event['EventName']} - Fastest Lap Telemetry")

    ax.set_ylim([v_min - 40, v_max + 20])

    plt.show()
    # Instead of distance do turns?


if __name__ == "__main__":
    main()
