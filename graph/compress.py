import os
import glob

def compress_to_text_files(base_directory: str = "."):
    target_folder = "bb_compressed_unique"
    os.makedirs(target_folder, exist_ok=True)
    print(f"Output directory established: ./{target_folder}/")

    seen_tapes = set() 
    
    file_limit = 100000
    current_file_idx = 1
    current_file_count = 0
    current_file = None
    
    search_pattern = os.path.join(base_directory, "bb*_*", "*.txt")
    all_files = [f for f in glob.glob(search_pattern) if target_folder not in f]
    
    print(f"Found {len(all_files)} files to process. Starting compression...\n")
    
    total_lines_read = 0
    unique_saved = 0
    
    for file_path in all_files:
        print(f"Processing: {file_path}")
        
        with open(file_path, 'r') as file:
            for line in file:
                total_lines_read += 1
                line = line.strip()
                if not line:
                    continue
                    
                parts = line.split(",")
                if len(parts) != 2:
                    continue
                    
                tape = parts[1]
                
                if tape in seen_tapes:
                    continue
                    
                seen_tapes.add(tape)
                
                if current_file is None:
                    out_path = os.path.join(target_folder, f"minimum_unique_halting_machines_{current_file_idx}.txt")
                    current_file = open(out_path, 'w')
                    
                current_file.write(f"{line}\n")
                current_file_count += 1
                unique_saved += 1
                
                if current_file_count >= file_limit:
                    current_file.close()
                    current_file = None
                    current_file_idx += 1
                    current_file_count = 0
                    
    if current_file is not None and not current_file.closed:
        current_file.close()
        
    print("\n--- COMPRESSION COMPLETE ---")
    print(f"Total lines read: {total_lines_read:,}")
    print(f"Total UNIQUE machines saved: {unique_saved:,}")
    print(f"Data safely secured across {current_file_idx} files in '{target_folder}/'.")

if __name__ == "__main__":
    compress_to_text_files()