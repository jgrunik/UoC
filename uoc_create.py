#!/usr/bin/env python3
"""
Command line interface for the UoC Creator
"""
import argparse
import sys

from src import UoCCreator


def main():
    parser = argparse.ArgumentParser(
        description="Create Unit of Competency documentation"
    )
    parser.add_argument(
        "--setup-templates",
        action="store_true",
        help="Download templates from VU intranet",
    )
    parser.add_argument(
        "--unit-code", type=str, help="Unit of Competency code to process"
    )
    parser.add_argument("--course-code", type=str, help="Course code (optional)")
    parser.add_argument("--course-title", type=str, help="Course title (optional)")
    parser.add_argument(
        "--interactive", action="store_true", help="Run in interactive mode"
    )

    args = parser.parse_args()

    try:
        if args.interactive:
            creator = UoCCreator.interactive_prepare_unit()
            print(f"Successfully prepared documentation for {creator.unit_code}")
            return 0

        # Handle template setup and/or unit creation mode.
        if args.unit_code or args.setup_templates:
            creator = UoCCreator()

            if args.setup_templates:
                creator.setup_templates()
                print("Templates downloaded successfully")

            if args.unit_code:
                # Create a dictionary of optional details, filtering out empty values.
                additional_details = {
                    k: v
                    for k, v in {
                        "course_code": args.course_code,
                        "course_title": args.course_title,
                    }.items()
                    if v
                }
                creator.prepare_unit(args.unit_code, additional_details)
                print(f"Successfully prepared documentation for {args.unit_code}")
            return 0

        # If no valid combination of arguments is provided, show help.
        parser.print_help()
        return 1

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
