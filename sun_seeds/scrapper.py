import os

def scrape_directory(directory_path, output_file):
    with open(output_file, 'w') as f:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, directory_path)
                f.write(relative_path + '\n')

# Example usage:
directory_path = '/path/to/your/directory'
output_file = 'file_paths.txt'
scrape_directory(directory_path, output_file)
print(f"All file paths scraped and saved to '{output_file}'")
