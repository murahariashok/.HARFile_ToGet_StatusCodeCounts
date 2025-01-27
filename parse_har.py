import json

har_file = "exactspace.har"
def parse_har_file(har_file):
    with open(har_file, "r") as har_file:
        har_data = json.load(har_file)

        # Extract all entries
    entries = har_data.get("log", {}).get("entries", [])
    # Initialize counters
    total_count = 0
    status_2xx = 0
    status_4xx = 0
    status_5xx = 0

    # Count status codes
    for entry in entries:
        if entry.get("method") == "Network.responseReceivedExtraInfo":
            status_code = entry.get("params", {}).get("statusCode")
            total_count += 1
            if 200 <= status_code < 300:
                status_2xx += 1
            elif 400 <= status_code < 500:
                status_4xx += 1
            elif 500 <= status_code < 600:
                status_5xx += 1
    return total_count, status_2xx, status_4xx, status_5xx

# Parse the generated HAR file
total_count, count_2xx, count_4xx, count_5xx = parse_har_file(har_file)

# Output the results
output = {
    "Total Status Code Count": total_count,
    "2XX Status Codes Count": count_2xx,
    "4XX Status Codes Count": count_4xx,
    "5XX Status Codes Count": count_5xx,
}

# Save the output to a .txt file
output_file = "status_code_counts.txt"
try:
    with open(output_file, 'w') as file:
        for key, value in output.items():
            file.write(f"{key}: {value}\n")
    print(f"Results have been saved to {output_file}.")
except Exception as e:
    print(f"Error saving output: {e}")



# Ensure the HAR file is in the same directory
parse_har_file(har_file)