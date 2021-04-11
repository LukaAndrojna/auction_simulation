from models.simulation import Simulation


def main():
    simulation = Simulation(100, 2, 5.0, 10.0, 1000)
    simulation.run()


if __name__ == "__main__":
    main()