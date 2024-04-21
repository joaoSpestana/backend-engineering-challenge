# Data Engineering Challenge

## Description:
This code is designed to compute the moving average of a dataset containing translation delivery durations. The input dataset is expected to be in JSON format, where each line represents a valid JSON object with a timestamp and a duration.
<br> <br>

## Assumptions:
1. The input file is expected to be in JSON format, where each line represents a valid JSON object with a timestamp and a duration.
2. Each JSON object should contain the following fields:
   - `"timestamp"`: A valid datetime string in the format `"YYYY-MM-DD HH:MM:SS.ssssss"`.
   - `"duration"`: A valid integer representing the duration of translation delivery in seconds.
   - Other fields are present but not used for the moving average calculation
<br> <br>

## Implementation Options:
1. **Limit Date Argument:**
   - An optional third argument, `--limit_date`, allows filtering the oldest date for computing the moving average.
2. **Use of Pandas Package:**
   - Utilizes the pandas package for efficient data manipulation. The dataset is converted into a DataFrame, and the datetime column is set as the index for optimized filtering.
3. **Output File Saving:**
   - The script creates an "Outputs" directory on the desktop to save the output JSON file, ensuring organized output storage.
<br> <br>
  
## Implementation Options:
