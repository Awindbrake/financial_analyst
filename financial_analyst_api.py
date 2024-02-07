

import base64
import requests
import pandas as pd
import io
from io import StringIO
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError
from typing import Dict, TypedDict, Optional



app = FastAPI(
        title = "Financial Analysis API",
        description = "Performs financial analysis and calculates various KPIs based on submitted financial data.",
        version = "1.0.0",
        servers = [
            {

            "url": "https://financialanalyst-d8993699e73a.herokuapp.com",
            "description": "financial report analyst"
            }
        ]
            )

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
    other_operational_income: Optional[float]
    other_income: Optional[float]
    interest_income: Optional[float]
    op_cash_flow: Optional[float]

class FinancialFigures(BaseModel):
    data: Dict[str, FinancialDetails]

@app.post("/submitData")
def submit_data(input_data: FinancialFigures):
    
    return {"message": "Data received successfully"}

@app.post("/calculateKPIs")
def api_calculate_kpis(input_data: FinancialFigures):
    # Debug print to check the structure of input_data
    print("Type of input_data:", type(input_data))
    print("Keys in input_data.data:", input_data.data.keys())

    # Call the simplified calculate_kpis function
    kpi_results = calculate_kpis(input_data.data)
    return kpi_results

# @app.post("/calculateKPIs")
# def api_calculate_kpis(input_data: FinancialFigures):
#     try:
#         kpi_results = calculate_kpis(input_data.data)
#         return kpi_results
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")

# def calculate_kpis(financial_data: Dict[str, FinancialDetails]) -> Dict[str, any]:
#     # Just return a simple response for debugging
#     return {"debug": "function reached successfully", "keys": list(financial_data.keys())}

def calculate_kpis(financial_data: Dict[str, FinancialDetails]) -> Dict[str, Dict[str, float]]:
    try:
        kpi_data = {}
        for year, details in financial_data.items():
            # Directly access attributes of FinancialDetails model, ensuring defaults where necessary
            equity = details.get('equity', 0)
            inventories = details.get('inventories', 0)
            non_current_assets = details.get('intangible_assets', 0) + details.get('property_plant_and_equipment', 0) + details.get('other_non_current_assets', 0)
            current_assets = details.get('cash_and_cash_equivalents', 0) + details.get('trade_receivables', 0) + details.get('other_current_assets', 0)
            # equity = details.equity or 0
            # inventories = details.inventories or 0
            # non_current_assets = (details.intangible_assets or 0) + (details.property_plant_and_equipment or 0) + (details.other_non_current_assets or 0)
            # current_assets = (details.cash_and_cash_equivalents or 0) + (details.trade_receivables or 0) + (details.other_current_assets or 0)
            # other_assets = details.other_assets or 0
            # active_accruals_deferrals = details.active_accruals_deferrals or 0
            # total_assets = non_current_assets + current_assets + other_assets + active_accruals_deferrals
            # short_term_liabilities = details.short_term_and_current_liabilities or 0
            # long_term_liabilities = details.long_term_debt_and_non_current_liabilities or 0
            # provisions = details.provisions or 0
            # passive_accruals_deferrals = details.passive_accruals_deferrals or 0
            # total_liabilities = short_term_liabilities + long_term_liabilities + provisions + passive_accruals_deferrals
            # sales_revenue = details.sales_revenue or 0
            # ebitda = sales_revenue - (details.cogs or 0)
            # ebit = ebitda - (details.depreciation or 0)
            # net_income = ebit - (details.other_operational_expense or 0) + (details.other_operational_income or 0) - (details.interest_expenses or 0) + (details.interest_income or 0) - (details.other_expenses or 0) + (details.other_income or 0)
            # op_cash_flow = details.op_cash_flow or 0

            # # Calculated KPIs based on the provided structure
            kpi_data[year] = {
                'Equity': equity,}

            #     'EBITDA': ebitda,
            #     'EBIT': ebit,
            #     'Net Income': net_income,
            #     'Equity Ratio': equity / total_assets if total_assets else 0,
                # 'Debt Ratio': total_liabilities / total_assets if total_assets else 0,
                # 'Equity-to-Fixed Assets Ratio I': equity / non_current_assets if non_current_assets else 0,
                # 'Equity-to-Fixed Assets Ratio II': equity / (non_current_assets + long_term_liabilities) if non_current_assets else 0,
                # 'Effective Debt': (short_term_liabilities + long_term_liabilities) - current_assets,
                # 'Static Gearing': total_liabilities / equity if equity else 0,
                # 'Dynamic Gearing in years': (short_term_liabilities + long_term_liabilities - current_assets) / op_cash_flow if op_cash_flow else 0,
                # 'Intensity of Inventories': inventories / total_assets if total_assets else 0,
                # 'Working Capital': current_assets - short_term_liabilities,
                # 'Property Constitution': non_current_assets / total_assets if total_assets else 0,
                # 'Current Ratio': current_assets / short_term_liabilities if short_term_liabilities else 0,
                # 'Quick Ratio': (current_assets - inventories) / short_term_liabilities if short_term_liabilities else 0,
                # 'Cash Ratio': current_assets / short_term_liabilities if short_term_liabilities else 0,
                # 'Return on Sales': net_income / sales_revenue if sales_revenue else 0,
                # 'Return on Assets': net_income / total_assets if total_assets else 0,
                # 'Return on Equity': net_income / equity if equity else 0,
                # 'Frequency of Capital Turnover': sales_revenue / total_assets if total_assets else 0,
                # 'Return on Investment': net_income / (equity + total_liabilities) if (equity + total_liabilities) else 0,
            # }

        return kpi_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error calculating KPIs: {str(e)}")

if __name__ == "__main__":
    # Placeholder for server start, actual server running code would be needed here
    pass

