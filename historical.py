import datetime
import statistics
import requests
import json
import main_functions

def pricing_cleanup(num):
    gold = num // 10000
    silver = (num % 10000) // 100
    bronze = num % 100

    medal_strs = []
    if gold > 0:
        medal_strs.append("<span style='color:GoldenRod'>{0}G</span>".format(gold))
    if silver > 0:
        medal_strs.append("<span style='color:SlateGrey'>{0}S</span>".format(silver))
    if bronze > 0:
        medal_strs.append("<span style='color:Sienna'>{0}C</span>".format(bronze))

    return " ".join(medal_strs)

# grabs pricing data for single item
def get_historical_data(item_id):
    response = requests.get("https://api.datawars2.ie/gw2/v1/history?itemID={0}".format(item_id))
    # Returns data if success
    if response.status_code == 200:
        data = json.loads(response.content)
        return data
    else:
        print(f"Error: {response.status_code} - {response.reason}")

# gets basic data for single item
def get_item_data(item_id):
    response = requests.get("https://api.guildwars2.com/v2/items/{0}".format(item_id))
    # returns data if success
    if response.status_code == 200:
        data = json.loads(response.content)
        return data
    else:
        print(f"Error: {response.status_code} - {response.reason}")

def get_commerce_data(item_id):
    response = requests.get("https://api.guildwars2.com/v2/commerce/prices/{0}".format(item_id))
    # returns data if success
    if response.status_code == 200:
        data = json.loads(response.content)
        item_pricing = {
            "buys":pricing_cleanup(data["buys"]["unit_price"]),
            "sells":pricing_cleanup(data["sells"]["unit_price"])
        }
        return item_pricing
    else:
        print(f"Error: {response.status_code} - {response.reason}")

# cleans pricing and supply&demand data
def amalgamated_historical_data(item_id,duration):
    # Get the relevant dates and data
    today = datetime.date.today()
    thirty_days_ago = today - datetime.timedelta(days=duration)
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

    # Initialize the output object
    output = {
            "date": [],
            "average_buys": [],
            "high_buys": [],
            "low_buys": [],
            "average_sells": [],
            "high_sells": [],
            "low_sells": [],
            "average_buy_quantities": [],
            "max_buy_quantities": [],
            "min_buy_quantities": [],
            "average_sell_quantities": [],
            "max_sell_quantities": [],
            "min_sell_quantities": []
        }

    # Loop through each date in the combined_data dictionary
    for date in combined_data:
        # Calculate the averages, highs, and lows for the buy prices
        average_buys = round(sum(combined_data[date]["buys"]) / len(combined_data[date]["buys"]), 2)
        high_buys = max(combined_data[date]["buys"])
        low_buys = min(combined_data[date]["buys"])
        # Calculate the averages, highs, and lows for the sell prices
        average_sells = round(sum(combined_data[date]["sells"]) / len(combined_data[date]["sells"]), 2)
        high_sells = max(combined_data[date]["sells"])
        low_sells = min(combined_data[date]["sells"])
        # Calculate the averages, highs, and lows for the buy quantities
        average_buy_quantities = round(
            sum(combined_data[date]["buy_quantities"]) / len(combined_data[date]["buy_quantities"]), 2)
        max_buy_quantities = max(combined_data[date]["buy_quantities"])
        min_buy_quantities = min(combined_data[date]["buy_quantities"])
        # Calculate the averages, highs, and lows for the sell quantities
        average_sell_quantities = round(
            sum(combined_data[date]["sell_quantities"]) / len(combined_data[date]["sell_quantities"]), 2)
        max_sell_quantities = max(combined_data[date]["sell_quantities"])
        min_sell_quantities = min(combined_data[date]["sell_quantities"])

        # Create a new object with the calculated values and add it to the output object
        output["date"].append(str(date))
        output["average_buys"].append(average_buys)
        output["high_buys"].append(high_buys)
        output["low_buys"].append(low_buys)
        output["average_sells"].append(average_sells)
        output["high_sells"].append(high_sells)
        output["low_sells"].append(low_sells)
        output["average_buy_quantities"].append(average_buy_quantities)
        output["max_buy_quantities"].append(max_buy_quantities)
        output["min_buy_quantities"].append(min_buy_quantities)
        output["average_sell_quantities"].append(average_sell_quantities)
        output["max_sell_quantities"].append(max_sell_quantities)
        output["min_sell_quantities"].append(min_sell_quantities)

    return output