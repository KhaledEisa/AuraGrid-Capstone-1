# AuraGrid Capstone: Renewable Grid Performance Monitoring System


## Project Overview
---

End-to-end Python application for processing sensor data from renewable energy sources, performing comprehensive time-series analysis, and generating automated visual reports for grid stability monitoring.

**Project Lead:** Khaled Eissa (Member 1)  
**Team:** AuraGrid Development Team (8 Members)  
**Date:** February 13, 2026

---

## Features

✅ **Object-Oriented Architecture** - Modular design with GridDataProcessor and ReportGenerator classes  
✅ **Robust Exception Handling** - Production-ready error handling for file I/O and data processing  
✅ **Time-Series Analysis** - Weekly aggregation and resampling using Pandas  
✅ **Static Visualizations** - Professional Matplotlib line plots for trend analysis  
✅ **Interactive Dashboards** - Plotly scatter plots with hover tooltips and filtering  
✅ **Automated Reporting** - Generates reports without manual intervention  

---

## Installation

### Prerequisites
- Python 3.x
- pip package manager

### Dependencies
```bash
pip install pandas numpy matplotlib plotly
```

Or install from requirements file:
```bash
pip install -r requirements.txt
```

---

## Project Structure

```
AuraGrid_Capstone/
├── grid_optimizer.py           # Main application (complete pipeline)
├── sensor_data.csv             # Input: Renewable energy sensor data
├── README.md                   # This file
├── requirements.txt            # Python dependencies
└── reports/                    # Output directory
    ├── weekly_output_trend.png     # Static: Weekly power trends (Matplotlib)
    └── efficiency_dashboard.html   # Interactive: Efficiency analysis (Plotly)
```

---

## Usage

### Quick Start
```bash
python grid_optimizer.py
```

The application will:
1. Load sensor data from `sensor_data.csv`
2. Clean and transform the data
3. Aggregate to weekly totals by source
4. Generate visualizations in the `reports/` directory

### Expected Output
```
✓ Total records processed: 34,785
✓ Unique energy sources: 12
✓ Analysis period: 2025-08-01 to 2025-11-30
✓ Total power output: 9,480,823.40 kWh

📁 Output Files:
  1. reports/weekly_output_trend.png
  2. reports/efficiency_dashboard.html
```

---

## Input Data Format

### sensor_data.csv
The input CSV file must contain the following columns:

| Column | Type | Description |
|--------|------|-------------|
| `Time` | datetime | Timestamp of sensor reading (YYYY-MM-DD HH:MM:SS) |
| `Source_ID` | string | Renewable energy source identifier (e.g., SRC_001) |
| `Power_Output` | float | Power generated in kWh |
| `Efficiency_Factor` | float | Efficiency rating (0.0-1.0) |

**Example:**
```csv
Time,Source_ID,Power_Output,Efficiency_Factor
2025-11-05 12:00:00,SRC_011,840.05,0.9307
2025-09-08 08:00:00,SRC_007,335.70,0.8666
2025-11-24 23:00:00,SRC_002,81.20,0.9044
```

---

## Output Reports

### 1. Weekly Output Trend (Matplotlib)
**File:** `reports/weekly_output_trend.png`

- **Type:** Static PNG image (300 DPI)
- **Content:** Line plot showing weekly total power output for top 5 sources
- **Features:**
  - Professional styling with color-coded sources
  - Grid lines for readability
  - Legend and axis labels
  - Time-series trend visualization

**Use Case:** Executive presentations, printed reports, documentation

---

### 2. Efficiency Dashboard (Plotly)
**File:** `reports/efficiency_dashboard.html`

- **Type:** Standalone interactive HTML
- **Content:** Scatter plot of Efficiency Factor vs Power Output
- **Features:**
  - Hover tooltips with detailed information
  - Color-coded by Source_ID
  - Interactive zoom and pan
  - Filter by source
  - Responsive design

**Use Case:** Web dashboards, interactive analysis, stakeholder presentations

---

## Class Architecture

### GridDataProcessor
Handles data ingestion, cleaning, transformation, and aggregation.

**Key Methods:**
- `read_data()` - Load CSV with exception handling
- `clean_data()` - Convert datetime and remove nulls
- `transform_data()` - Calculate efficiency ratios
- `aggregate_weekly_output()` - Weekly totals by source

