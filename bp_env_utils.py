from dotenv import load_dotenv
import os

def edit_env_file(env_file, variable_name, new_value):
    new_value_str = '"'+str(new_value)+'"'
    # Open the .env file in read mode
    with open(env_file, "r") as f:
        lines = f.readlines()

    # Update the value in the lines
    updated_lines = []
    for line in lines:
        line = line.strip()
        if line and "=" in line:
            key, value = line.split("=", 1)
            if key == variable_name:
                line = f"{key}={new_value_str}"
        updated_lines.append(line)

    # Write the updated lines back to the .env file
    with open(env_file, "w") as f:
        f.write("\n".join(updated_lines))
        
def return_env_variables():
    load_dotenv()
    
    bucket = os.environ['INFLUX_BUCKET'] 
    org = os.environ['INFLUX_ORG']
    token = os.environ['INFLUX_TOKEN']
    url = os.environ['INFLUX_URL'] + ":8086"
    rpi_id = os.environ['RPI_ID']
    
    return bucket, org, token, url, rpi_id