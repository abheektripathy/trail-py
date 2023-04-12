import click
import csv
import dateutil.parser
import matplotlib.pyplot as plt

@click.command()
@click.option('--account', prompt='Enter account number', help='Account number to track')
@click.option('--amount', prompt='Enter transaction amount', type=float, help='Minimum transaction amount to track')
@click.option('--timeframe', prompt='Enter timeframe in days', type=int, help='Timeframe in days to track transactions')
def track(account, amount, timeframe):
    """Track transactions for a specified account"""
    # Read transaction data dump and filter transactions for the specified account, amount, and timeframe
    with open('transactions.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip header row
        transactions = []
        for row in reader:
            transaction_id, from_acc, to_acc, transaction_amount, transaction_time = row
            if from_acc == account and float(transaction_amount) >= amount:
                parsed_time = dateutil.parser.parse(transaction_time)
                if (parsed_time.date() - dateutil.parser.parse('1970-01-01').date()).days >= timeframe:
                    transactions.append((parsed_time, float(transaction_amount)))

    # Create graph
    fig, ax = plt.subplots()
    ax.plot_date([t for t, _ in transactions], [amount for _, amount in transactions], '-')
    ax.set_xlabel('Date')
    ax.set_ylabel('Transaction Amount')
    ax.set_title(f'Transactions for Account {account}')

    # Add markers for each transaction
    for t, amount in transactions:
        ax.plot_date([t], [amount], 'o', color='r', markersize=8)

    # Display transactions and graph
    print(f'Transactions for Account {account}:')
    for t, amount in transactions:
        print(f'{t}: {amount}')
    plt.show()
