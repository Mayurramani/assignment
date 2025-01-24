
# Quiz Performance Analysis

This Python script analyzes and compares quiz performance across two datasets: historical quiz data and current quiz data. The analysis includes calculating accuracy by topic and difficulty level, generating key insights, providing recommendations, and profiling the student’s strengths and weaknesses.

## Features
- Fetches data from two different quiz data sources (historical and current).
- Processes data using `pandas` DataFrames for easy manipulation.
- Compares historical and current performance by topic and difficulty.
- Generates insights about improvements, declines, and areas needing attention.
- Provides recommendations based on performance trends.
- Analyzes student persona to identify strengths, weaknesses, and behavior.

## Requirements
- Python 3.x
- `requests` (for fetching the data)
- `pandas` (for data manipulation)
- `numpy` (for calculations)

To install the required dependencies, run:
```bash
pip install requests pandas numpy
```

## Files
- `app.py`: The main Python script that performs the analysis and outputs results.

## How to Use
1. **Clone the repository or download the `app.py` file** to your local machine.
2. **Run the script** in your terminal using the command:
   ```bash
   python app.py
   ```
3. **View the results** in the terminal, which will include:
   - Comparison of historical vs. current quiz performance by topic and difficulty.
   - Key insights about improvements or declines in performance.
   - Recommendations based on the analysis.
   - Student persona analysis based on performance trends.

## Example Output

```
Historical vs Current Performance by Topic:

Historical vs Current Performance by Difficulty:

Key Insights:
Topics with improvement: 0
Topics with decline: 0
Difficulty levels with improvement: 0
Difficulty levels with decline: 0

Recommendations:
No major weaknesses detected. Keep up the good work!

Student Persona Analysis:
Strengths: 
Weaknesses: 
Labels: The Steady Student: No Major Improvements
Behavior: This student is performing steadily across all levels with no major weaknesses.
```

## Contribution
Feel free to contribute by:
- Reporting bugs or issues.
- Suggesting improvements or additional features.


