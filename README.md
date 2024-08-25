# Skyscanner Flight Data Extraction

This project is a Python-based application that extracts flight prices and schedules from the Skyscanner API. The input is provided via a text file containing details such as the origin, destination, and travel dates. The application processes this input, retrieves the relevant data from Skyscanner, and then saves the output in CSV format.

## Project Structure

```plaintext
skyscanner-flight-extraction/
│
├── data/
│   └── input.txt             # Input file containing flight details
│
├── scripts/
│   ├── file_utils.py         # Utility functions for handling files
│   ├── skyscanner_api.py     # Module for interacting with the Skyscanner API
│   └── main.py               # Main script to execute the ETL process
│
├── Dockerfile                # Dockerfile for containerizing the application
├── README.md                 # Project documentation
└── requirements.txt          # Python dependencies
```
## Features

- Extracts flight prices and schedules based on user input from a text file.
- Utilizes the Skyscanner API to fetch real-time data.
- Saves the output data into CSV files for easy analysis and further processing.

## Prerequisites

To run this project, you'll need to have the following installed:

- Python 3.x
- Pip (Python package installer)

## Setup Instructions

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/skyscanner-flight-extraction.git
   cd skyscanner-flight-extraction
   ```

2. **Install Dependencies:**
   
  Install the required Python packages listed in requirements.txt:
  ```bash
  pip install -r requirements.txt
  ```

3. **Set Up the Input File:**
   
  Edit the data/input.txt file to include the flight details. The format is as follows:
  ```init
  [FLIGHT 1]
  origin_country=PT
  dest_country=UK
  origin_airport=Porto
  dest_airport=London
  origin_date=2024-12-28
  dest_date=2025-01-04
  
  [FLIGHT 2]
  origin_country=PT
  dest_country=UK
  origin_airport=Porto
  dest_airport=London
  origin_date=2024-12-28
  dest_date=2024-01-05
  ```
  You can add multiple flights by copying the structure used for [FLIGHT 1].

4. **Run the Script:**
   Execute the main script to extract data from the Skyscanner API based on the input file:
   ```bash
   python scripts/main.py
   ```

5. **Check the Output:**
After running the script, the output data will be saved into CSV files in the data/ directory:

- prices.csv: Contains the flight prices.
- schedules.csv: Contains the flight schedules.

# Using Docker (Optional)
If you prefer to run the application in a Docker container, follow these steps:
1. Build the Docker Image:
   ```bash
   docker build -t skyscanner-flight-extraction .
   ```
   
2. Run the Docker Container:
   ```bash
   docker run -v $(pwd)/data:/app/data skyscanner-flight-extraction
   ```

## Dependencies
The project relies on the following Python packages:
```plaintext
requests
pandas
```
These are listed in the requirements.txt file.

## Future Enhancements
- Add support for additional input parameters such as cabin class, number of passengers, etc.
- Improve error handling and logging.
- Integrate more comprehensive data validation for the input file.

## License
This project is licensed under the MIT License.

## Contact
If you have any questions or suggestions, feel free to open an issue or reach out to the project maintainer.
