import argparse
import os
import sys
import pandas as pd


"""
Parses command line arguments to retrieve input file path, window size, and optional limit date.

Returns:
    tuple: A tuple containing input file path, window size, and limit date.
"""
def get_parameters():
    parser = argparse.ArgumentParser(description='Script command line')
    parser.add_argument("--input_file")
    parser.add_argument("--window_size")
    parser.add_argument("--limit_date", default=-1)

    args = parser.parse_args()
    limit_datetime= -1

    try:
        time_window =int(args.window_size)
        if args.limit_date != -1:
            limit_datetime = pd.to_datetime(args.limit_date)
    except ValueError:
        sys.exit("Invalid inputs. Please confirm if the window_size or the limit_date are valid.")

    #Verifies if the input_file argument is a path or simply a filename
    if '\\' in args.input_file or '/' in args.input_file:
        return args.input_file, time_window, limit_datetime
    else:
        #In case it is a filename the default path is the Desktop
        path = os.path.join(os.path.expanduser('~'), 'Desktop') + '\\' + args.input_file
        return path, time_window, limit_datetime


"""
Reads JSON file into a DataFrame and sets the timestamp column as the index.

Args:
    filepath (str): Path to the JSON file.

Returns:
    pandas.DataFrame: DataFrame with timestamp as index.
"""
def read_file(filepath):
    try:
        data = pd.read_json(filepath, lines=True)

        data['timestamp'] = pd.to_datetime(data['timestamp'])

        return data.set_index('timestamp')
    except FileNotFoundError:
        sys.exit("File not found. Please confirm that the path is correct")


"""
Computes the moving average of a DataFrame within a specified time window.

Args:
    data_events (pandas.DataFrame): DataFrame containing timestamp-indexed data.
    window_size (int): Size of the moving window in minutes.
    start_datetime (pandas.Timestamp): Start of the time interval.
    end_datetime (pandas.Timestamp): End of the time interval.

Returns:
    pandas.DataFrame: DataFrame containing moving average data for each datetime.
"""
def compute_moving_average(data_events, window_size, start_datetime, end_datetime):

    step = pd.Timedelta(minutes=1)
    current_datetime = start_datetime

    moving_avg_data = []

    while current_datetime <= end_datetime:
        #Get the events within the desired time window
        window_data = data_events.loc[(data_events.index >= current_datetime - pd.Timedelta(minutes=window_size)) &
                                      (data_events.index <= current_datetime)]

        # Compute the moving average for this minute
        moving_avg = round(window_data['duration'].mean(), 1)

        # Append the result to a list
        moving_avg_data.append([str(current_datetime), moving_avg, window_size])

        current_datetime += step

    return pd.DataFrame(moving_avg_data, columns=['date', 'average_delivery_time', 'window_size']).fillna(0)


"""
Generates final output by print the DataFrame to the console and writing it to a JSON file.

Args:
    data_events (pandas.DataFrame): DataFrame containing final output data.
    datetime (pandas.Timestamp): End datetime of the analysis.
    time_window (int): Size of the moving window used.

Returns:
    None
"""
def generate_final_output(data_events, datetime, time_window):
    string_time = str(datetime).split()[0].replace("-", "")
    path_directory = os.path.join(os.path.expanduser('~'), 'Desktop', 'Outputs')

    os.makedirs(path_directory, exist_ok=True)

    json_output = data_events.to_json(orient='records', lines=True)

    print("The Output is:")
    print(json_output)

    #The name of the output file is: events_LastDate_TimeWindow.json
    path_output = path_directory + '\\events_' +  string_time + "_" + str(time_window) + ".json"

    with open(path_output, "w") as json_file:
        json_file.write(json_output)


"""
  Main entry point of the script.

  Parses command line arguments, reads input file, computes moving average, 
  generates final output, and writes it to a JSON file.
"""
if __name__ == "__main__":
    file_path, time_window, limit_datetime = get_parameters()

    file_events = read_file(file_path)

    end_datetime = file_events.index[-1].replace(second=0) + pd.Timedelta(minutes=1)

    if(limit_datetime == -1):
        start_datime = file_events.index[0].replace(second=0)
    else:
        start_datime = limit_datetime

    events_moving_average = compute_moving_average(file_events, time_window, start_datime, end_datetime)
    generate_final_output(events_moving_average, end_datetime, time_window)

