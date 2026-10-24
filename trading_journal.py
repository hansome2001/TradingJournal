"""
AUTHOR:Hansome Anthony 

PURPOSE:The program will help traders record and track their trades and calculate 
their profit or loss over time. It will make it easier for traders to review their 
trading results and understand their performance.

"""

import csv
from datetime import datetime
import os 
#import os # checks if the file trades.csv already exists
def save_trade(
        trade_date, 
        asset, 
        direction,
        entry_price, exit_price, leverage, margin_amount
    ):
    #save the users trade to the csv file
    if direction.lower() == "buy/long":
        price_change = exit_price - entry_price
    elif direction.lower() == "sell/short":
        price_change = entry_price - exit_price
    else:
        raise ValueError("Invalid direction. Please enter BUY/LONG or SELL/SHORT")
#calculating for percentage change
    if entry_price<=0:
        print("Entry price must be greater than zero.")
        return
    if exit_price<=0:
        print("Exit price must be greater than zero.")
        return 
    if leverage <=0: 
        print("Levarage must be greater than zero.")
        return
    if margin_amount<=0:
        print("Margin amount must be greater than zero.")
        return
#calculating the estimate profit or loss
    price_change_percentage = price_change / entry_price * 100
    profit_loss = (price_change_percentage / 100) * leverage * margin_amount 
#now dealing with CSV file 
    file_exists = os.path.isfile("trades.csv") #to check if the csv file exits
  
    with open("trades.csv", "a", newline ="") as file:
        writer = csv.writer(file)
        if not file_exists:
           writer.writerow(["trade_date","Asset","Direction","Entry Price","Exit Price","Leverage","Margin Amount","Profit/Loss"])
        writer.writerow([trade_date,
                        asset,
                        direction, 
                        entry_price, 
                        exit_price, 
                        leverage, 
                        margin_amount, 
                        profit_loss])
    #calculating all trades from csv     
def calculate_total_profit_loss():
    total_profit_loss = 0.0
    with open("trades.csv", "r") as file:
        reader = csv.reader(file)
        next(reader, None) 
        for row in reader:
            if not row:
                continue
            if len(row)<8:
                print(f"Skipping incomplete row: {row}")
                continue
            total_profit_loss += float(row[7]) 
    return total_profit_loss
def calculate_total_profit(): #calculates the total profit from multiple trades
    total_profit = 0.0
    with open("trades.csv", "r") as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            if not row:
                continue
            if len(row)<8:
                print(f"Skipping incomplete row: {row}")
                continue
            profit_loss = float(row[7])
            if profit_loss > 0:
                total_profit += profit_loss
    return total_profit 

def calculate_total_loss():  #calculates the total losses from multiple trades
    total_loss = 0.0
    with open("trades.csv", "r") as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            if not row:
                continue
            if  len(row) < 8:
                print(f"skipping incomplete row: {row}")
                continue 
            profit_loss = float(row[7]) 
            if profit_loss < 0:
                total_loss += abs(profit_loss) 
    return total_loss

def calculate_win_rate(): #calculates the percentage of profitable trades
    win_rate = 0.0
    total_trades = 0.0
    winning_trades = 0.0

    with open("trades.csv", "r") as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            if not row:
                continue
            if len(row) < 8:
                continue
            total_trades += 1
            profit_loss = float(row[7])
            if profit_loss > 0:
                 winning_trades += 1
    if total_trades > 0:
       win_rate = (winning_trades/total_trades)*100
    return win_rate 

def read_trades(): #reads the saved trading record
    trades = []
    with open("trades.csv", "r") as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            if not row:
                continue
            if len(row) < 8:
                continue
            trades.append(row)             
    return trades

def calculate_trade_statistics(): #calculates basic statistics from the trading records
    trades = read_trades()
    total_trades = len(trades)
    winning_trades = 0
    losing_trades = 0
    breakeven_trades = 0

    for trade in trades:
        profit_loss = float(trade[7])
        if profit_loss > 0:
            winning_trades += 1
        elif profit_loss < 0:
            losing_trades += 1
        else:
            breakeven_trades += 1
    return {
        "total_trades": total_trades, 
        "winning_trades": winning_trades,
        "losing_trades": losing_trades,
        "breakeven_trades": breakeven_trades
    }


    
def display_summary(): #displays the trading results and summary to the user
    total_profit = calculate_total_profit()
    total_loss = calculate_total_loss()
    total_profit_loss = calculate_total_profit_loss()
    win_rate = calculate_win_rate()
    statistics = calculate_trade_statistics()

    print("\n========== TRADING JOURNAL SUMMARY ==========")
    print(f"Total trades: {statistics['total_trades']}")
    print(f"Winning trades: {statistics['winning_trades']}")
    print(f"Losing trades: {statistics['losing_trades']}")
    print(f"Breakeven trades: {statistics['breakeven_trades']}")
    print(f"Win rate: {win_rate:.2f}%")
    print(f"Total estimated profit: ${total_profit:.2f}")
    print(f"Total estimated loss: ${total_loss:.2f}")

    if total_profit_loss > 0:
        print(f"Net estimated profit: +${total_profit_loss:.2f}")
    elif total_profit_loss < 0:
        print(f"Net estimated loss: -${abs(total_profit_loss):.2f}")
    else:
        print("Net estimated profit/loss: $0.00")

    print("=============================================")

def main():
    try:
        trade_date = datetime.strptime(input("Enter trade date (DD-MM-YYYY): "),"%d-%m-%Y").date()
    except ValueError:
        print("Invalid date. please use DD-MM-YYYY format ")
        return 
    asset = input("Enter assest (e.g BTCUSDT): ")
    direction = input("Enter direction (BUY/LONG OR SELL/SHORT): ")
    try:
       entry_price = float(input("Enter entry price: "))
       if entry_price <= 0:
               print("Entry price must be greater than Zero.")
               return
       exit_price = float(input("Enter exit price: ")) 
       leverage = int(input("Enter leverage: "))
       margin_amount = float(input("Enter margin amount: "))
    except ValueError:
        print("Invalid input. Please enter numbers for prices, leverage and margin_amount")
        return 
    #Creating a try to verify the save_trade
    try:
        save_trade(trade_date,
                   asset,
                   direction,
                   entry_price,
                   exit_price,
                   leverage,
                   margin_amount
                   )
        
    except ValueError as error:
        print(error) 
        return
    
    display_summary()

if __name__ == "__main__":
    main()  
