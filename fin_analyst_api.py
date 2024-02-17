from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI(
    title="Financial Analysis",
    description="Performs basic financial analysis and calculates key financial ratios.",
    version="1.0.0",
    servers=[
        {
            "url": "https://financialanalyst-d8993699e73a.herokuapp.com",
            "description": "Financial Analysis API"
        }
    ]
)
class FinancialData(BaseModel):
    intangible_assets: float = Field(..., description="Total intangible assets.")
    property_plant_and_equipment: float = Field(..., description="Total property, plant, and equipment.")
    other_non_current_assets: float = Field(..., description="Total other non-current assets.")
    inventories: float = Field(..., description="Total inventories.")
    trade_receivables: float = Field(..., description="Total trade receivables.")
    cash_and_cash_equivalents: float = Field(..., description="Total cash and cash equivalents.")
    other_current_assets: float = Field(..., description="Total other current assets.")
    other_assets: float = Field(..., description="Total other assets.")
    active_accruals_deferrals: float = Field(..., description="Total active accruals and deferrals.")
    equity: float = Field(..., description="Total equity.")
    short_term_liabilities: float = Field(..., description="Total short-term liabilities.")
    long_term_liabilities: float = Field(..., description="Total long-term liabilities.")
    provisions: float = Field(..., description="Total provisions.")
    passive_accruals_deferrals: float = Field(..., description="Total passive accruals and deferrals.")
    sales_revenue: float = Field(..., description="Total sales revenue.")
    cogs: float = Field(..., description="Total cost of goods sold.")
    other_operational_expense: float = Field(..., description="Total other operational expenses.")
    depreciation: float = Field(..., description="Total depreciation.")
    interest_expenses: float = Field(..., description="Total interest expenses.")
    other_expenses: float = Field(..., description="Total other expenses.")
    other_operational_income: float = Field(..., description="Total other operational income.")
    other_income: float = Field(..., description="Total other income.")
    interest_income: float = Field(..., description="Total interest income.")
    op_cash_flow: float = Field(..., description="Total operating cash flow.")



def calculate_kpi(intangible_assets: float, property_plant_and_equipment: float, other_non_current_assets: float,
                         inventories: float, trade_receivables: float, cash_and_cash_equivalents: float,
                         other_current_assets: float, other_assets: float, active_accruals_deferrals: float,
                         equity: float, short_term_liabilities: float, long_term_liabilities: float,
                         provisions: float, passive_accruals_deferrals: float, sales_revenue: float, cogs: float,
                         other_operational_expense: float, depreciation: float, interest_expenses: float,
                         other_expenses: float, other_operational_income: float, other_income: float,
                         interest_income: float, op_cash_flow: float) -> dict:
    
    non_current_assets = intangible_assets + property_plant_and_equipment + other_non_current_assets
    current_assets = inventories + trade_receivables + cash_and_cash_equivalents + other_current_assets
    total_assets = non_current_assets + current_assets + other_assets + active_accruals_deferrals
    total_liabilities = short_term_liabilities+long_term_liabilities
    ebitda = sales_revenue - cogs - other_operational_expense  + other_operational_income 
    ebit = ebitda - depreciation
    net_income = net_income = ebit - interest_expenses + interest_income - other_expenses + other_income
    equity_ratio = equity / total_assets if total_assets else 0
    debt_ratio = total_liabilities / total_assets if total_assets else 0
    equity_to_fixed_assets_ratio_I = equity / non_current_assets if non_current_assets else 0
    equity_to_fixed_assets_ratio_II = equity / (non_current_assets + long_term_liabilities) if (non_current_assets + long_term_liabilities) else 0
    effective_debt = (short_term_liabilities + long_term_liabilities) - current_assets
    static_gearing = total_liabilities / equity if equity else 0
    dynamic_gearing_in_years = (short_term_liabilities + long_term_liabilities - current_assets) / op_cash_flow if op_cash_flow else 0
    intensity_of_inventories = inventories / total_assets if total_assets else 0
    working_capital = current_assets - short_term_liabilities
    property_constitution = non_current_assets / total_assets if total_assets else 0
    current_ratio = current_assets / short_term_liabilities if short_term_liabilities else 0
    quick_ratio = (current_assets - inventories) / short_term_liabilities if short_term_liabilities else 0
    cash_ratio = cash_and_cash_equivalents / short_term_liabilities if short_term_liabilities else 0
    return_on_sales = net_income / sales_revenue if sales_revenue else 0
    return_on_assets = net_income / total_assets if total_assets else 0
    return_on_equity = net_income / equity if equity else 0
    frequency_of_capital_turnover = sales_revenue / total_assets if total_assets else 0
    return_on_investment = net_income / (equity + total_liabilities) if (equity + total_liabilities) else 0

    # Return a dictionary instead of a list
    return {
        "EBITDA": ebitda,
        "EBIT": ebit,
        "Net Income": net_income,
        "Equity Ratio": equity_ratio,
        "Debt Ratio": debt_ratio,
        "Equity to Fixed Assets Ratio I": equity_to_fixed_assets_ratio_I,
        "Equity to Fixed Assets Ratio II": equity_to_fixed_assets_ratio_II,
        "Effective Debt": effective_debt,
        "Static Gearing": static_gearing,
        "Dynamic Gearing in Years": dynamic_gearing_in_years,
        "Intensity of Inventories": intensity_of_inventories,
        "Working Capital": working_capital,
        "Property Constitution": property_constitution,
        "Current Ratio": current_ratio,
        "Quick Ratio": quick_ratio,
        "Cash Ratio": cash_ratio,
        "Return on Sales": return_on_sales,
        "Return on Assets": return_on_assets,
        "Return on Equity": return_on_equity,
        "Frequency of Capital Turnover": frequency_of_capital_turnover,
        "Return on Investment": return_on_investment
    }

def calculate_earnings(sales_revenues: float, cogs: float) -> float:
    return sales_revenues - cogs

def calculate_return_on_equity(earnings: float, equity: float) -> float:
    return earnings / equity

@app.post("/analyze")
async def analyze_financials(data: FinancialData):
    kpis = calculate_kpi(
        data.intangible_assets, data.property_plant_and_equipment, data.other_non_current_assets,
        data.inventories, data.trade_receivables, data.cash_and_cash_equivalents, data.other_current_assets,
        data.other_assets, data.active_accruals_deferrals, data.equity, data.short_term_liabilities,
        data.long_term_liabilities, data.provisions, data.passive_accruals_deferrals, data.sales_revenue,
        data.cogs, data.other_operational_expense, data.depreciation, data.interest_expenses,
        data.other_expenses, data.other_operational_income, data.other_income, data.interest_income,
        data.op_cash_flow
    )
    return {
        "kpis": kpis
    }

@app.get("/")
def read_root():
    return {"message": "Welcome to the Financial Analysis API. Visit /docs for documentation."}
