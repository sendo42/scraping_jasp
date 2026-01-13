import os
import config

def load_progress(progress_path):
    if not os.path.exists(progress_path):
        return set()

    with open(progress_path, "r") as f:
        return set(line.strip() for line in f if line.strip())


def save_progress(progress_path, filename):
    with open(progress_path, "a") as f:
        f.write(filename + "\n")


def count_remaining_files():
    csv_files = [f for f in os.listdir(config.INPUT_DIR) if f.endswith(".csv")]
    done_files = load_progress(
        os.path.join(config.OUTPUT_DIR, "progress.txt")
    )
    return len([f for f in csv_files if f not in done_files])
