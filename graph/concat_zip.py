import zlib
import random

def run_random_concat_experiment():
    n_bits = 4096
    iterations = 100
    
    total_size_a = 0
    total_size_b = 0
    total_size_individual = 0
    total_size_concat = 0
    
    for _ in range(iterations):
        # Create fully random 256-bit strings
        str_a = "".join(random.choices(['0', '1'], k=n_bits))
        str_b = "".join(random.choices(['0', '1'], k=n_bits))
        
        # Compress individually
        comp_a = len(zlib.compress(str_a.encode('utf-8')))
        comp_b = len(zlib.compress(str_b.encode('utf-8')))
        
        # Compress concatenated
        comp_concat = len(zlib.compress((str_a + str_b).encode('utf-8')))
        
        # Aggregate totals
        total_size_a += comp_a
        total_size_b += comp_b
        total_size_individual += (comp_a + comp_b)
        total_size_concat += comp_concat
        
    # Calculate averages
    avg_a = total_size_a / iterations
    avg_b = total_size_b / iterations
    avg_individual = total_size_individual / iterations
    avg_concat = total_size_concat / iterations
    
    # Display results
    print(f"--- Random String Concatenation Phenomenon ---")
    print(f"Over {iterations} iterations of {n_bits}-bit random strings:\n")
    print(f"Average Size of String A (Alone):              {avg_a:.2f} bytes")
    print(f"Average Size of String B (Alone):              {avg_b:.2f} bytes")
    print(f"----------------------------------------------------------")
    print(f"Average Size of A + B (Compressed Separately): {avg_individual:.2f} bytes")
    print(f"Average Size of A + B (Compressed Together):   {avg_concat:.2f} bytes")
    print(f"----------------------------------------------------------")
    print(f"Average Savings by Concatenating:              {avg_individual - avg_concat:.2f} bytes")

if __name__ == "__main__":
    run_random_concat_experiment()