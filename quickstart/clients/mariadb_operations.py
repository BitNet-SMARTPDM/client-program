# Module Imports
import mariadb


def connect_to_mariadb():
    # Connect to MariaDB Platform
    try:
        conn = mariadb.connect(
            user="root",
            password="pa55w0rd123",
            host="142.93.239.56",
            port=3306,
            database="mimosa_db"

        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return None

    return conn


def insert_mariadb_arrowhead(conn, table_name, json):
    if conn is None:
        conn = connect_to_mariadb()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO ' + table_name + '(Time, Power, Rotor_Speed, Nacelle_Position, Generator_Speed, '
                                              'Torque_Actual_Value_Percent, Torque_Set_Value_Percent, '
                                              'Tower_Acceleration_Normal, Tower_Acceleration_Lateral, '
                                              'Temp_Tower_Base, Temp_Ambient, Windspeed, Temp_GBX_Bearing, '
                                              'Temp_GBX_Bearing_Hollow_Shaft, Temp_GBX_OIL_1, Temp_GBX_OIL_2, '
                                              'Temp_GBX_T1_HSS, Temp_GBX_T3_HSS, Temp_GBX_T1_IMS, Temp_GBX_T3_IMS, '
                                              'Temp_GBX_Distr, Temp_GBX_OIL, Temp_Shaft_Bearing_1, '
                                              'Temp_Shaft_Bearing_2, Prox_Sensor_45, Prox_Sensor_135, '
                                              'Prox_Sensor_225, Prox_Sensor_315, Blade_2_Actual_Value, '
                                              'Blade_3_Actual_Value, Blade_1_Set_Value, Blade_1_Actual_Value, '
                                              'Resampled, Anomaly) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, '
                                              '?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (json['Time'], json['Power'], json['Rotor_Speed'], json['Nacelle_Position'], json['Generator_Speed'],
                 json['Torque_Actual_Value_Percent'], json['Torque_Set_Value_Percent'],
                 json['Tower_Acceleration_Normal'], json['Tower_Acceleration_Lateral'], json['Temp_Tower_Base'],
                 json['Temp_Ambient'], json['Windspeed'], json['Temp_GBX_Bearing'],
                 json['Temp_GBX_Bearing_Hollow_Shaft'], json['Temp_GBX_OIL_1'], json['Temp_GBX_OIL_2'], json['Temp_GBX_T1_HSS'],json['Temp_GBX_T3_HSS'],
                 json['Temp_GBX_T1_IMS'], json['Temp_GBX_T3_IMS'], json['Temp_GBX_Distr'], json['Temp_GBX_OIL'],
                 json['Temp_Shaft_Bearing_1'], json['Temp_Shaft_Bearing_2'], json['Prox_Sensor_45'],
                 json['Prox_Sensor_135'], json['Prox_Sensor_225'], json['Prox_Sensor_315'],
                 json['Blade_2_Actual_Value'], json['Blade_3_Actual_Value'], json['Blade_1_Set_Value'],
                 json['Blade_1_Actual_Value'], json['Resampled'], json['Anomaly']))

            conn.commit()
            conn.close()
        except Exception as e:
            if conn is not None:
               conn.close()
            print(f"Error: {e}")
