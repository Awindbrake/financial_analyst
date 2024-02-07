from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(
    title="Financial Analysis",
    description="Performs basic financial analysis and calculates key financial ratios.",
    version="1.0.0",
    servers=[
        {
            "url": "https://financial-analysis.herokuapp.com",
            "description": "Financial Analysis API"
        }
    ]
)

class FinancialData(BaseModel):
    current_assets: float = Field(..., gt=0, description="Total current assets.")
    non_current_assets: float = Field(..., gt=0, description="Total non-current assets.")
    equity: float = Field(..., gt=0, description="Total equity.")
    current_liabilities: float = Field(..., gt=0, description="Total current liabilities.")
    non_current_liabilities: float = Field(..., gt=0, description="Total non-current liabilities.")
    sales_revenues: float = Field(..., gt=0, description="Total sales revenues.")
    cogs: float = Field(..., gt=0, description="Total cost of goods sold.")

def calculate_earnings(sales_revenues: float, cogs: float) -> float:
    return sales_revenues - cogs

def calculate_return_on_equity(earnings: float, equity: float) -> float:
    return earnings / equity

@app.post("/analyze")
async def analyze_financials(data: FinancialData):
    earnings = calculate_earnings(data.sales_revenues, data.cogs)
    return_on_equity = calculate_return_on_equity(earnings, data.equity)
    return {
        "earnings": earnings,
        "return_on_equity": return_on_equity
    }

@app.get("/")
def read_root():
    return {"message": "Welcome to the Financial Analysis API. Visit /docs for documentation."}
