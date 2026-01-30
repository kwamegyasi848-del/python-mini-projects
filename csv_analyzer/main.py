import csv
import argparse

def analyze_csv(file_path):
    with open(file_path, newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    if not rows:
        print("CSV file is empty.")
        return

    headers = rows[0]
    data = rows[1:]

    print(f"Total rows: {len(data)}")
    print("Columns:")
    for header in headers:
        print(f"- {header}")

def main():
    parser = argparse.ArgumentParser(description="Analyze a CSV file")
    parser.add_argument("--file", required=True, help="Path to CSV file")
    args = parser.parse_args()

    analyze_csv(args.file)

if __name__ == "__main__":
    main()
