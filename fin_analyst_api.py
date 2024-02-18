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
    net_income = ebit - interest_expenses + interest_income - other_expenses + other_income
    equity_ratio = round(equity / total_assets, 2) if total_assets else 0 
    debt_ratio = round(total_liabilities / total_assets,2) if total_assets else 0
    equity_to_fixed_assets_ratio_I = round(equity / non_current_assets,2) if non_current_assets else 0
    equity_to_fixed_assets_ratio_II = round(equity / (non_current_assets + long_term_liabilities),2) if (non_current_assets + long_term_liabilities) else 0
    effective_debt = (short_term_liabilities + long_term_liabilities) - current_assets
    static_gearing = round(total_liabilities / equity,2) if equity else 0
    dynamic_gearing_in_years = round((short_term_liabilities + long_term_liabilities - current_assets) / op_cash_flow,1) if op_cash_flow else 0
    intensity_of_inventories = round(inventories / total_assets,2) if total_assets else 0
    working_capital = current_assets - short_term_liabilities
    property_constitution = round(non_current_assets / total_assets,2) if total_assets else 0
    current_ratio = round(current_assets / short_term_liabilities,2) if short_term_liabilities else 0
    quick_ratio = round((current_assets - inventories) / short_term_liabilities,2) if short_term_liabilities else 0
    cash_ratio = round(cash_and_cash_equivalents / short_term_liabilities,2) if short_term_liabilities else 0
    return_on_sales = round(net_income / sales_revenue,2) if sales_revenue else 0
    return_on_assets = round(net_income / total_assets,2) if total_assets else 0
    return_on_equity = round(net_income / equity,2) if equity else 0
    frequency_of_capital_turnover = round(sales_revenue / total_assets,1) if total_assets else 0
    return_on_investment = round(net_income / (equity + total_liabilities),2) if (equity + total_liabilities) else 0

    
    ebitda_string = f"EBITDA (Earnings Before Interest, Taxes, Depreciation, and Amortization) of {ebitda:,.2f} indicates the company's operational profitability before non-cash charges and capital structure effects."
    ebit_string = f"EBIT (Earnings Before Interest and Taxes) of {ebit:,.2f} represents the company's operating income after subtracting all operational expenses except interest and taxes."
    net_income_string = f"Net Income of {net_income:,.2f} is the company's total earnings after deducting all expenses, including interest and taxes, indicating the company's profitability."
    equity_ratio_string = f"The Equity Ratio of {equity_ratio*100:.2f}% indicates that equity finances {equity_ratio*100:.2f}% of the company's assets, showing the proportion of ownership funding."
    debt_ratio_string = f"The Debt Ratio of {debt_ratio*100:.2f}% shows that {debt_ratio*100:.2f}% of the company's assets are financed through debt, highlighting the leverage level."
    equity_to_fixed_assets_ratio_I_string = f"The Equity to Fixed Assets Ratio I of {equity_to_fixed_assets_ratio_I:.2f} indicates the proportion of equity financing used for non-current assets."
    equity_to_fixed_assets_ratio_II_string = f"The Equity to Fixed Assets Ratio II of {equity_to_fixed_assets_ratio_II:.2f} shows the proportion of equity and long-term liabilities funding non-current assets."
    effective_debt_string = f"Effective Debt of {effective_debt:,.2f} represents the net amount of short and long-term liabilities after considering current assets, highlighting the company's net leverage."
    static_gearing_string = f"Static Gearing of {static_gearing:.2f} indicates the ratio of total liabilities to equity, showing the degree of financial leverage and risk."
    dynamic_gearing_in_years_string = f"Dynamic Gearing in Years of {dynamic_gearing_in_years} years shows how long it would take to pay off the company's net debt using its operating cash flow."
    intensity_of_inventories_string = f"Inventory Intensity of {intensity_of_inventories*100:.2f}% indicates that {intensity_of_inventories*100:.2f}% of the company's assets are tied up in inventories."
    working_capital_string = f"Working Capital of {working_capital:,.2f} represents the excess of current assets over short-term liabilities, indicating the company's short-term financial health."
    property_constitution_string = f"Property Constitution of {property_constitution*100:.2f}% shows that {property_constitution*100:.2f}% of the company's assets are non-current, indicating investment in long-term assets."
    current_ratio_string = f"The Current Ratio of {current_ratio:.2f} indicates that for every dollar of short-term liabilities, the company has {current_ratio:.2f} dollars in current assets, measuring liquidity."
    quick_ratio_string = f"The Quick Ratio of {quick_ratio:.2f} measures the company's ability to meet short-term obligations with its most liquid assets, excluding inventories."
    cash_ratio_string = f"The Cash Ratio of {cash_ratio:.2f} shows the company's ability to cover short-term liabilities with cash and cash equivalents, indicating immediate liquidity."
    return_on_sales_string = f"The Return on Sales of {return_on_sales*100:.2f}% indicates that the company earns {return_on_sales*100:.2f}% net income for every dollar of sales, measuring profitability."
    return_on_assets_string = f"The Return on Assets of {return_on_assets*100:.2f}% shows that the company generates {return_on_assets*100:.2f}% net income for every dollar of assets, assessing asset efficiency."
    return_on_equity_string = f"The Return on Equity of {return_on_equity*100:.2f}% indicates that the company generates {return_on_equity*100:.2f}% net income for every dollar of equity, measuring profitability to shareholders."
    frequency_of_capital_turnover_string = f"The Frequency of Capital Turnover of {frequency_of_capital_turnover:.2f} times indicates how often the company's assets are converted into sales, assessing asset utilization."
    return_on_investment_string = f"The Return on Investment of {return_on_investment*100:.2f}% shows the company's efficiency in using the combined equity and liabilities to generate profits."



    # Return a dictionary instead of a list
    return {
    "non-current assets": non_current_assets,
    "current assets": current_assets,
    "total assets": total_assets,
    "equity": equity,
    "long-term liabilities": long_term_liabilities,
    "short-term liabilities": short_term_liabilities,
    "total liabilities": total_liabilities,
    "Sales revenue": sales_revenue,
    "cost of goods sold (COGS)": cogs,
    "EBITDA": {"value": ebitda, "explanation": ebitda_string},
    "depreciation and amortization": depreciation,
    "EBIT": {"value": ebit, "explanation": ebit_string},
    "Net Income": {"value": net_income, "explanation": net_income_string},
    "Equity Ratio": {"value": equity_ratio, "explanation": equity_ratio_string},
    "Debt Ratio": {"value": debt_ratio, "explanation": debt_ratio_string},
    "Equity to Fixed Assets Ratio I": {"value": equity_to_fixed_assets_ratio_I, "explanation": equity_to_fixed_assets_ratio_I_string},
    "Equity to Fixed Assets Ratio II": {"value": equity_to_fixed_assets_ratio_II, "explanation": equity_to_fixed_assets_ratio_II_string},
    "Effective Debt": {"value": effective_debt, "explanation": effective_debt_string},
    "Static Gearing": {"value": static_gearing, "explanation": static_gearing_string},
    "Dynamic Gearing in Years": {"value": dynamic_gearing_in_years, "explanation": dynamic_gearing_in_years_string},
    "Intensity of Inventories": {"value": intensity_of_inventories, "explanation": intensity_of_inventories_string},
    "Working Capital": {"value": working_capital, "explanation": working_capital_string},
    "Property Constitution": {"value": property_constitution, "explanation": property_constitution_string},
    "Current Ratio": {"value": current_ratio, "explanation": current_ratio_string},
    "Quick Ratio": {"value": quick_ratio, "explanation": quick_ratio_string},
    "Cash Ratio": {"value": cash_ratio, "explanation": cash_ratio_string},
    "Return on Sales": {"value": return_on_sales, "explanation": return_on_sales_string},
    "Return on Assets": {"value": return_on_assets, "explanation": return_on_assets_string},
    "Return on Equity": {"value": return_on_equity, "explanation": return_on_equity_string},
    "Frequency of Capital Turnover": {"value": frequency_of_capital_turnover, "explanation": frequency_of_capital_turnover_string},
    "Return on Investment": {"value": return_on_investment, "explanation": return_on_investment_string}
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
