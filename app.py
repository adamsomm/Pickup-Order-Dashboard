from flask import Flask, render_template, redirect, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from order import PickupOrder
import csv
import os


app = Flask(__name__)

# Google Sheets setup
def get_google_sheet():
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)

    # Replace with your actual sheet name
    sheet = client.open("Lakelands Pickup Order Schedule").sheet1
    return sheet

def load_orders_from_sheet():
    sheet = get_google_sheet()
    data = sheet.get_all_values()

    headers = data[0]
    rows = data[1:]

    blacklist = get_blacklisted_ids()
    orders = []

    for idx, row_values in enumerate(rows, start=2):  # 1-based indexing for rows
        try:
            unique_id = row_values[0]#.strip()
            contact = row_values[2]
            company = row_values[1]
            titan_number = row_values[3]
            details = row_values[5]
            pickup_date = row_values[4]

            if contact and unique_id not in blacklist:
                order = PickupOrder(unique_id, contact, company, details, pickup_date, titan_number)
                order.excel_row = idx
                orders.append(order)
        except IndexError:
            continue  # skip malformed rows

    return orders


def get_blacklisted_ids():
    try:
        with open('blacklist.csv', mode='r', newline='') as file:
            reader = csv.reader(file)
            # Skip header if present
            rows = list(reader)
            if rows and rows[0][0].lower().strip() == 'orderid':
                rows = rows[1:]
            return {row[0].strip() for row in rows if row and row[0].strip()}
    except FileNotFoundError:
        return set()


if not os.path.exists('blacklist.csv'):
    with open('blacklist.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['OrderID'])


@app.route('/')
def dashboard():
    orders = load_orders_from_sheet()
    return render_template('dashboard.html', orders=orders)

@app.route('/update-orders', methods=['POST'])
def update_orders():
    remove_ids = request.form.getlist('remove_rows')
    remove_ids = [uid.strip() for uid in remove_ids if uid.strip()]

    if remove_ids:
        existing_blacklist = get_blacklisted_ids()
        new_ids = [uid for uid in remove_ids if uid not in existing_blacklist]

        if new_ids:
            with open('blacklist.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                for uniqueID in new_ids:
                    writer.writerow([uniqueID])

    return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)
