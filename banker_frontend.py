import banker_db
import snack

class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

States = Enum(["CHOOSE_ACTION", "CHOOSE_YEAR", "CHOOSE_MONTH",
    "DISPLAY_STATEMENT", "ADD_TRANSACTION"])

# Actions which can be carried out from the top-level menu.
Actions = Enum(["VIEW_STATEMENTS", "ADD_TRANSACTION", "EXIT"])

def make_listbox(height, items):
    listbox = snack.Listbox(height, returnExit=1, scroll=1)
    for index, item in enumerate(items):
        listbox.append(str(item), index)
    return listbox

# Return a choice from the list of items.
def get_choice(screen, items):
    listbox = make_listbox(20, items)
    grid = snack.GridForm(screen, "Banker", 1, 1)
    grid.add(listbox, 0, 0)
    grid.runOnce()
    return listbox.current()

# Return a choice from the list of items,
# or None if the user chooses the "Back" choice.
def get_choice_or_back(screen, items):
    index = get_choice(screen, items + ["Back"])
    if index < len(items):
        return index
    return None

# Choose from the months in the chosen year which have one or more transactions.
def choose_month(conn, screen, year):
    months = banker_db.get_months(conn, year)
    index = get_choice_or_back(screen, months)
    if index is None:
        return index
    return months[index]

# Choose from all the years in the database which have transactions.
def choose_year(conn, screen):
    years = banker_db.get_years(conn)
    index = get_choice_or_back(screen, years)
    if index is None:
        return index
    return years[index]

# Display a list of transactions for the chosen year and month.
def display_statement(conn, screen, year, month):
    transactions = banker_db.get_transactions(conn, year, month)
    transaction_strings =\
        map(lambda t: "%2d %30s %10.2f" %\
            (t.day, t.name, float(t.amount) / 100), transactions)
    get_choice(screen, transaction_strings)

def parse_transaction(transaction_string):
    try:
        fields = transaction_string.split(',')
        year = int(fields[0])
        month = int(fields[1])
        day = int(fields[2])
        name = fields[3]
        amount = int(fields[4])
        transaction = banker_db.Transaction(year, month, day, name, amount)
        return transaction
    except:
        raise RuntimeError("Failed to parse transaction.")

# Prompt the user to enter details about a new transaction.
def create_transaction(conn, screen):
    entry = snack.Entry(60, returnExit=1)
    grid = snack.GridForm(screen, "Banker", 1, 1)
    grid.add(entry, 0, 0)
    grid.runOnce()
    try:
        transaction = parse_transaction(entry.value())
        return transaction
    except:
        return None

# Choose a top-level action to perform.
def choose_action(conn, screen):
    actions = [Actions.VIEW_STATEMENTS, Actions.ADD_TRANSACTION, Actions.EXIT]
    action_strings = ["View statements", "Add transaction", "Exit"]
    index = get_choice(screen, action_strings)
    return actions[index]

# Set up initial state, then start the main loop.
def main(screen, conn):
    state = States.CHOOSE_ACTION
    running = True
    year = None
    month = None
    while running:
        # Choose a top-level action.
        if state == States.CHOOSE_ACTION:
            action = choose_action(conn, screen)
            if action == Actions.VIEW_STATEMENTS:
                state = States.CHOOSE_YEAR
            elif action == Actions.ADD_TRANSACTION:
                state = States.ADD_TRANSACTION
            elif action == Actions.EXIT:
                running = False
        # Choose a year.
        elif state ==  States.CHOOSE_YEAR:
            year = choose_year(conn, screen)
            if year:
                state = States.CHOOSE_MONTH
            else:
                state = States.CHOOSE_ACTION
        # Choose a month (assuming a year has already been chosen).
        elif state == States.CHOOSE_MONTH:
            month = choose_month(conn, screen, year)
            if month:
                state = States.DISPLAY_STATEMENT
            else:
                state = States.CHOOSE_YEAR
        # Display a statement.
        elif state == States.DISPLAY_STATEMENT:
            display_statement(conn, screen, year, month)
            state = States.CHOOSE_MONTH
        # Add a transaction.
        elif state == States.ADD_TRANSACTION:
            transaction = create_transaction(conn, screen)
            if transaction:
                banker_db.add_transaction(conn, transaction)
            else:
                state = States.CHOOSE_ACTION
