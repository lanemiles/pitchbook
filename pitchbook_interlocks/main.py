from pitchbook_interlocks.models.universe import Universe
from pitchbook_interlocks.build_universe.build_universe import build_universe
from pitchbook_interlocks.print_results.print_results import print_results
import contextlib
import argparse


def main():
    parser = argparse.ArgumentParser(description="Pitchbook.")
    parser.add_argument(
        "--validate", action="store_true", help="Check the installation."
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Include extra logging while loading CSVs.",
    )
    args = parser.parse_args()

    if args.validate:
        print("The code is installed!")
        return

    universe = Universe(verbose_mode=args.verbose)
    if not universe.input_data_exists():
        print(
            "Missing one or more input data files. Please check the input_data directory."
        )
        return

    build_universe(universe)

    with open(universe.output_file, "w") as f:
        with contextlib.redirect_stdout(f):
            print_results(universe)


if __name__ == "__main__":
    main()
