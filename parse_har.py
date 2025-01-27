import json

def parse_har_file(har_file_path):
    with open(har_file_path, "r") as har_file:
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

    print(f"Total status code count: {total_count}")
    print(f"Total count for 2XX status codes: {status_2xx}")
    print(f"Total count for 4XX status codes: {status_4xx}")
    print(f"Total count for 5XX status codes: {status_5xx}")

if __name__ == "__main__":
    har_file_path = "exactspace.har"  # Ensure the HAR file is in the same directory
    parse_har_file(har_file_path)
