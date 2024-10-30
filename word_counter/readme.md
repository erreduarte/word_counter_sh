# Word Counter

## Overview

The Word Counter script uses Python's threading to count words in large text files. It breaks the input file into smaller line chunks and spreads the work across ten threads. This helps use resources better and speeds up processing.

## Implementation

### Functions

- **count_words(thread_lines)**: This function takes a list of lines (a chunk) as input. It decodes the lines if they are in bytes, cleans up the text by removing unwanted characters using a regex, and then splits the lines into words. It updates the global `word_counter` with the count of each word, ensuring thread safety with a lock.

- **save(word_counter, output_file)**: This function saves the word counts to a new output file. It calculates the total number of words processed and writes each word and its count to the file in descending order. It also prints out the total number of words processed and the location of the output file.

- **thread_job(filename, num_threads)**: This function manages the threading process. It reads the input file, calculates how many lines each thread should handle, and creates threads to process the chunks of lines. It also handles any remaining lines that do not evenly divide among the threads. It starts each thread and waits for them to finish.

## Testing

To check if the threading worked well, I ran two tests with these text files:

1. **"War and Peace"**: A text file of the classic novel, about 3.5 MB in size.
2. **Sample Text File**: A random text file I found online, about 100 MB.

Both tests showed that the workload was shared successfully among all the threads, proving that my method of chunking the file worked well.

## Conclusion

The Word Counter script demonstrates how to use threading to handle large text files efficiently. By carefully managing the tasks and testing, I was able to solve the challenges of distributing work, resulting in a useful word counting tool.
