import os
import zlib
import random
import matplotlib.pyplot as plt
import csv

def run_range_experiment():
    results = []
    num_flips = 100            # Flips to perform per 'n'
    num_random_controls = 100  # Controls to generate per 'n'
    results_file = "compression_results_range.csv"
    
    print("Running experiment for n = 32 to 64...")
    
    for n in range(32, 65):
        data_list = ['1'] * n
        
        # Initial state
        initial_string = "".join(data_list)
        initial_compressed_size = len(zlib.compress(initial_string.encode('utf-8')))
        initial_int = int(initial_string, 2)
        results.append((n, "Gradual", initial_int, initial_compressed_size))

        # Flips
        for _ in range(num_flips):
            flip_index = random.randint(1, n - 1)
            
            # Toggle the character
            if data_list[flip_index] == '1':
                data_list[flip_index] = '0'
            else:
                data_list[flip_index] = '1'
                
            current_string = "".join(data_list)
            compressed_size = len(zlib.compress(current_string.encode('utf-8')))
            current_int = int(current_string, 2)
            results.append((n, "Gradual", current_int, compressed_size))

        for _ in range(num_random_controls):
            random_string = "".join([random.choice(['0', '1']) for _ in range(n)])
            random_compressed_size = len(zlib.compress(random_string.encode('utf-8')))
            random_int = int(random_string, 2)
            results.append((n, "Random", random_int, random_compressed_size))

    with open(results_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["n_bits", "Type", "Integer_Value", "Compressed_Size_Bytes"])
        writer.writerows(results)

    gradual_ints = [r[2] for r in results if r[1] == "Gradual"]
    gradual_sizes = [r[3] for r in results if r[1] == "Gradual"]
    
    random_ints = [r[2] for r in results if r[1] == "Random"]
    random_sizes = [r[3] for r in results if r[1] == "Random"]

    plt.figure(figsize=(12, 7))
    
    plt.scatter(gradual_ints, gradual_sizes, alpha=0.3, color='blue', s=15, label='Gradual Flips')
    plt.scatter(random_ints, random_sizes, alpha=0.2, color='red', marker='x', s=15, label='Random Controls')
    
    plt.xscale('log')
    
    plt.title('Integer Value vs. Compressed Size (n = 32 to 64 bits)')
    plt.xlabel('Integer Value (Log Scale, Base-10 representation)')
    plt.ylabel('Compressed Size (Bytes)')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('compression_plot_range.png')
    
    print("--- Experiment Complete ---")
    print(f"File created: '{results_file}'")
    print(f"File created: 'compression_plot_range.png'")

if __name__ == "__main__":
    run_range_experiment()