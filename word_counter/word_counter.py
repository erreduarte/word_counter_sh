import threading
from pathlib import Path
from collections import Counter
import re

input_file = "sample_file.txt"
num_threads = 10
counter_lock = threading.Lock()
word_counter = Counter()
output_file = f"{input_file[:-4]}_wordcount.txt"



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
        print(f"An error ocurred: {e}")   



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
        print(f"An error occurred in save function: {e}")


    print(f"A total of {total_words} words were processed")    
    print(f"File written to {output_path}")
    


def thread_job(filename, num_threads):

    try:

        with open(filename, 'rb') as file_pointer:
            lines = file_pointer.readlines()
            total_lines = len(lines)
            lines_per_thread = total_lines // num_threads
            
            print(f"The input file contains a total of {total_lines} lines") 
            print(f"{lines_per_thread=}")
        
        
        remaining_lines = total_lines % num_threads
        threads = []
        for i in range(num_threads):
            start = i * lines_per_thread
            end = start + lines_per_thread            

            thread_lines = lines[start:end]

            #Conditional to handle remaining lines.
            if i == num_threads - 1:
                print(f"Conditional 1: Thread {i + 1} will process data from {start} to {end} and an additional of {remaining_lines} remaining lines")
                end += remaining_lines

            thread_lines = lines[start:end]

           
            t = threading.Thread(target=count_words, args=(thread_lines,))
            threads.append(t)

            #Print the thread that has started
            print(f'{t.name} started')
            
            t.start()

            print(f"{t.name} to process data from {start} to {end} ")

        for t in threads:
            t.join()

    except Exception as e:
        print(f"An error ocurred: {e}")

    file_pointer.close()    


if __name__ == '__main__':
    thread_job(input_file, num_threads)
    save(word_counter, output_file)



