import threading
import logging
from pathlib import Path
from collections import Counter
import re
import time



input_file = "war_and_peace.txt"
num_threads = 10
counter_lock = threading.Lock()
word_counter = Counter()
output_file = f"{input_file[:-4]}_wordcount.txt"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def count_words(thread_lines):
    
    try:

        for line in thread_lines:
            if isinstance(line, bytes):
                line = line.decode('utf-8')
        
            line = line.replace('\n', ' ')
            # This regex may need adjustment based on the content of the file. 
            # It works well for book-like text but may not be suitable for files 
            # containing URLs or other non-standard text.
            line = re.sub(r"[^\w\s']|(?<=\s)'|'(?=\s)", '', line).lower()

            words = line.split()
            
            with counter_lock:
                word_counter.update(words)

    except Exception as e:
        logging.error(f"An error ocurred in count_words: {e}")   



def save(word_counter, output_file):
    
    #Count total number of words just to print out as reference.
    total_words = sum(word_counter.values())

    #Save output file to the current directory
    output_path = Path(output_file)

    try:
        with open(output_path, 'w') as output_file:
            # Iterate in descending order using 'most_common'.
            # In ascending order include [::-1]
            for word, count in word_counter.most_common():
                output_file.write(f"{word}:{count}\n")

    except Exception as e:
        logging.error(f"An error occurred in save function: {e}")

    logging.info(f"A total of {total_words} words were processed")    
    logging.info(f"Output file: {output_path}")
    


def thread_job(filename, num_threads):

    start_time = time.time()
    try:
        logging.info(f"Opening {filename}")
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

            #Send remaining line to the last thread to proccess it.
            if i == num_threads - 1:
                logging.info(f"Thread-{i + 1} will process data from {start} to {end} and an additional of {remaining_lines} remaining lines")
                end += remaining_lines

           
            t = threading.Thread(target=count_words, args=(thread_lines,))

            threads.append(t)

            #Print the thread that has started
            print(f'{t.name} started')
            
            t.start()

            logging.info(f"{t.name} to process data from {start} to {end} ")

        for t in threads:
            t.join()

    except Exception as e:
        logging.error(f"An error ocurred: {e}")

    file_pointer.close()
    logging.info(f"The file {input_file} was closed")    


if __name__ == '__main__':
    thread_job(input_file, num_threads)
    save(word_counter, output_file)



