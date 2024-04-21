# Data Engineering Challenge

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
   - Uses the pandas package for efficient data manipulation. The dataset is converted into a DataFrame, and the datetime column is set as the index for optimized filtering.
3. **Output File Saving:**
   - The script creates an "Outputs" directory on the desktop to save the output JSON file, ensuring organized output storage.
<br> <br>

## Requirements:
   - Python 3.x
   - `pandas` library
<br> <br>

## Execution Guide:
To use the script, go to the script location and run it from the command line with the following arguments:
   - `--input_file`: Specifies the path for the input JSON file. By default, if only the filename is indicated, than the path is the Desktop folder.
   - `--window_size`: Specifies the size of the moving window in minutes for computing the moving average.
   - `--limit_date`: (Optional) Specifies the oldest date for computing the moving average. If not provided, the analysis starts from the earliest timestamp in the dataset.

This command will compute the moving average with a window size of 10 minutes for the entire dataset, using the input file located at the Desktop:
```
python Translation_Challenge.py --input_file input_file.json --window_size 10
```
This command will compute the moving average with a window size of 20 minutes for the timestamp from May 1, 2024, onwards, using the input file located at /path/to/input_file.json:
```
python Translation_Challenge.py --input_file /path/to/input_file.json --window_size 20 --limit_date 2024-05-01
```
