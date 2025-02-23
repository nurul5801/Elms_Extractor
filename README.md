# ELMS Extractor

This Python script scrapes participant names and email addresses from UIU ELMS courses, allowing users to extract data efficiently for email extraction purposes.

## Features
- Scrape all enrolled courses or a specific course by ID.
- Generates two output files per course:
  1. **CSV File** – Contains participant names and emails.
  2. **Text File** – Contains only email addresses.
- Eliminates duplicate email entries automatically.
- Organizes course names in a standardized format.
- Saves extracted data for easy access and further processing.

## Installation
1. Install the required dependencies:
   ```bash
   pip install requests beautifulsoup4 csv json
   ```
2. Run the script:
   ```bash
   python elms_extractor.py
   ```

## Usage
1. Ensure you have access to UIU ELMS and update the script with your session details.
2. Run the script, and it will automatically extract participant data from the selected courses.
3. The extracted data will be saved as CSV and text files for easy reference.

## Output Files
- **`course_code_users.csv`**: Contains participant names and emails.
- **`course_code_emails.txt`**: Contains email addresses only, one per line.

## Notes
- The script removes duplicate email entries to ensure clean data extraction.
- Requires an active internet connection to fetch data from UIU ELMS.
- The extracted data can be used for academic communication, attendance management, or other administrative purposes.

## Example Output
### Console Output:
```
Name: John Doe, Email: john.doe@example.com
Name: Jane Smith, Email: jane.smith@example.com

Total Emails Found: 2
CSV file 'CSE_323_users.csv' saved successfully.
Email list file 'CSE_323_emails.txt' saved successfully.
```

### CSV File (`CSE_323_users.csv`):
| Name        | Email                  |
|------------|------------------------|
| John Doe   | john.doe@example.com   |
| Jane Smith | jane.smith@example.com |

### Text File (`CSE_323_emails.txt`):
```
john.doe@example.com
jane.smith@example.com
```

## License
This script is for educational purposes only. Use it responsibly.

