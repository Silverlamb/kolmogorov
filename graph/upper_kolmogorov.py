import os
import zlib
import random
import matplotlib.pyplot as plt
import numpy as np

def run_line_plot():
    plt.figure(figsize=(14, 8))

    print("Generating data and drawing chronological line plots...")
    
    # We will draw a continuous line for each 'n' cluster
    for n in range(32, 65):
        data_list = ['1'] * n
        
        # Initial point (Orange)
        initial_string = "".join(data_list)
        init_size = len(zlib.compress(initial_string.encode('utf-8')))
        init_int = int(initial_string, 2)
        
        # We will store the chronological journey here to draw the line
        journey_x = [init_int]
        journey_y = [init_size]

        # Gradual flips
        for _ in range(100):
            flip_index = random.randint(1, n - 1)
            data_list[flip_index] = '0' if data_list[flip_index] == '1' else '1'
            
            curr_str = "".join(data_list)
            curr_size = len(zlib.compress(curr_str.encode('utf-8')))
            curr_int = int(curr_str, 2)
            
            # Append the next step in the journey
            journey_x.append(curr_int)
            journey_y.append(curr_size)
            
        # Draw a literal line connecting the chronological sequence of flips for this 'n'
        plt.plot(journey_x, journey_y, color='#2E86C1', alpha=0.4, linewidth=1.5)
        
        # Plot the starting point
        plt.scatter(init_int, init_size, color='#F39C12', s=50, edgecolors='black', zorder=5)
        
        # Plot the random controls
        rand_x = []
        rand_y = []
        for _ in range(100):
            rand_str = "".join([random.choice(['0', '1']) for _ in range(n)])
            rand_size = len(zlib.compress(rand_str.encode('utf-8')))
            rand_int = int(rand_str, 2)
            rand_x.append(rand_int)
            rand_y.append(rand_size)
            
        plt.scatter(rand_x, rand_y, color='#E74C3C', alpha=0.1, s=12, marker='x')

    # Add custom legend entries since we plotted in a loop
    from matplotlib.lines import Line2D
    custom_lines = [
        Line2D([0], [0], color='#2E86C1', lw=2, alpha=0.7),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#F39C12', markersize=10, markeredgecolor='black'),
        Line2D([0], [0], marker='x', color='w', markeredgecolor='#E74C3C', markersize=10)
    ]
    plt.legend(custom_lines, ['Chronological Flip Path (Line Plot)', 'Starting Points (All 1s)', 'Pure Random Controls'], frameon=True, shadow=True)

    plt.title('Chronological Line Plot: The "Random Walk" of Bit Flipping')
    plt.xlabel('Integer Value (Base-10)')
    plt.ylabel('Compressed Size (Bytes)')
    plt.grid(True, which='both', linestyle='--', alpha=0.4)
    
    plt.tight_layout()
    plt.savefig('compression_chronological_lines.png')
    print("Graph saved as 'compression_chronological_lines.png'")

if __name__ == "__main__":
    run_line_plot()