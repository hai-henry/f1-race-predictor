import fastf1


def main():
    session = fastf1.get_session(2024, 1, "Q")
    session.load()
    print(session.results)


if __name__ == "__main__":
    main()
