## The Assignment

1. About once every two weeks, SWORD asks its patients how likely they are to recommend its therapy to someone they know on a scale from 0 to 10. Assume you have a table called **Scores** containing a JSON string that includes the satisfaction scores of SWORD’s patients along with the corresponding date, structured as follows:

| id | patient_id | scores                                        | date       |
|----|------------|-----------------------------------------------|------------|
| 1  | 1323       | {'satisfaction': 9, 'pain': 2, 'fatigue': 2}  | 2020-06-25 |
| 2  | 9032       | {'satisfaction': 2, 'pain': 7, 'fatigue': 5}  | 2020-06-30 |
| 3  | 2331       | {'satisfaction': 7, 'pain': 1, 'fatigue': 1}  | 2020-07-05 |
| 4  | 2303       | {'satisfaction': 8, 'pain': 9, 'fatigue': 0}  | 2020-07-12 |
| 5  | 1323       | {'satisfaction': 10, 'pain': 0, 'fatigue': 0} | 2020-07-09 |
| 6  | 2331       | {'satisfaction': 8, 'pain': 9, 'fatigue': 5}  | 2020-07-20 |

   One of our most important metrics is the **Net Promoter Score (NPS)**, which is calculated using the following formula:

   [number of promoters - number of detractors / number of patients]

   Patients are classified into the following groups based on their most recent satisfaction report:
   - **Promoter**: satisfaction score > 8
   - **Detractor**: satisfaction score < 7

   
   Write a SQL query to calculate SWORD’s Digital Therapist NPS for each month. For example:

   | Month    | NPS |
   |----------|-----|
   | January  | 50  |
   | February | 45  |
   | March    | 53  |
   | ...      | ... |

2. Write a Python program that takes as input the name of a `.txt` file and creates another file that contains the number of occurrences of each word in the original file, sorted in descending order. For example:

the 563
of 431
to 320
it 210
that 109
...

Your program should distribute the computation by having 10 worker threads simultaneously building the resulting list


