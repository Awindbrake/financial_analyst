
import pandas as pd
import base64
import requests
import pandas as pd
import io
from io import StringIO
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError
from typing import Dict, TypedDict, Optional

app = FastAPI()

@app.get("/")
def read_root():
    return """
    <html>
        <head>
            <title>FastAPI Application</title>
        </head>
        <body>
            <h1>Welcome to the FastAPI application!</h1>
            <p>Visit <a href="/docs">/docs</a> for the API documentation.</p>
        </body>
    </html>
    """

# financial_data: {
#              "2021": {
#                "intangible_assets": 1000.0,
#                "property_plant_and_equipment": 5000.0,
#                "other_non_current_assets": 2000.0,
#                "inventories": 3000.0,
#                "trade_receivables": 1500.0,
#                "cash_and_cash_equivalents": 2500.0,
#                "other_current_assets": 1000.0,
#                "other_assets": 500.0,
#                "active_accruals_deferrals": 0,
#                "equity": 15000.0,
#                "short_term_and_current_liabilities": 5000.0,
#                "long_term_debt_and_non_current_liabilities": 8000.0,
#                "provisions": 200.0,
#                "passive_accruals_deferrals": 0,
#                "sales_revenue": 10000.0,
#                "cogs": 7000.0,
#                "other_operational_expense": 1000.0,
#                "depreciation": 500.0,
#                "interest_expenses": 300.0,
#                "other_expenses": 400.0,
#                "total_assets": 20000.0,
#                "total_liabilities": 13000.0,
#                "long_term_liabilities": 8000.0,
#                "other_operational_income": 1500.0,
#                "other_income": 250.0,
#                "interest_income": 100.0,
#                "ebit": 2300.0,
#                "net_income": 2100.0,
#                "op_cash_flow": 2200.0
#              }
#            }

class FinancialDetails(TypedDict, total=False):
    intangible_assets: Optional[float]
    property_plant_and_equipment: Optional[float]
    other_non_current_assets: Optional[float]
    inventories: Optional[float]
    trade_receivables: Optional[float]
    cash_and_cash_equivalents: Optional[float]
    other_current_assets: Optional[float]
    other_assets: Optional[float]
    active_accruals_deferrals: Optional[float]
    equity: Optional[float]
    short_term_and_current_liabilities: Optional[float]
    long_term_debt_and_non_current_liabilities: Optional[float]
    provisions: Optional[float]
    passive_accruals_deferrals: Optional[float]
    sales_revenue: Optional[float]
    cogs: Optional[float]  # Cost of Goods Sold
    other_operational_expense: Optional[float]
    depreciation: Optional[float]
    interest_expenses: Optional[float]
    other_expenses: Optional[float]
    total_assets: Optional[float]
    total_liabilities: Optional[float]
    long_term_liabilities: Optional[float]
    other_operational_income: Optional[float]
    other_income: Optional[float]
    interest_income: Optional[float]
    ebit: Optional[float]
    net_income: Optional[float]
    op_cash_flow: Optional[float]

class FinancialFigures(BaseModel):
    data: Dict[str, FinancialDetails]
    

@app.post("/submitData")
def submit_data(input_data: FinancialFigures):
    # Process the data
    # For example, you can pass this data to your calculation functions
    # and return the results
    return {"message": "Data received successfully"}


@app.post("/calculateKPIs")
def api_calculate_kpis(input_data: FinancialFigures):
    kpi_results = {}
    try:
        # Iterate through each year's data in the input
        for year, details in input_data.data.items():
            # Calculate KPIs for this year
            kpis_for_year = calculate_kpis(details, year)
            kpi_results[year] = kpis_for_year
        return kpi_results
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")

def calculate_kpis(financial_data: FinancialDetails, year: str):
    try:
        # Retrieve values from financial_data, set defaults to 0 if not present
        equity = financial_data.get('equity', 0)
        inventories = financial_data.get('inventories', 0)
        non_current_assets = financial_data.get('intangible_assets', 0) + financial_data.get('property_plant_and_equipment', 0) + financial_data.get('other_non_current_assets', 0)
        current_assets = financial_data.get('cash_and_cash_equivalents', 0) + financial_data.get('trade_receivables', 0) + financial_data.get('other_current_assets', 0)
        total_assets = non_current_assets + current_assets + financial_data.get('other_assets', 0) + financial_data.get('active_accruals_deferrals', 0)
        short_term_liabilities = financial_data.get('short_term_and_current_liabilities', 0)
        long_term_liabilities = financial_data.get('long_term_debt_and_non_current_liabilities', 0)
        total_liabilities = short_term_liabilities + long_term_liabilities + financial_data.get('provisions', 0) + financial_data.get('passive_accruals_deferrals', 0)
        balance_sum = total_liabilities + equity
        sales_revenue = financial_data.get('sales_revenue', 0)
        ebitda = sales_revenue - financial_data.get('cogs', 0) 
        ebit = ebitda - financial_data.get('depreciation', 0)
        net_income = ebit - financial_data.get('other_operational_expense', 0) + financial_data.get('other_operational_income', 0) - financial_data.get('interest_expenses', 0) + financial_data.get('interest_income', 0) - financial_data.get('other_expenses', 0)  + financial_data.get('other_income', 0) 
        op_cash_flow = financial_data.get('op_cash_flow', 0)

        # Perform calculations
        kpi_data = {
            'EBITDA': ebitda if ebitda else 0,
            'EBIT': ebit if ebit else 0,
            'Net Income': net_income,
            'Equity Ratio': equity / total_assets if total_assets else 0,
            'Debt Ratio': total_liabilities / total_assets if total_assets else 0,
            'Equity-to-Fixed Assets Ratio I': equity / non_current_assets if non_current_assets else 0,
            'Equity-to-Fixed Assets Ratio II': equity / (non_current_assets + long_term_liabilities) if non_current_assets else 0,
            'Effective Debt': (short_term_liabilities + long_term_liabilities) - current_assets,
            'Static Gearing': total_liabilities / equity if equity else 0,
            'Dynamic Gearing in years': 0 if op_cash_flow == 0 else ((short_term_liabilities + long_term_liabilities - current_assets) / op_cash_flow),
            'Intensity of Inventories': inventories / total_assets if total_assets else 0,
            'Working Capital': current_assets - short_term_liabilities,
            'Property Constitution': non_current_assets / total_assets if total_assets else 0,
            'Current Ratio': current_assets / short_term_liabilities if short_term_liabilities else 0,
            'Quick Ratio': (current_assets - inventories) / short_term_liabilities if short_term_liabilities else 0,
            'Cash Ratio': current_assets / short_term_liabilities if short_term_liabilities else 0,
            'Return on Sales': net_income / sales_revenue if sales_revenue else 0,
            'Return on Assets': net_income / total_assets if total_assets else 0,
            'Return on Equity': net_income / equity if equity else 0,
            'Frequency of Capital Turnover': sales_revenue / total_assets if total_assets else 0,
            'Return on Investment': net_income / (equity + total_liabilities) if (equity + total_liabilities) else 0,
        }
        
        return kpi_data

    except TypeError as e:
        # Handle specific type error (e.g., if non-numeric value encountered)
        raise HTTPException(status_code=422, detail=f"Type error in financial data: {e}")
    except ZeroDivisionError:
        # Handle division by zero error specifically
        raise HTTPException(status_code=422, detail="Attempted to divide by zero in KPI calculations")
    except Exception as e:
        # Catch-all for any other unexpected errors
        raise HTTPException(status_code=500, detail=f"Unexpected error calculating KPIs: {str(e)}")

