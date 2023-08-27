import os
import argparse
import subprocess
import re

def clean_directory(directory):
    if os.path.exists(directory):
        for root, dirs, files in os.walk(directory, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))
    else:
        os.makedirs(directory)

def index_files(source_dir, temp_file):
    with open(temp_file, 'w') as f:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                f.write(os.path.join(root, file) + '\n')

def remove_duplicate_extensions(file_list):
    unique_extensions = set()
    cleaned_files = []
    for file in file_list:
        filename, extension = os.path.splitext(file)
        if extension not in unique_extensions:
            unique_extensions.add(extension)
            cleaned_files.append(file)
    return cleaned_files

def compress_non_mp3_files(source_dir, dest_dir):
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            filename, extension = os.path.splitext(file)
            if extension.lower() not in ['.mp3']:
                input_path = os.path.join(root, file)
                output_subdir = os.path.join(dest_dir, extension.lstrip('.'))
                os.makedirs(output_subdir, exist_ok=True)
                output_filename = file + '.mp3'
                output_path = os.path.join(output_subdir, output_filename)
                subprocess.run(['ffmpeg', '-i', input_path, '-c:a', 'libmp3lame', '-q:a', '2', output_path])

def rename_files(dest_dir, patterns):
    for root, dirs, files in os.walk(dest_dir):
        for pattern in patterns:
            for file in files:
                new_filename = file
                for pattern in patterns:
                    new_filename = new_filename.replace(pattern, '')
                new_filename = re.sub(r'[\s-]+', ' ', new_filename).strip()
                new_filename = re.sub(r'(?<=\.)[^.]+$','', new_filename)
                new_filename = re.sub(r'[^\w\s]', '', new_filename)
                new_filename = new_filename + '.mp3'

                old_path = os.path.join(root, file)
                new_path = os.path.join(root, new_filename)
                os.rename(old_path, new_path)

def main():
    parser = argparse.ArgumentParser(description='File processing script')
    parser.add_argument('--dir', required=True, help='Source directory')
    parser.add_argument('--rmt', help='String patterns to remove from filenames (separated by |)')
    args = parser.parse_args()

    source_dir = args.dir
    temp_file = 'temp_file.txt'
    temp_dir = 'temp_dir'
    compressed_dir = 'compressed_dir'
    remove_patterns = args.rmt.split('|') if args.rmt else []

    clean_directory(temp_dir)
    clean_directory(compressed_dir)

    index_files(source_dir, temp_file)

    with open(temp_file, 'r') as f:
        file_list = f.read().splitlines()

    cleaned_files = remove_duplicate_extensions(file_list)
    compress_non_mp3_files(source_dir, compressed_dir)

    rename_files(compressed_dir, remove_patterns)

    os.remove(temp_file)
    clean_directory(temp_dir)

if __name__ == '__main__':
    main()

