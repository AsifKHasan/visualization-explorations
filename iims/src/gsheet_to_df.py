import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def read_google_sheet_to_dataframe(spreadsheet_name, worksheet_name, header_row, data_range):
    """
    Reads data from a Google Sheet worksheet into a Pandas DataFrame.

    Args:
        spreadsheet_name (str): The name of the Google Sheet.
        worksheet_name (str): The name of the worksheet.
        header_row (str): The cell range of the header (e.g., 'B3:P3').
        data_range (str): The range of cells containing the data (e.g., 'B4:P').

    Returns:
        pandas.DataFrame: The data from the worksheet as a DataFrame, or None if an error occurs.
    """

    try:
        # Use credentials from a JSON file (downloaded from Google Cloud Console)
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('../conf/credential-celloscope-2024-160107.json', scope) # Replace 'your_credentials.json'
        client = gspread.authorize(creds)

        # Open the Google Sheet and worksheet
        sheet = client.open(spreadsheet_name).worksheet(worksheet_name)

        # Get header from the header range
        headers = sheet.get(header_row)[0] # get the values from the provided header range.

        # Get all values from the specified data range
        data = sheet.get(data_range)

        # Create DataFrame
        df = pd.DataFrame(data, columns=headers)
        return df

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage:
spreadsheet_name = 'IIMS__billing-and-collection'
worksheet_name = 'life'
header_row = 'B3:P3'  # Header is in range B3:P3
data_range = 'B4:P' #data starts at B4, and goes to P.

df = read_google_sheet_to_dataframe(spreadsheet_name, worksheet_name, header_row, data_range)

if df is not None:
    print(df.head())
    print(df.columns)
