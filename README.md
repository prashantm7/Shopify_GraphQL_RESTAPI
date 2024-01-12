Shopify Data Extraction Script - Readme
Overview
The Shopify Data Extraction script facilitates the retrieval of order data from the Shopify API for a specific shop. It employs the requests library for API interaction and pandas for data manipulation. This script extracts essential information about orders, including order details and line items, storing the data in a structured CSV format.

Prerequisites
Before running the script, ensure the following libraries are installed:

bash
Copy code
pip install pandas requests pytz
Save to grepper
Configuration
Configure the following parameters in the script before execution:

token: Shopify API access token.
shop: Shopify store name.
api_version: Shopify API version.
shop_url: Shopify API endpoint for the specific shop.
Workflow
Calculate Time Window:

Determines the start of the previous day (yesterday) from 12 am in the UTC timezone.
Sets the end time to the current UTC time.
Get Data from Shopify API:

The get_data function sends a GET request to the Shopify API's Orders endpoint with the specified time window.
Retrieves paginated data, handling multiple pages if necessary.
Data Normalization:

Utilizes pd.json_normalize to flatten the nested JSON data returned from the Shopify API into a flat DataFrame.
Data Processing:

Selects relevant columns (name, id, created_at, line_items) from the DataFrame.
Explodes the line_items column to handle multiple line items per order.
Flatten Nested JSON:

Uses the flatten_json function to flatten the nested JSON structure within the line_items column.
Expand Line Items:

Applies the expand_line_items function to expand the line_items column, creating new columns for each line item attribute.
Concatenate DataFrames:

Concatenates the original and expanded line items DataFrames to create the final structured DataFrame.
Display Selected Columns:

Displays selected columns (name, id, created_at, line_item.name, line_item.id) from the final DataFrame.
Save to CSV:

Saves the final DataFrame to a CSV file named "shopify_data.csv" in the local directory.
Running the Script
To execute the script, run the Python file shopify.py using the correct Python interpreter path. Ensure the required libraries are installed.

bash
Copy code
python shopify.py
Save to grepper
The script will output information about the selected columns and save the data to a CSV file.

Notes
Ensure that the Shopify store credentials and API version are correctly configured.
Review the generated CSV file for the extracted data.
This documentation provides an overview of the script's functionality and usage. Refer to the inline comments in the code for more detailed explanations of each section.






