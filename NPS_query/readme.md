# NPS Calculation Query Performance Analysis

## Introduction
This README provides an analysis of two query approaches for calculating monthly Net Promoter Score (NPS) metrics in Google BigQuery. Based on discussions in the first interview regarding data performance and the use of nested queries versus Common Table Expressions (CTEs), I decided to run two queries for the same problem, one using a nested structure and the other using CTEs. The goal was to evaluate and compare their performance to determine the most efficient approach for this task.

## Analysis Overview
Both queries utilized the `CASE WHEN` statement to filter through columns and identify the scenarios of promoters and detractors. This approach helps in segmenting the data, allowing for a clear distinction between positive and negative feedback. By employing this logic, the analysis could accurately compute the NPS based on the defined criteria.

## Query Environment

To align with the platform requirements discussed in the first interview, I chose to execute and analyze both queries in Google BigQuery. This decision reflects the emphasis on using BigQuery for the job. You can review the saved queries here:

- **Query 1 (Nested)**: [View Query](Query1_Nested.sql)
- **Query 2 (CTEs)**: [View Query](Query2_CTE.sql)

This approach ensures consistency with the tools used in the job environment.


## Query Breakdown
The two approaches tested:
- **Query 1**: Uses a nested query structure, following the logic discussed in the interview.
- **Query 2**: Implements Common Table Expressions (CTEs), offering a more modular syntax but potentially impacting performance.

## General Performance Overview
Regardless of the approach, both queries indicate potential bottlenecks in the compute phase. In scenarios with large datasets, it would be beneficial to partition the table. My suggested partitioning would be based on the patient_id and date columns, as these are the most commonly used fields by analysts for daily analysis. Given that the NPS is evaluated bi-weekly, this partitioning would allow for improved parallelization and provide ready-to-use data. Additionally, pre-extracting data from the JSON column is important, as concurrency and on-demand JSON parsing can create significant overhead, impacting query performance and job stability.

## Performance Metrics


| Metric                  | Query 1 (Nested)| Query 2 (CTEs) |
|-------------------------|-----------------|----------------|
| Elapsed Time            | 181 ms          | 187 ms         |
| Slot Time Consumed      | 36 ms           | 41 ms          |
| Bytes Shuffled          | 144 B           | 144 B          |
| Bytes Spilled to Disk   | 0 B             | 0 B            |
| **Total Wait Time**     | 3 ms            | 3 ms           |
| **Total Read Time**     | 4 ms            | 3 ms           |
| **Total Write Time**    | 19 ms           | 18 ms          |
| **Total Compute Time**  | 19 ms           | 23 ms          |

## Analysis of Bottlenecks
- **Query 1**: This query took a total compute time of 19 ms, showing that it runs efficiently. The overall time of 181 ms indicates that it effectively uses resources, especially during the computing part.
- **Query 2**: The CTE approach, while making the query easier to read, adds a bit of extra time, resulting in a total compute time of 23 ms. This extra time is due to how CTEs handle temporary results. The overall time of 187 ms reflects this slight slowdown compared to the nested query.

## Conclusion
Although I generally prefer CTEs for their readability, the nested query (Query 1) performed better for the NPS calculation task. It finished faster and had a shorter compute time, making it the more efficient choice. 

This comparison highlights that while CTEs can improve clarity, the nested approach may be more suitable in situations requiring higher performance, particularly when dealing with large datasets. Striking a balance between query readability and performance is essential.
