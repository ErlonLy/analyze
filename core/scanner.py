import os

def list_all_files(folder_path):
    collected = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            collected.append(os.path.join(root, file))
    return collected