**Exception Handling:**
- `FileNotFoundError` - Missing input file
- `IOError` - Corrupted or unreadable data
- `ValueError` - Invalid data format

---

### ReportGenerator
Generates static and interactive visualizations.

**Key Methods:**
- `generate_matplotlib_report()` - Static line plot (PNG)
- `generate_plotly_dashboard()` - Interactive scatter plot (HTML)

**Output:**
- Saves reports to `reports/` directory
- Configurable styling and formatting
- Production-ready quality

---

## Data Processing Pipeline

```
┌─────────────────────┐
│  1. Data Ingestion  │  Load sensor_data.csv
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  2. Data Cleaning   │  Convert datetime, remove nulls
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 3. Transformation   │  Calculate Efficiency_Ratio
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  4. Aggregation     │  Weekly totals by Source_ID
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 5. Visualization    │  Generate Matplotlib + Plotly
└─────────────────────┘
```

---

## Error Handling

The application includes comprehensive exception handling:

### File Errors
```python
✗ ERROR: File not found
  Path: sensor_data.csv
  Please ensure the file exists in the correct location.
```

### Data Errors
```python
✗ ERROR: Failed to parse CSV file
  Error details: Missing required columns: ['Time']
```

### Recovery
- Graceful error messages with actionable guidance
- Non-blocking warnings for data quality issues
- Automatic fallbacks for edge cases

---

## Performance Metrics

**Test Dataset:** 35,136 sensor records  
**Processing Time:** ~2-3 seconds  
**Memory Usage:** < 100 MB  
**Output Quality:**
- Matplotlib: 300 DPI PNG (publication quality)
- Plotly: Standalone HTML (no external dependencies)

---

## Code Quality

✅ **PEP 8 Compliant** - Follows Python style guidelines  
✅ **Comprehensive Docstrings** - All classes and methods documented  
✅ **Type Hints** - Clear parameter and return types  
✅ **Error Handling** - Robust exception management  
✅ **Modular Design** - Separation of concerns  
✅ **Production Ready** - Suitable for automated deployment  

---

## Testing

### Manual Testing
```bash
# Test with provided sample data
python grid_optimizer.py

# Test with custom data
python grid_optimizer.py --input your_data.csv
```

### Expected Behavior
- ✓ Application runs without manual intervention
- ✓ Handles missing files gracefully
- ✓ Processes null values correctly
- ✓ Generates both visualization outputs
- ✓ Creates reports/ directory if missing

---

## Troubleshooting

### Issue: Module not found
**Solution:**
```bash
pip install pandas numpy matplotlib plotly
```

### Issue: File not found error
**Solution:**
- Ensure `sensor_data.csv` is in the same directory as `grid_optimizer.py`
- Check file permissions
- Verify CSV format matches specification

### Issue: Empty reports
**Solution:**
- Verify input data has valid records
- Check for null values in required columns
- Ensure date format is correct (YYYY-MM-DD HH:MM:SS)

---

## Development Team

**Member 1 (Project Lead):** Khaled Eissa  
- Architecture design and class interfaces
- Main execution pipeline implementation
- Integration testing and validation
- Documentation and final submission

**Contributing Members:** 8-person development team  
- Data ingestion, cleaning, transformation
- Aggregation and time-series analysis
- Matplotlib and Plotly visualization specialists
- Documentation and testing leads

---

## Future Enhancements

🔮 **Potential Improvements:**
- Real-time data streaming support
- Machine learning predictions for power output
- Anomaly detection algorithms
- Multi-source comparative analytics
- Email/Slack notification integration
- RESTful API for web integration

---

## License

Internal use only - AuraGrid Grid Stability Team

---

## Contact

For support or questions, contact:
- **Project Lead:** Khaled Eissa
- **Team:** AuraGrid Development Team
- **Organization:** Grid Stability Team, Renewable Energy Division

---

## Acknowledgments

Special thanks to:
- Dr. Lena Sharma (Lead Data Scientist, Grid Stability Team)
- AuraGrid Development Team (8 contributors)
- Renewable Energy Sensor Network Team

---

## Version History

**v1.0.0** (February 13, 2026)
- Initial release
- Complete data processing pipeline
- Matplotlib and Plotly visualizations
- Comprehensive documentation

---

*Generated by AuraGrid Capstone Project Team - February 13, 2026*
