import csv
import time

with open('drifter.csv', 'rt') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    set = []
    i = -1

    # Turn csv in to list or dictionary chunks
    for row in reader:
        if row[0] and "0-" not in row[0]:
            set.append([])
            i += 1
	    headers = row
        else:
            set[i].append(dict(zip(headers, row)))

    trials = {}
    trials_time = {}
    trials_count = {}
    for clump in set:
        for record in clump:
            # Filter out the keepalive pings
            if "Alarm3Mode" in record:
                break;
            try:
                esn = record["ESN"]
                if esn not in trials:
                    trials[esn] = []
                if esn not in trials_time:
                    trials_time[esn] = 0
                if esn not in trials_count:
                    trials_count[esn] = 0
                current_timestamp = time.mktime(time.strptime(record["Message Time US East Coast (EDT)"], '%m/%d/%y %H:%M'))
                if abs(current_timestamp - trials_time[esn]) > 10800:
                    trials_count[esn] += 1
                trials_time[esn] = current_timestamp
                trials[esn].append([
                    trials_count[esn],
                    esn,
                    record["Unit Name"],
                    record["Latitude"],
                    record["Longitude"],
                    current_timestamp,
                ])
            except (KeyError, ValueError) as e:
                print(e)
                print(record)
print(trials)
