import datetime
import statistics
import requests
import json
import main_functions

def get_historical_data(item_id):

    response = requests.get("https://api.datawars2.ie/gw2/v1/history?itemID={0}".format(item_id))

    if response.status_code == 200:
        data = json.loads(response.content)
        return data
    else:
        print(f"Error: {response.status_code} - {response.reason}")

def amalgamated_historical_data(item_id):
    # Get the relevant dates and data
    today = datetime.date.today()
    thirty_days_ago = today - datetime.timedelta(days=30)
    combined_data = {}

    # Send request to the API and load the data from the response
    data = get_historical_data(item_id)

    # Loop through each item in the data array
    for item in data:
        item_date = datetime.datetime.fromisoformat(item["date"].replace("Z", "+00:00")).date()

        # If the item is within the last 30 days
        if item_date >= thirty_days_ago:
            # If there is no data for this date yet, initialize a new entry
            if item_date not in combined_data:
                combined_data[item_date] = {
                    "buys": [],
                    "sells": [],
                    "buy_quantities": [],
                    "sell_quantities": []
                }
            # Add the buy and sell prices and quantities to the corresponding arrays
            combined_data[item_date]["buys"].append(item["buy_price_max"])
            combined_data[item_date]["sells"].append(item["sell_price_min"])
            combined_data[item_date]["buy_quantities"].append(item["buy_quantity_max"])
            combined_data[item_date]["sell_quantities"].append(item["sell_quantity_min"])

    # Initialize the output array
    output = []

    # Loop through each date in the combined_data dictionary
    for date in combined_data:
        # Calculate the averages, highs, and lows for the buy and sell prices and quantities
        average_buys = round(sum(combined_data[date]["buys"]) / len(combined_data[date]["buys"]), 2)
        high_buys = max(combined_data[date]["buys"])
        low_buys = min(combined_data[date]["buys"])
        average_sells = round(sum(combined_data[date]["sells"]) / len(combined_data[date]["sells"]), 2)
        high_sells = max(combined_data[date]["sells"])
        low_sells = min(combined_data[date]["sells"])
        average_buy_quantities = round(
            sum(combined_data[date]["buy_quantities"]) / len(combined_data[date]["buy_quantities"]), 2)
        max_buy_quantities = max(combined_data[date]["buy_quantities"])
        min_buy_quantities = min(combined_data[date]["buy_quantities"])
        average_sell_quantities = round(
            sum(combined_data[date]["sell_quantities"]) / len(combined_data[date]["sell_quantities"]), 2)
        max_sell_quantities = max(combined_data[date]["sell_quantities"])
        min_sell_quantities = min(combined_data[date]["sell_quantities"])

        # Create a new object with the calculated values and add it to the output array
        output.append({
            "date": str(date),
            "average_buys": average_buys,
            "high_buys": high_buys,
            "low_buys": low_buys,
            "average_sells": average_sells,
            "high_sells": high_sells,
            "low_sells": low_sells,
            "average_buy_quantities": average_buy_quantities,
            "max_buy_quantities": max_buy_quantities,
            "min_buy_quantities": min_buy_quantities,
            "average_sell_quantities": average_sell_quantities,
            "max_sell_quantities": max_sell_quantities,
            "min_sell_quantities": min_sell_quantities
        })

    return output