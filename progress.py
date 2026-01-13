import os

def load_progress(progress_path):
    if not os.path.exists(progress_path):
        return set()

    with open(progress_path, "r") as f:
        return set(line.strip() for line in f if line.strip())


def save_progress(progress_path, filename):
    with open(progress_path, "a") as f:
        f.write(filename + "\n")
