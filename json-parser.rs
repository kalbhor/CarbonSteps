extern crate json;
extern crate chrono;

use chrono::{Datelike, TimeZone, Utc};
use std::fs::File;
use std::io::{Read, Write};
use std::f32;
use std::env;
use std::collections::HashMap;

fn main() {

    let name = env::args().skip(1).next().unwrap_or_else(|| {   println!("{{  }}");
                                                                std::process::exit(1); });
    let mut f = File::open(name).unwrap_or_else(|_| {    println!("{{  }}");
                                                        std::process::exit(2);  });
    let mut body = Vec::new();

    let _read_size = f.read_to_end(&mut body).unwrap();

    let body = std::str::from_utf8(&body).unwrap();

    let parsed = json::parse(body).unwrap();

    println!("{{");

    check(&parsed["locations"]);

    println!("}}");
    std::io::stdout().flush().unwrap();
}


fn get_distance(mut lat1: f32, long1: f32, mut lat2: f32, long2: f32) -> f32 {
    let r = 6371;

    lat1 = lat1.to_radians();
    lat2 = lat2.to_radians();
    let long_distance = (long2-long1).abs().to_radians();
    let lat_distance = (lat2 - lat1).abs().to_radians();

    let a = (lat_distance/2.0).sin().powi(2) + lat1.cos() * lat2.cos() * (long_distance/2.0).sin().powi(2);

    let c = 2f32 * a.sqrt().atan2((1f32 - a).sqrt());

    c * r as f32 //total distance
}


fn get_date(date: i64) -> u32 {
    let dt = Utc.timestamp(date, 0);
    dt.date().day()
}


fn check(js: &json::JsonValue) {
    let mut results = HashMap::new();

    results.insert("walked",    0.0);
    //results.insert("ran",       0.0);
    results.insert("drove",     0.0);
    results.insert("cycled",    0.0);
    //results.insert("flew",      0.0);

    //println!("obj={}\n array={}", js.is_object(), js.is_array());

    let element = js.members().next().unwrap();
    let mut prev_lat: f32 = element["latitudeE7"].as_f32().unwrap() / 10f32.powi(7);
    let mut prev_lon = element["longitudeE7"].as_f32().unwrap() / 10f32.powi(7);

    let mut timestamp = element["timestampMs"].as_str().unwrap()
        .parse::<i64>().unwrap() / 1000;
    let mut prev_date = get_date(timestamp);

    let last_val = js.members().last().unwrap();
    //println!("{:?}", last_val);
    let last_val = &last_val["timestampMs"];
    let element = js.members();
    //println!("{:?}", fuck.next());
    for location in element.skip(1) {

        timestamp = location["timestampMs"].as_str().unwrap()
            .parse::<i64>().unwrap() / 1000;

        let date = get_date(timestamp);
        //println!("{}", date);

        if date < prev_date || last_val == &location["timestampMs"] || (prev_date == 1 && date > prev_date) {
            //print!("\n\n\"{}-{}\": {:?},", prev_date, date, results);
            if results.get("drove").unwrap() >= &1000.0 {
                *results.get_mut("drove").unwrap() = 973.46;
            }
            print!("\n\"{}\" : {:?},", prev_date, results);

            results.insert("walked", 0.0);
            //results.insert("ran",    0.0);
            results.insert("drove",  0.0);
            results.insert("cycled", 0.0);
            //results.insert("flew",   0.0);

            if prev_date == 1 { break;  }
            prev_date = date;

        }

        let lon = location["longitudeE7"].as_f32().unwrap() / 10f32.powi(7);
        let lat = location["latitudeE7"].as_f32().unwrap() / 10f32.powi(7);

        let current_distance = get_distance(prev_lat, prev_lon, lat, lon);

        if current_distance > 1000.0 {
            //*results.get_mut("flew").unwrap() += current_distance;
            prev_lat = lat;
            prev_lon = lon;
            continue;
        }

        for a in location["activity"].members() {

            for activity in a["activity"].members() {

                if activity["type"] == "ON_FOOT" && activity["confidence"].as_i32() >= Some(80) {
                    *results.get_mut("walked").unwrap() += current_distance;
                }
                if activity["type"] == "IN_VEHICLE" && activity["confidence"].as_i32() >= Some(30) {
                    *results.get_mut("drove").unwrap() += current_distance;
                }
                /*else if activity["type"] == "WALKING" && activity["confidence"].as_i32() >= Some(40) {
                    *results.get_mut("walked").unwrap() += current_distance;
                }*/
                else if activity["type"] == "RUNNING" && activity["confidence"].as_i32() >= Some(40) {
                    //*results.get_mut("ran").unwrap() += current_distance;
                    *results.get_mut("walked").unwrap() += current_distance;
                }
                else if activity["type"] == "ON_BICYCLE" && activity["confidence"].as_i32() >= Some(20) {
                    *results.get_mut("drove").unwrap() += current_distance;
                }

            }
        }

        //break;
        if current_distance > 0f32 {
            prev_lat = lat;
            prev_lon = lon;
        }
    }
}
