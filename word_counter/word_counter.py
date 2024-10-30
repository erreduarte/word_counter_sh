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
            line = re.sub(r"[^\w\s']|(?<=\s)'|'(?=\s)", '', line.replace('\n', ' ')).lower()
            words = line.split()
            
            with counter_lock:
                word_counter.update(words)
    except Exception as e:
        logging.error(f"An error occurred in count_words: {e}")


def save(word_counter, output_file):
    """Saves the word counts to an output file."""
    total_words = sum(word_counter.values())
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

            logging.info(f"The input file contains a total of {total_lines} lines")
            logging.info(f"Each thread will process {lines_per_thread} lines")

        remaining_lines = total_lines % num_threads
        threads = []

        for i in range(num_threads):
            start = i * lines_per_thread
            end = start + lines_per_thread            
            thread_lines = lines[start:end]

            # Add remaining lines to the last thread
            if i == num_threads - 1:
                logging.info(f"Thread-{i + 1} will process data from {start} to {end} with {remaining_lines} additional lines")
                end += remaining_lines

            t = threading.Thread(target=count_words, args=(thread_lines,))
            threads.append(t)
            logging.info(f'{t.name} started processing lines {start} to {end}')
            t.start()

        for t in threads:
            t.join()

    except Exception as e:
        logging.error(f"An error occurred: {e}")

    logging.info(f"The input file {input_file} was closed")


if __name__ == '__main__':
    thread_job(input_file, num_threads)
    save(word_counter, output_file)
