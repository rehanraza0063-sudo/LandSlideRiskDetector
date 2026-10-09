# Landslide Risk Assessment System

A Python-based desktop application that demonstrates how environmental observations can be used to assess potential landslide risk. The system evaluates rainfall, slope angle, soil moisture, ground movement, and recent earthquake observations to generate a risk category and recommended precautions.

The application includes a graphical user interface, local database storage, assessment history, and CSV export functionality.

## Project Overview

Landslides can threaten lives, infrastructure, roads, and communities. Monitoring environmental conditions and recognizing potential warning signs are important parts of landslide risk management.

This project demonstrates a simple, data-driven workflow for recording site conditions, assigning an illustrative risk score, and organizing assessment records for further analysis.

**Note:** This is an educational prototype. Its scoring rules are illustrative and have not been scientifically validated for operational landslide prediction or public early-warning decisions.

## Features

* **Rainfall Assessment:** Evaluates rainfall recorded over the previous 24 hours.
* **Slope Analysis:** Considers the slope angle provided by the user.
* **Soil Moisture Monitoring:** Incorporates manually entered soil moisture percentages.
* **Ground Movement Classification:** Supports no observed movement, slow movement, and abrupt movement.
* **Earthquake Observation:** Allows the user to record a known recent earthquake.
* **Risk Categorization:** Assigns Low, Moderate, High, or Critical risk categories.
* **Warning Messages:** Displays recommended precautions based on the assessment.
* **Assessment History:** Saves previous assessments in a local SQLite database.
* **CSV Export:** Exports assessment records for further analysis.
* **Graphical User Interface:** Provides an interactive desktop dashboard built with Tkinter.

## Technologies Used

| Technology | Purpose                            |
| ---------- | ---------------------------------- |
| Python     | Application logic and risk scoring |
| Tkinter    | Desktop graphical user interface   |
| SQLite     | Local assessment-history storage   |
| CSV        | Exporting assessment records       |
| `datetime` | Recording assessment timestamps    |

The project uses Python's standard library and does not require third-party packages.

## Project Structure

```text
LandslideProject/
│
├── landslide_monitor.py
├── landslide_history.db   # Created automatically at runtime
└── README.md
```

The SQLite database is generated automatically when the application runs for the first time.

## Getting Started

### 1. Prerequisites

Install Python 3 on your computer.

Verify your installation:

```bash
python --version
```

On Windows, you can also run:

```powershell
py --version
```

### 2. Clone the Repository

Replace `YOUR_USERNAME` with your GitHub username.

```bash
git clone https://github.com/YOUR_USERNAME/Landslide-Risk-Assessment-System.git
```

Navigate to the project folder:

```bash
cd Landslide-Risk-Assessment-System
```

### 3. Run the Application

```bash
python landslide_monitor.py
```

Alternatively, on Windows:

```powershell
py landslide_monitor.py
```

A desktop window will open where you can enter environmental observations and generate an assessment.

## How to Use

1. Launch the application.
2. Enter a monitoring location or site identifier.
3. Enter rainfall in millimetres for the previous 24 hours.
4. Enter the slope angle in degrees.
5. Enter soil moisture as a percentage.
6. Select the observed ground movement category.
7. Select the earthquake observation.
8. Click **Assess Risk**.
9. Review the calculated score, risk category, and recommended precautions.
10. View saved assessments in the history table.
11. Click **Export CSV** to save the assessment history to a CSV file.

## Risk Assessment Logic

The application calculates an illustrative screening score from 0 to 100 using predefined point values.

| Parameter         | Maximum Points |
| ----------------- | -------------: |
| Rainfall          |             35 |
| Slope angle       |             20 |
| Soil moisture     |             25 |
| Ground movement   |             30 |
| Recent earthquake |             15 |

The combined points are capped at 100. Since the individual parameters can total more than 100, the displayed score is a simplified screening score rather than a calibrated probability of a landslide.

### Risk Categories

| Score / Condition        | Category |
| ------------------------ | -------- |
| Below 40                 | Low      |
| 40–64                    | Moderate |
| 65–100                   | High     |
| Abrupt movement reported | Critical |

Abrupt movement triggers the Critical category regardless of the calculated score.

These categories and thresholds are demonstration settings, not official warning levels. A low score does not establish that a slope is safe.

## Data Storage

Assessment records are stored locally using SQLite.

Each record includes:

* Timestamp
* Location or monitoring site ID
* Rainfall measurement
* Slope angle
* Soil moisture
* Ground movement observation
* Earthquake observation
* Screening score
* Risk category
* Recommended precautions

The CSV export feature allows the records to be opened in spreadsheet applications or used for exploratory data analysis.

## Future Improvements

Potential extensions include:

* Integration with live weather and rainfall data.
* IoT sensor integration for real-time ground movement and soil moisture readings.
* Visualization of historical rainfall and slope movement trends.
* Integration of satellite-based Synthetic Aperture Radar (SAR) data.
* Geographical maps showing monitoring locations.
* Machine-learning models trained and validated on suitable historical landslide datasets.
* Configurable alert thresholds based on regional research and expert guidance.
* Automated notifications for authorized monitoring teams.
* Evaluation using historical events, false-alarm rates, missed detections, and field observations.

## Applications

The project can serve as a starting point for exploring:

* Environmental data analysis
* Landslide monitoring workflows
* Disaster risk management concepts
* Python desktop application development
* Geospatial and remote-sensing research
* Data-driven decision-support systems

## Limitations and Safety

This project uses manually entered or simulated measurements and illustrative rules. It does not currently connect to live sensors, weather services, satellite data, or an operational emergency-warning network.

It has not been validated for predicting actual landslides. Do not use its score to make evacuation, access-control, or other safety-critical decisions. Follow official local warnings and guidance from qualified authorities.

## Author

**Rehan Raza Shaikh**

Biomedical Engineering Student | Data Analytics & AI/ML Enthusiast

* GitHub: [rehanraza0063-sudo](https://github.com/rehanraza0063-sudo)
* LinkedIn: [Rehan Raza Shaikh](https://www.linkedin.com/in/rehan-raza-shaikh-3869a7328/)

## License

This project is available for educational and research purposes. A formal open-source license can be added to the repository if redistribution or reuse is intended.
