import os
import argparse
import shutil

def rename_files(source_dir, dest_dir, remove_patterns):
    for root, dirs, files in os.walk(source_dir):
        for pattern in remove_patterns:
            for file in files:
                new_filename = file.replace(pattern, '')
                if new_filename != file:
                    old_path = os.path.join(root, file)
                    new_path = os.path.join(dest_dir, new_filename)
                    os.makedirs(os.path.dirname(new_path), exist_ok=True)
                    shutil.copy2(old_path, new_path)

def clean_filenames(dest_dir):
    for root, dirs, files in os.walk(dest_dir):
        for file in files:
            filename, extension = os.path.splitext(file)
            new_filename = filename.replace(' - ', ' ').replace('-', ' ')
            new_filename = new_filename.strip()
            new_filename = new_filename[:new_filename.rfind('.')] + extension
            new_filename = ''.join(c for c in new_filename if c.isalnum() or c.isspace() or c in ['.', '_'])
            new_path = os.path.join(root, new_filename)
            old_path = os.path.join(root, file)
            os.rename(old_path, new_path)

def main():
    parser = argparse.ArgumentParser(description='File renaming script')
    parser.add_argument('--dir', required=True, help='Source directory')
    parser.add_argument('--dest', required=True, help='Destination directory')
    parser.add_argument('--rmt', help='String patterns to remove from filenames (separated by |)')
    args = parser.parse_args()

    source_dir = args.dir
    dest_dir = args.dest
    remove_patterns = args.rmt.split('|') if args.rmt else []

    rename_files(source_dir, dest_dir, remove_patterns)
    clean_filenames(dest_dir)

if __name__ == '__main__':
    main()

