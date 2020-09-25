from cassandra.cluster import Cluster

cluster = Cluster()
session = cluster.connect('digilog_n')

'''
rows = session.execute('SELECT * FROM digilog_n.obd')
for row in rows:
    print(row)

user_lookup_stmt = session.prepare("SELECT * FROM users WHERE user_id=?")

INSERT INTO 

users = []
for user_id in user_ids_to_query:
    user = session.execute(user_lookup_stmt, [user_id])
    users.append(user)


session.execute(
    """
    INSERT INTO users (name, credits, user_id)
    VALUES (%s, %s, %s)
    """,
    ("John O'Reilly", 42, uuid.uuid1())
)
'''

class obd:
    def __init__(csv_path):
        self.csv_path = csv.path

    def load(self):
        with open(self.csv_path, 'r') as f:
            lines = f.readlines()
            lines = [x.strip().split(',') for x in lines]

            for line in lines:
                vehicle_id = line[6]
                ts_year = 1900
                ts_month = 1
                ts_day = 1
                air_intake_temp = int(line[17])
                ambient_air_temp = int(line[11])
                // automatic: three options 's', 'n', or null
                automatic = line[5]
                barometric_pressure_kpa = int(line[7])
                car_year = int(line[3])
                days_of_week = int(line[30])
                dtc_number = line[24]
                engine_coolant_temp = int(line[8])
                engine_load = float(line[10])
                engine_power = float(line[4])
                engine_rpm = int(line[12])
                engine_runtime = line[22]
                epoch_time = line[0]
                equiv_ratio = line[27]
                fuel_level = line[9]
                fuel_pressure = line[18]
                fuel_type = line[16]
                hours = line[29]
                intake_manifold_pressure = line[13]
                long_term_fuel_trim_bank_2 = line[15]
                maf = line[14]
                mark = line[1]
                min = line[28]
                model = line[2]
                months = line[31]
                p_class = line[33]
                short_term_fuel_trim_bank_1 = line[21]
                short_term_fuel_trim_bank_2 = line[20]
                speed = line[19]
                throttle_pos = line[23]
                timing_advance = line[26]
                trouble_codes = line[25]
                year = line[32]

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

