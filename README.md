# trail-py
CLI tool to track money trails and analyse txns with various AML indicators.


### Description:<br/>
A security CLI tool for financial auditors, which would help them display the transaction dumps, provided by the bank. in form of graphs and tables, with filters, which allow you to sort the data by a specific time frame, most monetary amounts, etc.

Also, allows auto flagging of transactions based on specific AML(anti-money laundering) indicators, and displaying them as tables currently in the cli itself. Future plans include to use a deep forested ml model trained on actual txn dumps based on such AML tools and provide flagged accounts(basically accounts with a higher frequency of flagged txns) as csv or pdfs for a easier analysis.

you can check this [loom](https://www.loom.com/share/b48eb4aad7e44fff95490ca2c5111e20) for a quick product pitch.
<br/>
<br/>
#### Run Locally:

```bash
git clone
cd /
#add up txn's dumps in dummy_data.csv
```
#### Example Commands

```py

#this would show the txn flow as a graph for the account 123... above amount 4000 and for the latest month
python trail.py 0123456789123456 -amount=4000 -t=month

#this would display up the txns's of the specific account which is 2x or above the median amount maintained by the account.
python hightxnval.py 0123456789123456 "-t=month"

```
<br/>

we intend to add up a frontend as well, for the non technical folks, the cli we provided can be directly integrated into (as a new feature set) already scaled up infra's of such auditing/gov organizations, hence they don't have to rely up on new applications/infrastructure.