# def calculate_kpis(financial_data: FinancialDetails, year: str):
#     # Your code assumes all these values are available in financial_data or other sources.
#     # You would need to adjust the logic if they are calculated differently or elsewhere.

#     # Retrieve values from financial_data, set defaults to 0 if not present
#     equity = financial_data.get('equity', 0)
#     total_assets = financial_data.get('total_assets', 0)
#     non_current_assets = financial_data.get('other_non_current_assets', 0)
#     inventories = financial_data.get('inventories', 0)
#     current_assets = financial_data.get('cash_and_cash_equivalents', 0) + financial_data.get('trade_receivables', 0) + financial_data.get('other_current_assets', 0)
#     short_term_liabilities = financial_data.get('short_term_and_current_liabilities', 0)
#     long_term_liabilities = financial_data.get('long_term_debt_and_non_current_liabilities', 0)
#     total_liabilities = short_term_liabilities + long_term_liabilities
#     sales_revenue = financial_data.get('sales_revenue', 0)
#     ebit = sales_revenue - financial_data.get('cogs', 0) - financial_data.get('operating_expenses', 0)
#     ebitda = ebit + financial_data.get('depreciation', 0)
#     net_income = financial_data.get('earnings', 0)
#     op_cash_flow = financial_data.get('op_cash_flow', 0)

#     # Calculate KPIs
#     kpi_data = {
#         'EBITDA': ebitda if ebitda else 0,
#         'EBIT': ebit if ebit else 0,
#         'Equity Ratio': equity / total_assets if total_assets else 0,
#         'Debt Ratio': total_liabilities / total_assets if total_assets else 0,
#         'Equity-to-Fixed Assets Ratio I': equity / non_current_assets if non_current_assets else 0,
#         'Equity-to-Fixed Assets Ratio II': equity / (non_current_assets + long_term_liabilities) if non_current_assets else 0,
#         'Effective Debt': (short_term_liabilities + long_term_liabilities) - current_assets,
#         'Static Gearing': total_liabilities / equity if equity else 0,
#         'Dynamic Gearing in years': None if op_cash_flow is None else ((short_term_liabilities + long_term_liabilities - current_assets) / op_cash_flow),
#         'Intensity of Inventories': inventories / total_assets if total_assets else 0,
#         'Working Capital': current_assets - short_term_liabilities,
#         'Property Constitution': non_current_assets / total_assets if total_assets else 0,
#         'Current Ratio': current_assets / short_term_liabilities if short_term_liabilities else 0,
#         'Quick Ratio': (current_assets - inventories) / short_term_liabilities if short_term_liabilities else 0,
#         'Cash Ratio': current_assets / short_term_liabilities if short_term_liabilities else 0,
#         'Return on Sales': ebit / sales_revenue if sales_revenue else 0,
#         'Return on Assets': net_income / total_assets if total_assets else 0,
#         'Return on Equity': net_income / equity if equity else 0,
#         'Frequency of Capital Turnover': sales_revenue / total_assets if total_assets else 0,
#         'Return on Investment': net_income / (equity + long_term_liabilities) if (equity + long_term_liabilities) else 0,
#     }
#     # 'Return on Equity' should not be calculated if equity is non-negative,
#     # so we adjust it after the calculations
#     if equity >= 0:
#         kpi_data['Return on Equity'] = net_income / equity
#     else:
#         # If equity is zero or negative, set ROE to None or some other flag value that indicates it's not applicable.
#         kpi_data['Return on Equity'] = None


#     return kpi_data

# Main function, assuming it's now being used to run a simple server
def main():
    
    
    # Placeholder for server start, actual server running code would be needed here
    pass

if __name__ == "__main__":
    main()

