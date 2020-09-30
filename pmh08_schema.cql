CREATE KEYSPACE digilog_n

//Use SimpleStrategy, at least to start with.
//It's standard practice to have a replication factor of 3.
//Because we are using a single-node cluster however, a write could fail if it
// needs to successfully write to three nodes before returning.
WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 1};
//Note: durable_writes (writing data to commitlog first) is true by default.

USE digilog_n;

DROP TABLE pmh08;

CREATE TABLE pmh08(
	//units are not named, only numbered
	unit int,
	//timestamps are not provided, only cycles (presumably take-off + flight + landing = one engine cycle)
	cycle int,
	op1 float,
	op2 float,
	op3 float,
	sensor01 float,
	sensor02 float,
	sensor03 float,
	sensor04 float,
	sensor05 float,
	sensor06 float,
	sensor07 float,
	sensor08 float,
	sensor09 float,
	sensor10 float,
	sensor11 float,
	sensor12 float,
	sensor13 float,
	sensor14 float,
	sensor15 float,
	sensor16 float,
	sensor17 float,
	sensor18 float,
	sensor19 float,
	sensor20 float,
	sensor21 float,
	primary key ((unit), cycle)
); 
//COPY DigiLogN.OBD (TIMESTAMP, MARK,MODEL,CAR_YEAR,ENGINE_POWER,AUTOMATIC,VEHICLE_ID,BAROMETRIC_PRESSURE_KPA,ENGINE_COOLANT_TEMP,FUEL_LEVEL,ENGINE_LOAD,AMBIENT_AIR_TEMP,ENGINE_RPM,INTAKE_MANIFOLD_PRESSURE,MAF,LONG_TERM_FUEL_TRIM_BANK_2,FUEL_TYPE,AIR_INTAKE_TEMP,FUEL_PRESSURE,SPEED,SHORT_TERM_FUEL_TRIM_BANK_2,SHORT_TERM_FUEL_TRIM_BANK_1,ENGINE_RUNTIME,THROTTLE_POS,DTC_NUMBER,TROUBLE_CODES,TIMING_ADVANCE,EQUIV_RATIO,MIN,HOURS,DAYS_OF_WEEK,MONTHS,YEAR,Class) FROM '/home/peter/git/Data/OBD/v2/dailyRoutes.csv' WITH DELIMITER=',' AND HEADER=TRUE AND NULL='';
