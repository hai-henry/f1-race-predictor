import fastf1


def main():
    # Enable the cache for FastF1
    fastf1.Cache.enable_cache("f1_cache")

    # Load the session data for the Australian Grand Prix 2024
    session = fastf1.get_session(2024, "Australia", "R")
    session.load()
    print(session.name)


if __name__ == "__main__":
    main()
