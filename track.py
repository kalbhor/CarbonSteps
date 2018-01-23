import math
import datetime


def get_distance(lat1, long1, lat2, long2):
    r = 6371
    latitude1 = math.radians(lat1)
    latitude2 = math.radians(lat2)
    long_distance = math.radians(long2 - long1)
    lat_distance = math.radians(lat2 - lat1)

    a = math.sin(lat_distance / 2)**2 + math.cos(latitude1) * \
        math.cos(latitude2) * (math.sin(long_distance / 2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    total_distance = r * c

    return total_distance


def check(json):

    results = {"walked": 0, "ran": 0, "drove": 0, "cycled": 0, "flew": 0}

    for i, location in enumerate(json["locations"]):
        if i == 0:
            prev_lat = location["latitudeE7"] / math.pow(10, 7)
            prev_lon = location["longitudeE7"] / math.pow(10, 7)
            timestamp = str(location["timestampMs"])[:-3]
            timestamp = int(timestamp)
            prev_date = datetime.datetime.utcfromtimestamp(
                timestamp).strftime("%d")
            prev_date = int(prev_date)
            continue

        timestamp = str(location["timestampMs"])[:-3]
        timestamp = int(timestamp)

        date = datetime.datetime.utcfromtimestamp(timestamp).strftime("%d")
        date = int(date)

        if date == prev_date - 1:
            print(prev_date, date)
            print(results)
            prev_date = date
            results = {"walked": 0, "ran": 0, "drove": 0, "flew": 0}

        lon = location["longitudeE7"] / math.pow(10, 7)
        lat = location["latitudeE7"] / math.pow(10, 7)

        current_distance = get_distance(prev_lat, prev_lon, lat, lon)

        if current_distance > 1000:
            results["flew"] += current_distance

        try:
            for a in location["activity"]:
                conf = [i["confidence"] for i in a["activity"]]
                conf = max(conf)
                for activity in a["activity"]:
                    if activity["type"] == "ON_FOOT" and activity["confidence"] >= 80:
                        results["walked"] += current_distance
                    if activity["type"] == "IN_VEHICLE" and activity["confidence"] >= 30:
                        results["drove"] += current_distance
                    # elif activity["type"] == "WALKING" and activity["confidence"] >= 40:
                    #	results["walked"] += current_distance
                    elif activity["type"] == "RUNNING" and activity["confidence"] >= 40:
                        results["ran"] += current_distance
                    elif activity["type"] == "ON_BICYCLE" and activity["confidence"] >= 20:
                        results["drove"] += current_distance
        except KeyError as e:
            continue

        if current_distance > 0:
            prev_lat = lat
            prev_lon = lon
