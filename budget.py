import math


class Category:
  # constructor to create instance of category
  def __init__(self, description):
    self.description = description
    self.balance = 0
    self.ledger = []

  def __str__(self):
    stars = int((30 - len(self.description)) / 2)
    object_str = ('*' * stars) + self.description + ('*' * stars) + '\n'
    for e in self.ledger:
      desc = e['description']
      amount = '{0:.2f}'.format(float(e['amount']))
      len_desc = len(desc)
      if len_desc > 22:
        len_desc = 23
      tabs = (30 - len_desc) - len(amount)
      object_str += desc[:23] + (' ' * tabs) + amount + '\n'
    object_str += f'Total: {self.balance}'
    return object_str

  def deposit(self, amount, description=""):
    # append transaction to ledger
    self.ledger.append({"amount": amount, "description": description})
    # check if the desposit is smaller than zero
    if (amount < 0):
      return "Error: Please use withdraw to withdraw money instead of deposit!"
    self.balance += amount

  def withdraw(self, amount, description=""):
    if self.check_funds(amount):
      self.ledger.append({"amount": (amount * -1), "description": description})
      self.balance -= amount
      return True
    return False

  def get_balance(self):
    return self.balance

  def transfer(self, amount, category):
    # Transfer an amount from one category to another
    # check if the balance isn't to small
    if self.check_funds(amount):
      # prepare transaction strings
      transaction_w_str = f'Transfer to {category.description}'
      transaction_d_str = f'Transfer from {self.description}'
      self.ledger.append({
        "amount": (amount * -1),
        "description": transaction_w_str
      })
      category.ledger.append({
        "amount": amount,
        "description": transaction_d_str
      })
      self.balance -= amount
      category.balance += amount
      return True
    return False

  def check_funds(self, amount):
    return True if self.balance >= amount else False


def create_spend_chart(categories):
  # calculate percentage spend by each category based on withdraws
  percentage = []
  tmp = []
  w_sum = 0
  c_w_sum = 0
  for c in categories:
    for t in c.ledger:
      if t['amount'] < 0:
        w_sum += t['amount']
        c_w_sum += t['amount']
    tmp.append(c_w_sum)
    c_w_sum = 0

  # round values to next ten
  for p in tmp:
    percentage.append(int((p * 100) / w_sum))
    print(math.trunc((p * 100) / w_sum))

  # print bar chart table
  spend_chart = 'Percentage spent by category\n'
  for i in range(100, -10, -10):
    spend_chart += ' ' * (3 - len(str(i)))
    spend_chart += f'{i}|'
    for j in range(0, len(categories), 1):
      if percentage[j] >= i:
        spend_chart += '  o'
      else:
        spend_chart += ' ' * 3
    spend_chart += '\n'

  # print divider
  spend_chart += ' ' * 4
  spend_chart += '-' * (len(categories) * 3) + '\n'

  # get max length of category description and extend all descriptions to this length
  max_length_cat = max([len(c.description) for c in categories])
  cato = []
  for c in categories:
    val = max_length_cat - len(c.description)
    c.description += (' ' * val)
    cato.append(c.description)
  for cat in range(max_length_cat):
    spend_chart += ' ' * 6
    for c in categories:
      spend_chart += f'{c.description[cat]}  '
    spend_chart += '\n'
  return spend_chart
