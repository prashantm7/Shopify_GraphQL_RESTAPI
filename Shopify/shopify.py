import pandas as pd
import os
import requests
from datetime import datetime, timedelta
import pytz  # Make sure to install the `pytz` library

def main():
    token = ""
    shop = ""
    api_version = '2023-10'
    shop_url = f""

    # Calculate the start of the previous day (yesterday) from 12 am
    yesterday_time = (datetime.now().astimezone(pytz.utc) - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(hours=5, minutes=30)
    yesterday = yesterday_time.strftime('%Y-%m-%dT%H:%M:%S')

    # Set today to the current time
    today = datetime.now().astimezone(pytz.utc).isoformat()

    def get_data(object_name):
        # Function to get data from Shopify API
        endpoint = f"{shop_url}/{object_name}.json"
        headers = {
            "X-Shopify-Access-Token": token,
        }
        params = {
            'status': 'any',
            'created_at_min': yesterday,
            'created_at_max': today,
        }
        response = requests.get(endpoint, headers=headers, params=params)
        response_data = response.json().get(object_name, [])

        all_data = response_data

        while response.links.get('next'):
            next_url = response.links['next']['url']
            response = requests.get(next_url, headers=headers)
            response_data = response.json().get(object_name, [])
            all_data.extend(response_data)

        return all_data

    # Get Shopify orders data
    orders = get_data('orders')
    data = pd.json_normalize(orders) 

    # Extract relevant columns
    data_temp_1 = data[["name", "id", "created_at", "line_items"]]

    # Explode line_items column to handle multiple line items per order
    data_temp_2 = data_temp_1.explode("line_items").reset_index(drop=True)

    def flatten_json(nested_json, prefix='', exclude=[''], separator='_'):
        # Function to flatten nested JSON structure
        out = {}
        def flatten(x, name='', exclude=exclude):
            if type(x) is dict:
                for a in x:
                    if a not in exclude: flatten(x[a], name + a + separator)
            elif type(x) is list:
                i = 0
                for a in x:
                    flatten(a, name + str(i) + separator)
                    i += 1
            else:
                out[prefix + name[:-1]] = x

        flatten(nested_json)
        return out

    def expand_line_items(row):
        # Function to expand line_items column
        line_item_json = row['line_items']

        if line_item_json is not None:
            line_item_dict = flatten_json(line_item_json, 'line_item.')
        else:
            line_item_dict = {}

        return pd.Series({**line_item_dict})

    # Apply line item expansion function
    data_temp_3 = data_temp_2.apply(expand_line_items, axis=1)

    # Concatenate original and expanded line items data
    final_data = pd.concat([data_temp_2, data_temp_3], axis=1)

    # Display selected columns
    selected_columns = ["name", "id", "created_at", "line_item.name", "line_item.id"]
    print(final_data[selected_columns])

    # Save the DataFrame to a CSV file in the current working directory
    csv_filename = "shopify_data.csv"
    final_data.to_csv(csv_filename, index=False)
    print(f"Data saved to {csv_filename}")

if __name__ == "__main__":
    main()
