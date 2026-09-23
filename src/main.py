import sys
from simulation import Simulator


def main() -> None:

    if len(sys.argv) != 2:
        print("Usage: python3 main.py <map_file>", file=sys.stderr)
        sys.exit(1)

    map_file = sys.argv[1]

    try:
        simulator = Simulator(map_file)
        simulator.simulate()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
