import os
import zlib
import random
import matplotlib.pyplot as plt

def simple_scatter_plot_opaque():
    print("Generating raw data with higher opacity...")
    
    init_x, init_y = [], []
    grad_x, grad_y = [], []
    rand_x, rand_y = [], []
    
    for n in range(32, 65):
        data_list = ['1'] * n
        
        # 1. Starting Point (All 1s)
        initial_string = "".join(data_list)
        init_size = len(zlib.compress(initial_string.encode('utf-8')))
        init_int = int(initial_string, 2)
        init_x.append(init_int)
        init_y.append(init_size)

        # 2. Gradual Flips
        for _ in range(100):
            flip_index = random.randint(1, n - 1)
            data_list[flip_index] = '0' if data_list[flip_index] == '1' else '1'
            
            curr_str = "".join(data_list)
            curr_size = len(zlib.compress(curr_str.encode('utf-8')))
            curr_int = int(curr_str, 2)
            grad_x.append(curr_int)
            grad_y.append(curr_size)
                
        # 3. Pure Random Controls
        for _ in range(100):
            rand_str = "".join([random.choice(['0', '1']) for _ in range(n)])
            rand_size = len(zlib.compress(rand_str.encode('utf-8')))
            rand_int = int(rand_str, 2)
            rand_x.append(rand_int)
            rand_y.append(rand_size)

    # Plotting the raw data
    plt.figure(figsize=(12, 7))
    
    # Plot Gradual (Blue) - Alpha increased to 0.6
    plt.scatter(grad_x, grad_y, alpha=0.7, s=15, color='#2E86C1', label='Gradual Flips')
    
    # Plot Random Controls (Red) - Alpha increased to 0.5
    plt.scatter(rand_x, rand_y, alpha=0.6, s=15, marker='x', color='#E74C3C', label='Pure Random Controls')
    
    # Plot Starting Points (Orange)
    plt.scatter(init_x, init_y, s=60, color='#F39C12', edgecolors='black', label='Starting Points (All 1s)', zorder=5)
    
    plt.title('Raw Data: Bitstring Integer Value vs. Compressed Size')
    plt.xlabel('Integer Value (Base-10)')
    plt.ylabel('Compressed Size (Bytes)')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(frameon=True, shadow=True)
    
    plt.tight_layout()
    plt.savefig('compression_raw_scatter.png')

if __name__ == "__main__":
    simple_scatter_plot_opaque()