import os
import zlib
import random
import matplotlib.pyplot as plt
import numpy as np

def simple_scatter_plot_envelope():
    print("Generating raw data with lower envelope...")
    
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

    plt.figure(figsize=(12, 7))
    
    # Plotting Data
    plt.scatter(grad_x, grad_y, alpha=0.7, s=15, color='#2E86C1', label='Gradual Flips')
    plt.scatter(rand_x, rand_y, alpha=0.6, s=15, marker='x', color='#E74C3C', label='Pure Random Controls')
    plt.scatter(init_x, init_y, s=60, color='#F39C12', edgecolors='black', label='Starting Points (All 1s)', zorder=5)
    
    # --- SPATIAL BINNING (JAGGED ENVELOPE) ---
    all_x = np.array(init_x + grad_x + rand_x)
    all_y = np.array(init_y + grad_y + rand_y)
    
    # Create 150 equal-width bins across the x-axis space
    num_bins = 150
    bins = np.linspace(all_x.min(), all_x.max(), num_bins)
    bin_indices = np.digitize(all_x, bins)
    
    binned_x = []
    binned_y = []
    
    for b in range(1, len(bins)):
        in_bin = (bin_indices == b)
        if np.any(in_bin): # Only plot if there is data in this slice
            # Anchor the x-coordinate to the center of the bin
            bin_center = (bins[b-1] + bins[b]) / 2
            binned_x.append(bin_center)
            
            # Find the deepest dip specifically in this slice
            binned_y.append(np.min(all_y[in_bin]))
            
    # Plot the jagged envelope line
    plt.plot(binned_x, binned_y, color='lime', linewidth=2, label='Local Minima (Binned)', zorder=6)
    # ----------------------------------------

    plt.title('Bitstring Integer Value vs. Compressed Size with Lower Envelope')
    plt.xlabel('Integer Value (Base-10)')
    plt.ylabel('Compressed Size (Bytes)')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(frameon=True, shadow=True)
    
    plt.tight_layout()
    plt.savefig('compression_envelope.png')
    plt.show()

if __name__ == "__main__":
    simple_scatter_plot_envelope()