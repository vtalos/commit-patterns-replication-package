import os
import pandas as pd

def check_and_remove_zero_column_csvs(base_dir):
    # Expected subdirectories
    subdirs = [
        "CommitCountsPerDay",
        "CommitPercentagesPerDay",
        "CommitCountsPerHour",
        "CommitPercentagesPerHour"
    ]

    for subdir in subdirs:
        dir_path = os.path.join(base_dir, subdir)
        if not os.path.isdir(dir_path):
            print(f"Skipping missing directory: {dir_path}")
            continue

        output_txt = os.path.join(base_dir, f"{subdir}_ZeroColumns.txt")
        with open(output_txt, 'w') as log_file:
            for filename in os.listdir(dir_path):
                if not filename.endswith(".csv"):
                    continue

                file_path = os.path.join(dir_path, filename)
                try:
                    df = pd.read_csv(file_path)
                    zero_columns = df.columns[(df == 0).all()]
                    if not zero_columns.empty:
                        log_file.write(file_path + '\n')
                        os.remove(file_path)
                        print(f"Deleted file with all-zero column: {file_path}")
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python check_and_remove_zero_columns.py <base_directory>")
    else:
        check_and_remove_zero_column_csvs(sys.argv[1])