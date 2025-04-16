#!/usr/bin/env python3
"""
Command line interface for the UoC Creator
"""
import argparse
import sys

from src import StopExecution, UoCCreator


def main():
    parser = argparse.ArgumentParser(description="Create Unit of Competency documentation")
    parser.add_argument("--setup-templates", action="store_true", 
                       help="Download templates from VU intranet")
    parser.add_argument("--unit-code", type=str,
                       help="Unit of Competency code to process")
    parser.add_argument("--course-code", type=str,
                       help="Course code (optional)")
    parser.add_argument("--course-title", type=str,
                       help="Course title (optional)")
    parser.add_argument("--interactive", action="store_true",
                       help="Run in interactive mode")
    
    args = parser.parse_args()
    
    try:
        creator = UoCCreator()
        
        if args.setup_templates:
            creator.setup_templates()
            print("Templates downloaded successfully")
            if not args.unit_code and not args.interactive:
                return 0
        
        if args.interactive:
            creator = UoCCreator.interactive_prepare_unit()
            print(f"Successfully prepared documentation for {creator.unit_code}")
            return 0
        
        if args.unit_code:
            additional_details = {}
            if args.course_code:
                additional_details['course_code'] = args.course_code
            if args.course_title:
                additional_details['course_title'] = args.course_title
            
            creator.prepare_unit(args.unit_code, additional_details)
            print(f"Successfully prepared documentation for {args.unit_code}")
            return 0
        
        parser.print_help()
        return 1
        
    except StopExecution:
        print("Operation cancelled by user")
        return 1
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
