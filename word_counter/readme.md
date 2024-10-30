# Word Counter

## Overview

The Word Counter script uses Python's threading to count words in large text files. It breaks the input file into smaller line chunks and spreads the work across ten threads. This helps use resources better and speeds up processing.

## Implementation

One of the main challenges I faced was sharing tasks among the threads. At first, I tried using `ThreadPoolExecutor`, but it didn’t keep a fixed number of threads. Instead, it only used as many threads as needed. For a 3.5 MB file, it ended up using only one thread, which wasn’t efficient.

To fix this, I decided to manage the threads myself. I split the input file into smaller parts to make sure each thread had a fair amount of work. This way, I had better control over how the threads were used, which improved the overall speed.

After the script counts the words, it creates a new text file. This output file takes the name of the input file and adds "output" to it (e.g., `input_filename_output.txt`). It is saved in the same folder where the script runs, making it easy to find.

## Testing

To check if the threading worked well, I ran two tests with these text files:

1. **"War and Peace"**: A text file of the classic novel, about 3.5 MB in size.
2. **Sample Text File**: A random text file I found online, about 100 MB.

Both tests showed that the workload was shared successfully among all the threads, proving that my method of chunking the file worked well.

## Conclusion

The Word Counter script demonstrates how to use threading to handle large text files efficiently. By carefully managing the tasks and testing, I was able to solve the challenges of distributing work, resulting in a useful word counting tool.
