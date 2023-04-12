import argparse
import csv
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# create an empty graph
G = nx.Graph()

# add nodes
for i in range(1, 81):
    G.add_node(i)

# add edges
with open("dummy_data.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)  # skip header row
    for row in reader:
        from_acc = int(row[1])
        to_acc = int(row[2])
        amount = float(row[3])
        G.add_edge(from_acc, to_acc, amount=amount)

# parse command-line arguments
parser = argparse.ArgumentParser(description='AML search tool')
parser.add_argument('from_acc', type=int, help='the account to start from')
parser.add_argument('-m', action='store_true', help='account with max transactions from the given account')
parser.add_argument('-amount', type=int, help='transactions above this amount')
parser.add_argument('-t', choices=['day', 'week', 'month'], default='month', help='transactions within the specified time period (default: %(default)s)')
args = parser.parse_args()


# filter edges based on command-line arguments
edges = []
for from_acc, to_acc, attributes in G.edges(data=True):
    amount = attributes['amount']
    if from_acc == args.from_acc:
        if args.amount is None or amount >= args.amount:
            if args.t == 'day':
                date_format = '%Y-%m-%d %H:%M:%S'
                txn_date = datetime.strptime('2023-04-12 00:00:00', date_format) - timedelta(days=1)
                txn_date_str = txn_date.strftime(date_format)
                if attributes.get('date', '') >= txn_date_str:
                    edges.append((from_acc, to_acc, amount))
            elif args.t == 'week':
                date_format = '%Y-%m-%d %H:%M:%S'
                txn_date = datetime.strptime('2023-04-12 00:00:00', date_format) - timedelta(weeks=1)
                txn_date_str = txn_date.strftime(date_format)
                if attributes.get('date', '') >= txn_date_str:
                    edges.append((from_acc, to_acc, amount))
            else:
                edges.append((from_acc, to_acc, amount))


# sort edges by transaction amount
if len(edges) > 0:
    edges.sort(key=lambda x: x[2], reverse=True)

# print edges based on command-line arguments
if len(edges) > 0:
    print(f"Transactions from account {args.from_acc}:")
    for edge in edges:
        to_acc = edge[1]
        amount = edge[2]
        date = edge[2].get('date', '')
        print(f"{args.from_acc} -> {to_acc}: ${amount:,} ({date})")
else:
    print(f"No transactions found for account {args.from_acc}")

# create a subgraph based on the filtered edges
print(edges)
l = [(x, y, d) for x, y, d in edges]
print(l)
subgraph = G.edge_subgraph(l)
# if requested, find the account with the max transactions from the given account
if args.m:
    max_acc = -1
    max_count = -1
    for node in subgraph.neighbors(args.from_acc):
        count = len(subgraph.edges(args.from_acc, node))
        if count > max_count:
            max_acc = node
            max_count = count
    if max_acc == -1:
        print(f"\nAccount with max transactions from {args.from_acc}: {max_acc} ({max_count} transactions)")

# draw the subgraph
pos = nx.spring_layout(subgraph)
nx.draw(subgraph, pos, with_labels=True, font_weight='bold', node_size=500, font_size=10)
edge_labels = {(u, v): d for u, v, d in subgraph.edges(data=True)}
nx.draw_networkx_edge_labels(subgraph, pos, edge_labels=edge_labels, font_size=8)
plt.show()
