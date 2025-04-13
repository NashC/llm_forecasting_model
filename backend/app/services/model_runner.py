import ast
import builtins
import inspect
import traceback
import pandas as pd
import numpy as np
import io
import sys
import matplotlib.pyplot as plt
from typing import Dict, Any, Tuple, List, Optional

# List of allowed modules for sandboxing
ALLOWED_MODULES = {
    'pandas': pd,
    'numpy': np,
    'math': __import__('math'),
    'datetime': __import__('datetime'),
    'matplotlib.pyplot': plt,
    'scipy': __import__('scipy'),
    'statsmodels': __import__('statsmodels'),
}

# List of allowed builtins for sandboxing
ALLOWED_BUILTINS = {
    'dict': dict,
    'list': list,
    'tuple': tuple,
    'set': set,
    'int': int,
    'float': float,
    'str': str,
    'bool': bool,
    'len': len,
    'range': range,
    'enumerate': enumerate,
    'zip': zip,
    'min': min,
    'max': max,
    'sum': sum,
    'round': round,
    'abs': abs,
    'all': all,
    'any': any,
    'sorted': sorted,
    'print': print,
}


def run_model(code: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Runs the financial model code with the provided parameters.
    Returns the model output which should be a dictionary.
    
    Args:
        code: Python code to execute
        parameters: Dictionary of model parameters
        
    Returns:
        Dictionary containing model results
    """
    result = {}
    error = None
    figures = []
    
    # Create a secure execution environment
    globals_dict = {**ALLOWED_MODULES}
    locals_dict = {**ALLOWED_BUILTINS, 'parameters': parameters, 'result': result}
    
    # Redirect stdout to capture print statements
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout
    
    try:
        # First, parse the code to catch syntax errors
        ast.parse(code)
        
        # Execute the code
        exec(code, globals_dict, locals_dict)
        
        # Get the result
        result = locals_dict.get('result', {})
        
        # Check if there are figures to convert to base64
        figures = locals_dict.get('figures', [])
        
        # Convert any pandas DataFrames to dictionaries
        for key, value in result.items():
            if isinstance(value, pd.DataFrame):
                result[key] = value.to_dict(orient='records')
        
    except Exception as e:
        error = {
            'type': str(type(e).__name__),
            'message': str(e),
            'traceback': traceback.format_exc()
        }
    finally:
        # Restore stdout
        sys.stdout = old_stdout
        output = new_stdout.getvalue()
    
    # Add any console output and error info to the result
    if output:
        result['console_output'] = output
    
    if error:
        result['error'] = error
    
    return result


def generate_model_code(model_type: str, prompt: str, parameters: Optional[Dict[str, Any]] = None) -> str:
    """
    Generates Python code for a financial model based on the provided prompt.
    
    Args:
        model_type: Type of financial model (revenue, expense, cash_flow, etc.)
        prompt: Natural language description of the model
        parameters: Initial parameters for the model (optional)
        
    Returns:
        Generated Python code for the model
    """
    # This is a stub - in a real implementation, this would call the LLM service
    # For now, return a sample template for the corresponding model type
    
    if model_type == "revenue":
        return generate_revenue_model_template(prompt, parameters)
    elif model_type == "expense":
        return generate_expense_model_template(prompt, parameters)
    elif model_type == "cash_flow":
        return generate_cash_flow_model_template(prompt, parameters)
    else:
        return generate_custom_model_template(model_type, prompt, parameters)


def generate_revenue_model_template(prompt: str, parameters: Optional[Dict[str, Any]] = None) -> str:
    """Generate a revenue model template"""
    return '''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Get parameters or use defaults
params = parameters.copy()
start_date = params.get('start_date', '2023-01-01')
periods = params.get('periods', 36)  # 3 years by default
initial_customers = params.get('initial_customers', 100)
monthly_growth_rate = params.get('monthly_growth_rate', 0.05)  # 5% monthly growth
average_revenue_per_customer = params.get('average_revenue_per_customer', 100)
churn_rate = params.get('churn_rate', 0.02)  # 2% monthly churn

# Create date range
date_range = pd.date_range(start=start_date, periods=periods, freq='M')

# Initialize arrays
customers = np.zeros(periods)
new_customers = np.zeros(periods)
lost_customers = np.zeros(periods)
revenue = np.zeros(periods)

# Set initial values
customers[0] = initial_customers
new_customers[0] = initial_customers
revenue[0] = customers[0] * average_revenue_per_customer

# Calculate values for each period
for i in range(1, periods):
    # New customers acquired
    new_customers[i] = customers[i-1] * monthly_growth_rate
    
    # Customers lost to churn
    lost_customers[i] = customers[i-1] * churn_rate
    
    # Net customers
    customers[i] = customers[i-1] + new_customers[i] - lost_customers[i]
    
    # Revenue
    revenue[i] = customers[i] * average_revenue_per_customer

# Create a dataframe with the results
df = pd.DataFrame({
    'date': date_range,
    'customers': customers,
    'new_customers': new_customers,
    'lost_customers': lost_customers,
    'revenue': revenue,
})

# Create a plot for visualization
plt.figure(figsize=(12, 6))
plt.plot(df['date'], df['revenue'], label='Monthly Revenue')
plt.title('Revenue Forecast')
plt.xlabel('Date')
plt.ylabel('Revenue ($)')
plt.legend()
plt.grid(True)

# Create summary metrics
total_revenue = df['revenue'].sum()
max_monthly_revenue = df['revenue'].max()
total_customers_acquired = df['new_customers'].sum()
total_customers_lost = df['lost_customers'].sum()
final_customer_count = df['customers'].iloc[-1]

# Store results in the result dictionary
result = {
    'forecast_data': df.to_dict(orient='records'),
    'summary': {
        'total_revenue': total_revenue,
        'max_monthly_revenue': max_monthly_revenue,
        'total_customers_acquired': total_customers_acquired,
        'total_customers_lost': total_customers_lost,
        'final_customer_count': final_customer_count,
    }
}
'''


def generate_expense_model_template(prompt: str, parameters: Optional[Dict[str, Any]] = None) -> str:
    """Generate an expense model template"""
    return '''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Get parameters or use defaults
params = parameters.copy()
start_date = params.get('start_date', '2023-01-01')
periods = params.get('periods', 36)  # 3 years by default
fixed_costs = params.get('fixed_costs', {
    'rent': 5000,
    'salaries': 20000,
    'utilities': 1000,
    'insurance': 1500,
    'other_fixed': 2000
})
variable_costs = params.get('variable_costs', {
    'marketing': 0.10,  # 10% of revenue
    'sales_commission': 0.05,  # 5% of revenue
    'customer_support': 0.03,  # 3% of revenue
    'other_variable': 0.02,  # 2% of revenue
})
initial_revenue = params.get('initial_revenue', 50000)
revenue_growth_rate = params.get('revenue_growth_rate', 0.03)  # 3% monthly growth
inflation_rate = params.get('inflation_rate', 0.02 / 12)  # Annual inflation rate converted to monthly

# Create date range
date_range = pd.date_range(start=start_date, periods=periods, freq='M')

# Initialize arrays
revenue = np.zeros(periods)
fixed_expenses = np.zeros(periods)
variable_expenses = np.zeros(periods)
total_expenses = np.zeros(periods)

# Set initial values
revenue[0] = initial_revenue

# Calculate initial fixed expenses (sum of all fixed costs)
initial_fixed_expenses = sum(fixed_costs.values())
fixed_expenses[0] = initial_fixed_expenses

# Calculate initial variable expenses
initial_variable_expenses = sum([rate * revenue[0] for rate in variable_costs.values()])
variable_expenses[0] = initial_variable_expenses
total_expenses[0] = fixed_expenses[0] + variable_expenses[0]

# Calculate values for each period
for i in range(1, periods):
    # Revenue grows each month
    revenue[i] = revenue[i-1] * (1 + revenue_growth_rate)
    
    # Fixed expenses increase with inflation
    fixed_expenses[i] = fixed_expenses[i-1] * (1 + inflation_rate)
    
    # Variable expenses as a percentage of revenue
    variable_expenses[i] = sum([rate * revenue[i] for rate in variable_costs.values()])
    
    # Total expenses
    total_expenses[i] = fixed_expenses[i] + variable_expenses[i]

# Create a dataframe with the results
df = pd.DataFrame({
    'date': date_range,
    'revenue': revenue,
    'fixed_expenses': fixed_expenses,
    'variable_expenses': variable_expenses,
    'total_expenses': total_expenses,
    'profit_loss': revenue - total_expenses
})

# Create a plot for visualization
plt.figure(figsize=(12, 6))
plt.plot(df['date'], df['total_expenses'], label='Total Expenses')
plt.plot(df['date'], df['fixed_expenses'], label='Fixed Expenses')
plt.plot(df['date'], df['variable_expenses'], label='Variable Expenses')
plt.title('Expense Forecast')
plt.xlabel('Date')
plt.ylabel('Expenses ($)')
plt.legend()
plt.grid(True)

# Create expense breakdown for the last period
final_fixed_expenses = fixed_expenses[-1]
final_variable_expenses = variable_expenses[-1]
final_total_expenses = total_expenses[-1]

fixed_breakdown = {name: value * (1 + inflation_rate) ** (periods - 1) 
                  for name, value in fixed_costs.items()}
variable_breakdown = {name: rate * revenue[-1] for name, rate in variable_costs.items()}

# Store results in the result dictionary
result = {
    'forecast_data': df.to_dict(orient='records'),
    'expense_breakdown': {
        'fixed': fixed_breakdown,
        'variable': variable_breakdown
    },
    'summary': {
        'total_expenses_sum': df['total_expenses'].sum(),
        'average_monthly_expenses': df['total_expenses'].mean(),
        'final_expense_ratio': total_expenses[-1] / revenue[-1] if revenue[-1] > 0 else 0,
    }
}
'''


def generate_cash_flow_model_template(prompt: str, parameters: Optional[Dict[str, Any]] = None) -> str:
    """Generate a cash flow model template"""
    return '''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Get parameters or use defaults
params = parameters.copy()
start_date = params.get('start_date', '2023-01-01')
periods = params.get('periods', 36)  # 3 years by default
initial_cash = params.get('initial_cash', 100000)
monthly_revenue = params.get('monthly_revenue', 50000)
revenue_growth_rate = params.get('revenue_growth_rate', 0.03)  # 3% monthly growth
collection_delay = params.get('collection_delay', 1)  # Months to collect revenue
monthly_expenses = params.get('monthly_expenses', 40000)
expense_growth_rate = params.get('expense_growth_rate', 0.02)  # 2% monthly growth
payment_delay = params.get('payment_delay', 0)  # Months to pay expenses
investments = params.get('investments', [])  # List of (month, amount) tuples
financing = params.get('financing', [])  # List of (month, amount) tuples
loan_payments = params.get('loan_payments', [])  # List of (month, amount) tuples

# Create date range
date_range = pd.date_range(start=start_date, periods=periods, freq='M')

# Initialize arrays
cash_balance = np.zeros(periods)
revenue = np.zeros(periods)
expenses = np.zeros(periods)
collections = np.zeros(periods)
payments = np.zeros(periods)
investing_cash_flow = np.zeros(periods)
financing_cash_flow = np.zeros(periods)
net_cash_flow = np.zeros(periods)

# Set initial values
cash_balance[0] = initial_cash
revenue[0] = monthly_revenue
expenses[0] = monthly_expenses

# If collection delay is 0, collect immediately
if collection_delay == 0:
    collections[0] = revenue[0]
# If payment delay is 0, pay immediately
if payment_delay == 0:
    payments[0] = expenses[0]

# Add initial investments and financing if any
for month, amount in investments:
    if month == 0:
        investing_cash_flow[0] -= amount  # Negative because it's an outflow
        
for month, amount in financing:
    if month == 0:
        financing_cash_flow[0] += amount
        
for month, amount in loan_payments:
    if month == 0:
        financing_cash_flow[0] -= amount  # Negative because it's an outflow

# Calculate net cash flow for the first period
net_cash_flow[0] = collections[0] - payments[0] + investing_cash_flow[0] + financing_cash_flow[0]

# Calculate values for each period
for i in range(1, periods):
    # Revenue and expenses grow each month
    revenue[i] = revenue[i-1] * (1 + revenue_growth_rate)
    expenses[i] = expenses[i-1] * (1 + expense_growth_rate)
    
    # Collect revenue with delay
    if i >= collection_delay:
        collections[i] = revenue[i - collection_delay]
    
    # Pay expenses with delay
    if i >= payment_delay:
        payments[i] = expenses[i - payment_delay]
    
    # Add investments and financing
    for month, amount in investments:
        if month == i:
            investing_cash_flow[i] -= amount
            
    for month, amount in financing:
        if month == i:
            financing_cash_flow[i] += amount
            
    for month, amount in loan_payments:
        if month == i:
            financing_cash_flow[i] -= amount
    
    # Net cash flow
    net_cash_flow[i] = collections[i] - payments[i] + investing_cash_flow[i] + financing_cash_flow[i]
    
    # Cash balance
    cash_balance[i] = cash_balance[i-1] + net_cash_flow[i]

# Create a dataframe with the results
df = pd.DataFrame({
    'date': date_range,
    'cash_balance': cash_balance,
    'revenue': revenue,
    'expenses': expenses,
    'collections': collections,
    'payments': payments,
    'investing_cash_flow': investing_cash_flow,
    'financing_cash_flow': financing_cash_flow,
    'net_cash_flow': net_cash_flow
})

# Create a plot for visualization
plt.figure(figsize=(12, 6))
plt.plot(df['date'], df['cash_balance'], label='Cash Balance')
plt.title('Cash Flow Forecast')
plt.xlabel('Date')
plt.ylabel('Cash ($)')
plt.legend()
plt.grid(True)

# Create another plot for cash flows
plt.figure(figsize=(12, 6))
plt.plot(df['date'], df['net_cash_flow'], label='Net Cash Flow')
plt.plot(df['date'], df['collections'], label='Collections')
plt.plot(df['date'], df['payments'], label='Payments')
plt.title('Cash Flow Components')
plt.xlabel('Date')
plt.ylabel('Amount ($)')
plt.legend()
plt.grid(True)

# Store results in the result dictionary
result = {
    'forecast_data': df.to_dict(orient='records'),
    'summary': {
        'min_cash_balance': df['cash_balance'].min(),
        'max_cash_balance': df['cash_balance'].max(),
        'final_cash_balance': df['cash_balance'].iloc[-1],
        'total_collections': df['collections'].sum(),
        'total_payments': df['payments'].sum(),
        'total_net_cash_flow': df['net_cash_flow'].sum(),
    }
}
'''


def generate_custom_model_template(model_type: str, prompt: str, parameters: Optional[Dict[str, Any]] = None) -> str:
    """Generate a custom model template"""
    return '''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Get parameters or use defaults
params = parameters.copy()
start_date = params.get('start_date', '2023-01-01')
periods = params.get('periods', 36)  # 3 years by default

# Create date range
date_range = pd.date_range(start=start_date, periods=periods, freq='M')

# Initialize arrays for our model
values = np.zeros(periods)
growth_rate = params.get('growth_rate', 0.02)  # 2% monthly growth

# Set initial value
values[0] = params.get('initial_value', 1000)

# Calculate values for each period
for i in range(1, periods):
    values[i] = values[i-1] * (1 + growth_rate)

# Create a dataframe with the results
df = pd.DataFrame({
    'date': date_range,
    'value': values,
})

# Create a plot for visualization
plt.figure(figsize=(12, 6))
plt.plot(df['date'], df['value'], label='Forecast')
plt.title('Custom Forecast Model')
plt.xlabel('Date')
plt.ylabel('Value')
plt.legend()
plt.grid(True)

# Store results in the result dictionary
result = {
    'forecast_data': df.to_dict(orient='records'),
    'summary': {
        'total_value': df['value'].sum(),
        'average_value': df['value'].mean(),
        'final_value': df['value'].iloc[-1],
    }
}
''' 