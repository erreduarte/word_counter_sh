import threading
import logging
from pathlib import Path
from collections import Counter
import re

# Configuration
input_file = "war_and_peace.txt"
num_threads = 10
output_file = f"{input_file[:-4]}_wordcount.txt"

# Initialize thread-safe counter and lock
counter_lock = threading.Lock()
word_counter = Counter()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def count_words(thread_lines):
    """Counts words in a given set of lines, updates shared word counter."""
    try:
        for line in thread_lines:
            if isinstance(line, bytes):
                line = line.decode('utf-8')
            # Cleanup tailored for literary texts; for other types, consider using strip for specific elements.
            # Lowercasing standardizes all words to prevent counting distinctions. e.g.: Word: 1 / word: 1
            line = re.sub(r"[^\w\s']|(?<=\s)'|'(?=\s)", '', line.replace('\n', ' ')).lower()
            words = line.split()
            
            with counter_lock:
                word_counter.update(words)
    except Exception as e:
        logging.error(f"An error occurred in count_words: {e}")


def save(word_counter, output_file):
    """Saves the word counts to an output file."""
    #For the purpose of printing the counting of words after processing.
    total_words = sum(word_counter.values())
    #For the purpose of printing the whole path after file is processed.
    output_path = Path(output_file).resolve()

    try:
        with open(output_path, 'w') as output_file:
            for word, count in word_counter.most_common():
                output_file.write(f"{word}:{count}\n")
    except Exception as e:
        logging.error(f"An error occurred in save function: {e}")

    logging.info(f"A total of {total_words} words were processed")    
    logging.info(f"Output file was saved in the following directory: {output_path}")


def thread_job(filename, num_threads):
    """Divides the file into chunks and assigns each to a separate thread for processing."""
    
    try:
        logging.info(f"Opening input file {filename}")
        with open(filename, 'rb') as file_pointer:
            lines = file_pointer.readlines()
            total_lines = len(lines)
            lines_per_thread = total_lines // num_threads

            logging.info(f"The input file contains a total of {total_lines} line(s)")
            logging.info(f"Each thread will process {lines_per_thread} line(s)")

        remaining_lines = total_lines % num_threads
        logging.info(f"A total of {remaining_lines} remaining line(s) will be distributed across threads")
        threads = []
        #Set previous end so processing don't overlap
        previous_end = 0

        for i in range(num_threads):
            start = previous_end 
            end = start + lines_per_thread + (1 if i < remaining_lines else 0) ## If there are remaining lines, add 1 to the end for the first few threads.
           
            
            #Making sure start from threads don't overlap with end of the previous one.
            if i > 0:
                start = previous_end + 1 
            
            previous_end = end #Ensure next line start in the right position

            
            thread_lines = lines[start:end]

            t = threading.Thread(target=count_words, args=(thread_lines,))
            threads.append(t)
            #Logs lines that will be processed and remaining lines if they exist.
            logging.info(f'{t.name} started processing lines {start} to {end} and {1 if i < remaining_lines else 0} remaining line(s)')
            t.start()

        for t in threads:
            t.join()

    except Exception as e:
        logging.error(f"An error occurred in thread_job: {e}")

    logging.info(f"The input file {input_file} was closed")


if __name__ == '__main__':
    thread_job(input_file, num_threads)
    save(word_counter, output_file)
