from prometheus_client import start_http_server, Gauge
import serial
import time

# Create metric object for the co2 level
co2_gauge = Gauge('co2_level_ppm', 'CO2 value')

def read_co2(serial_port):
    ser = serial.Serial(serial_port, baudrate=9600, timeout=2)
    time.sleep(2)  # Sleep time to allow sensor to start up properly

    ser.flushInput()
    ser.write(b"\xff\x01\x86\x00\x00\x00\x00\x00\x79")  # Command to read the CO2 value
    response = ser.read(9)
    if len(response) == 9 and response[0] == 0xff and response[1] == 0x86:
        high = response[2]
        low = response[3]
        co2 = (high << 8) + low
        return co2
    else:
        return None

if __name__ == "__main__":
    # Start a HTTP server to expose the Prometheus metrics
    start_http_server(8000)

    serial_port = "/dev/serial0"  # Or "/dev/ttyS0" depending on the Raspberry Pi version

    try:
        while True:
            co2_value = read_co2(serial_port)
            if co2_value is not None:
                co2_gauge.set(co2_value)  # Update the CO2 metrics
                print("CO2 value:", co2_value, "ppm")
            else:
                print("Unable to read CO2 value. Make sure sensor is correctly connected.")
            time.sleep(60)  # Wait a minute before scraping again
    except KeyboardInterrupt:
        print("Program stop.")