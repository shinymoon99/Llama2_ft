import os

def combine_text_files(input_folder, output_file):
# Usage example:
# input_folder = 'path/to/your/input/folder'
# output_file = 'path/to/your/output/file.txt'
# combine_text_files(input_folder, output_file)

    try:
        # Open the output file in write mode
        with open(output_file, 'w') as output_file:
            # List all files in the input folder
            files = os.listdir(input_folder)

            # Iterate through the files
            for file_name in files:
                if file_name.endswith('.txt'):  # Check if the file is a .txt file
                    file_path = os.path.join(input_folder, file_name)
                    
                    # Open the current text file and read its contents
                    with open(file_path, 'r') as input_file:
                        lines = input_file.readlines()
                        
                        # Append the content of the current file to the output file
                        output_file.writelines(lines)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

