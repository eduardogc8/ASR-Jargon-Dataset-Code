import os

def fix_json_file(file_path):
    """
    Reads a JSON file line by line, replaces 'NaN' with 'null',
    and overwrites the original file with the corrected version.
    """
    temp_file_path = file_path + ".tmp"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f_in, \
             open(temp_file_path, 'w', encoding='utf-8') as f_out:
            
            print(f"Processing '{file_path}'...")
            for line in f_in:
                # To be safe, we replace ': NaN' to avoid changing "NaN" if it appears in a string.
                # JSON format for this is usually "key": NaN
                corrected_line = line.replace(': NaN', ': null')
                f_out.write(corrected_line)
        
        # Replace the original file with the corrected temporary file
        os.replace(temp_file_path, file_path)
        print(f"Successfully fixed '{file_path}'!")

    except Exception as e:
        print(f"An error occurred: {e}")
        # If something went wrong, remove the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

# --- Main execution ---
if __name__ == "__main__":
    # Path to the problematic JSON file
    # Make sure this path is correct relative to where you run the script.
    problematic_file = "dataset.json"
    
    fix_json_file(problematic_file)