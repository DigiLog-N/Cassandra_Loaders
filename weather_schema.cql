// ***************************************************************************
// weather_schema.cql
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
USE digilog_n;

CREATE TABLE weather_live(
	station_id                      ascii,
	ct_timestamp                    double,
	date_time                       ascii,
	altimeter_set_1                 float,
	air_temp_set_1                  float,
	dew_point_temperature_set_1     float,
	relative_humidity_set_1         float,
	wind_speed_set_1                float,
	wind_direction_set_1            float,
	wind_gust_set_1                 float,
	sea_level_pressure_set_1        float,
	weather_cond_code_set_1         int,
	cloud_layer_3_code_set_1        double,
	pressure_tendency_set_1         double,
	precip_accum_one_hour_set_1     float,
	precip_accum_three_hour_set_1   float,
	cloud_layer_1_code_set_1        double,
	cloud_layer_2_code_set_1        double,
	precip_accum_six_hour_set_1     float,
	precip_accum_24_hour_set_1      float,
	visibility_set_1                float,
	metar_remark_set_1              ascii,
	metar_set_1                     ascii,
	air_temp_high_6_hour_set_1      float,
	air_temp_low_6_hour_set_1       float,
	peak_wind_speed_set_1           float,
	ceiling_set_1                   float,
	pressure_change_code_set_1      double,
	air_temp_high_24_hour_set_1     float,
	air_temp_low_24_hour_set_1      float,
	peak_wind_direction_set_1       float,
	dew_point_temperature_set_1d    float,
	cloud_layer_1_set_1d            double,
	cloud_layer_3_set_1d            double,
	cloud_layer_2_set_1d            double,
	wind_chill_set_1d               float,
	weather_summary_set_1d          ascii,
	wind_cardinal_direction_set_1d  ascii,
	pressure_set_1d                 float,
	sea_level_pressure_set_1d       float,
	heat_index_set_1d               float,
	weather_condition_set_1d        ascii,
	primary key ((station_id), ct_timestamp)
);
