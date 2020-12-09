// ***************************************************************************
// obd_schema.cql
// https://github.com/DigiLog-N/DigiLog-N
// Copyright 2020 Canvass Labs, Inc.
// 
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
// 
// http://www.apache.org/licenses/LICENSE-2.0
// 
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
// ***************************************************************************
CREATE KEYSPACE digilog_n
//Use SimpleStrategy, at least to start with.
//It's standard practice to have a replication factor of 3.
//Because we are using a single-node cluster however, a write could fail if it
// needs to successfully write to three nodes before returning.
WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 1};
//Note: durable_writes (writing data to commitlog first) is true by default.

USE digilog_n;

DROP TABLE obd;

CREATE TABLE obd(
      vehicle_id text,
      // in order to use year, month and day as clustering columns,
      //  we need to derive ts_year, ts_month, and ts_day from
      //  the epoch timestamp. if ts_year and ts_month can be shown
      //  to be equivalent always to year and months, then we're good.
      //  however, we would still need to determine the day of the month,
      //  as the day of the week isn't equivalent to the day of the month.
      // we can preserve the epoch timestamp as is, or just the number of
      //  seconds since the day started, or just convert to the time.
      ts_year int,
      ts_month int,
      ts_day int,
      air_intake_temp int,
      ambient_air_temp int,
      // automatic: three options 's', 'n', or null
      automatic ascii,
      barometric_pressure_kpa int,
      car_year int,
      // could be boolean if it was acceptable to map 0 to false and 1 to true.
      // ascii is perhaps cheaper to capture 1 and 0 than utf-8 text string.
      class ascii,
      days_of_week int,
      dtc_number text,
      engine_coolant_temp int,
      engine_load float,
      engine_power float,
      engine_rpm int,
      // could be converted to elapsed time in seconds or hours minutes seconds
      engine_runtime text,
      equiv_ratio float,
      fuel_level float,
      fuel_pressure int,
      fuel_type text,
      hours int,
      intake_manifold_pressure int,
      long_term_fuel_trim_bank_2 float,
      maf float,
      mark text,
      min int,
      model text,
      months int,
      short_term_fuel_trim_bank_1 float,
      short_term_fuel_trim_bank_2 float,
      speed int,
      throttle_pos float,
      timestamp bigint,
      timing_advance float,
      trouble_codes text,
      // vehicle_id should be key as well
      year int,
      //standard practice for time-series data would be to use vehicle_id
      // itself as the primary key, and use year, month, and day components
      // of the timestamp to be clustering columns.
      primary key ((vehicle_id), ts_year, ts_month, ts_day)
); 

//COPY DigiLogN.OBD (TIMESTAMP, MARK,MODEL,CAR_YEAR,ENGINE_POWER,AUTOMATIC,VEHICLE_ID,BAROMETRIC_PRESSURE_KPA,ENGINE_COOLANT_TEMP,FUEL_LEVEL,ENGINE_LOAD,AMBIENT_AIR_TEMP,ENGINE_RPM,INTAKE_MANIFOLD_PRESSURE,MAF,LONG_TERM_FUEL_TRIM_BANK_2,FUEL_TYPE,AIR_INTAKE_TEMP,FUEL_PRESSURE,SPEED,SHORT_TERM_FUEL_TRIM_BANK_2,SHORT_TERM_FUEL_TRIM_BANK_1,ENGINE_RUNTIME,THROTTLE_POS,DTC_NUMBER,TROUBLE_CODES,TIMING_ADVANCE,EQUIV_RATIO,MIN,HOURS,DAYS_OF_WEEK,MONTHS,YEAR,Class) FROM '/home/peter/git/Data/OBD/v2/dailyRoutes.csv' WITH DELIMITER=',' AND HEADER=TRUE AND NULL='';


