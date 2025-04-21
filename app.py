from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
db = SQLAlchemy(app)

def format_money(amount):
    return "{:,.0f}".format(amount).replace(",", ".")

app.jinja_env.filters['format_money'] = format_money

class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Income(date='{self.date}', category='{self.category}', description='{self.description}', amount={self.amount})"

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Expense(date='{self.date}', category='{self.category}', description='{self.description}', amount={self.amount})"

@app.route('/add_income', methods=['POST'])
def add_income():
    date = datetime.datetime.strptime(request.form['income_date'], '%Y-%m-%d').date()
    category = request.form['income_category']
    description = request.form['income_description']
    amount = float(request.form['income_amount'])

    new_income = Income(date=date, category=category, description=description, amount=amount)
    db.session.add(new_income)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/')
def index():
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    expenses = [{**expense.__dict__, 'amount': int(expense.amount)} for expense in expenses]
    incomes = Income.query.order_by(Income.date.desc()).all()
    incomes = [{**income.__dict__, 'amount': int(income.amount)} for income in incomes]
    today_date = datetime.date.today().strftime('%Y-%m-%d')
    return render_template('index.html', expenses=expenses, incomes=incomes, today_date=today_date)

@app.route('/add', methods=['POST'])
def add_expense():
    date = datetime.datetime.strptime(request.form['date'], '%Y-%m-%d').date()
    category = request.form['category']
    description = request.form['description']
    amount = float(request.form['amount'])

    new_expense = Expense(date=date, category=category, description=description, amount=amount)
    db.session.add(new_expense)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/report')
def report():
    now = datetime.datetime.now()
    month = now.month
    year = now.year

    expenses = Expense.query.filter(db.extract('month', Expense.date) == month, db.extract('year', Expense.date) == year).all()
    total_expenses = int(sum(expense.amount for expense in expenses))
    incomes = Income.query.filter(db.extract('month', Income.date) == month, db.extract('year', Income.date) == year).all()
    total_incomes = int(sum(income.amount for income in incomes))

    category_totals = {}
    for expense in expenses:
        if expense.category in category_totals:
            category_totals[expense.category] += expense.amount
        else:
            category_totals[expense.category] = expense.amount

    category_totals = {category: int(total) for category, total in category_totals.items()}
    category_totals = {category: int(total) for category, total in category_totals.items()}
    expenses = [{**expense.__dict__, 'amount': int(expense.amount)} for expense in expenses]
    incomes = [{**income.__dict__, 'amount': int(income.amount)} for income in incomes]
    return render_template('report.html', expenses=expenses, incomes=incomes, total_expenses=total_expenses, total_incomes=total_incomes, category_totals=category_totals, month=month, year=year)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)