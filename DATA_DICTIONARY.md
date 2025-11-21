# Data Dictionary

This document provides a detailed reference for the datasets generated in the **B2B Customer Profitability Analysis** project. It covers the schema, data types, and business logic used for each field.

## 1. Customer Master (`01_customer_master.csv`)
**Source:** `python/02_data_generation/02_customer_master_generation.py`
**Description:** Core customer reference data, including demographics, segmentation, and service complexity drivers.

| Column Name | Data Type | Description | Logic / Notes |
| :--- | :--- | :--- | :--- |
| `CustomerID` | String | Unique identifier (e.g., `CUST-001`) | Sequential |
| `CustomerName` | String | Company name | Generated (Faker) |
| `OriginalChannel` | Integer | UCI Channel ID | 1=HORECA, 2=Retail |
| `ChannelName` | String | Business channel name | Mapped from `OriginalChannel` |
| `OriginalRegion` | Integer | UCI Region ID | 1=Lisbon, 2=Porto, 3=Other |
| `RegionName` | String | Geographic region name | Mapped from `OriginalRegion` |
| `AnnualFreshSpending` | Float | Annual spend on Fresh products | From UCI dataset |
| `AnnualMilkSpending` | Float | Annual spend on Milk products | From UCI dataset |
| `AnnualGrocerySpending` | Float | Annual spend on Grocery products | From UCI dataset |
| `AnnualFrozenSpending` | Float | Annual spend on Frozen products | From UCI dataset |
| `AnnualDetergentsPaperSpending` | Float | Annual spend on Detergents/Paper | From UCI dataset |
| `AnnualDelicatessenSpending` | Float | Annual spend on Delicatessen | From UCI dataset |
| `TotalAnnualRevenue` | Float | Total annual revenue from customer | Sum of all 6 categories |
| `CustomerSegment` | String | Strategic segment | SMB (<€20k), Mid-Market (€20-50k), Enterprise (>€50k) |
| `PaymentTerms` | String | Payment terms (Days Sales Outstanding) | Net-30, Net-60, Net-90. 88% Segment-based, 12% Random. |
| `OrderFrequencyPerMonth` | Float | Avg orders per month | HORECA (3-5/mo), Retail (0.5-2/mo) |
| `ServiceIntensityScore` | Float | Complexity score (1-10) | Based on Channel, Frequency, Terms |
| `ServiceIntensityDrivers` | String | Explanation of intensity score | Text description of drivers |
| `HasPremiumRequests` | Boolean | Flag for premium service needs | True if Score > 6 |
| `DaysAsCustomer` | Integer | Customer tenure in days | Random (1-3 years) |
| `AcquisitionDate` | Date | Date customer was acquired | Calculated from `DaysAsCustomer` |
| `SalesRepAssigned` | String | Assigned sales representative | Random (REP-01 to REP-25) |
| `AccountTier` | String | Service tier | PREMIUM (Score≥7), STANDARD, ENTERPRISE (Rev>50k) |

---

## 2. Transactions (`02_transactions_generated.csv`)
**Source:** `python/02_data_generation/02_generate_transactions.py`
**Description:** Line-item transaction data with seasonality and order characteristics.

| Column Name | Data Type | Description | Logic / Notes |
| :--- | :--- | :--- | :--- |
| `TransactionID` | String | Unique transaction ID | Format: `TXN-2023-XXXXXX` |
| `CustomerID` | String | Foreign key to Customer Master | |
| `TransactionDate` | Date | Date of order | Deterministic seasonality applied |
| `OrderMonth` | Integer | Month of order (1-12) | Used for seasonality logic |
| `OrderDayOfWeek` | String | Day of week | Random |
| `ProductCategory` | String | Product category | Weighted by customer's category spend |
| `TransactionAmount` | Float | Revenue for this line item | Derived from spend & seasonality |
| `Quantity` | Integer | Units ordered | Amount / ~€25 |
| `NumberOfLineItems` | Integer | Complexity proxy | Random 1-6 |
| `IsStandardOrder` | Boolean | Standard vs Custom order | Based on Channel parameters |
| `IsUrgent` | Boolean | Urgency flag | Based on Channel parameters |
| `CustomerServiceInteractionRequired` | Boolean | Support flag | Based on Channel parameters |
| `OrderIntensityLevel` | String | Operational complexity | Low, Medium, High |
| `ServiceCostMultiplier` | Float | Cost multiplier for operations | Derived from intensity flags (1.0 - 1.8x) |

---

## 3. Product Catalog (`03_products_generated.csv`)
**Source:** `python/02_data_generation/03_generate_products.py`
**Description:** Catalog of 275 SKUs with pricing, margins, and physical attributes.

| Column Name | Data Type | Description | Logic / Notes |
| :--- | :--- | :--- | :--- |
| `SKU` | String | Unique Product ID | Format: `SKU-CAT-XXXX` |
| `ProductName` | String | Product Name | Example or Generated |
| `Category` | String | Product Category | 6 major categories |
| `UnitCost` | Float | Wholesale cost (COGS basis) | Random range by category |
| `ListPrice` | Float | Retail price | Cost * Markup |
| `Weight_kg` | Float | Physical weight | Used for shipping/handling costs |
| `IsPerishable` | Boolean | Spoilage risk flag | True for Fresh, Milk, Deli, Frozen |
| `ReturnRate_Percent` | Float | Expected return rate | Varies by category (0.1% - 12%) |
| `GrossMargin_Percent` | Float | Theoretical margin | ((Price - Cost) / Price) % |
| `Markup_Multiplier` | Float | Price markup factor | Range 1.2x - 2.0x |

---

## 4. Warehouse Costs (`04_warehouse_costs_generated.csv`)
**Source:** `python/02_data_generation/04_generate_warehouse_costs.py`
**Description:** Detailed Activity-Based Costing (ABC) for warehouse operations.

| Column Name | Data Type | Description | Logic / Notes |
| :--- | :--- | :--- | :--- |
| `TransactionID` | String | FK to Transactions | |
| `PickPackCost_EUR` | Float | Picking & packing labor | €5.50-7.50 per item * LineItems |
| `ReceivingCost_EUR` | Float | Inbound handling | Flat €5.00 per order |
| `PutawayCost_EUR` | Float | Stocking labor | €0.65 per unit |
| `StorageCost_EUR` | Float | Occupancy cost | Weight * Duration * Rate |
| `IndirectLaborCost_EUR` | Float | Supervision/Mgmt | 15% of direct labor |
| `InboundTransportCost_EUR` | Float | Freight in | Flat €10.00 per order |
| `ShrinkageCost_EUR` | Float | Spoilage/Theft | % of value (0.5% - 8%) |
| `ReturnsCost_EUR` | Float | Handling returned items | Varies by Category & Custom flag |
| `EquipmentTechCost_EUR` | Float | Forklifts/Scanners/IT | 5% of subtotal |
| `ColdChainMultiplier` | Float | Energy cost factor | 1.5x for perishable, 1.0x others |
| `TotalWarehouseOperationsCost_EUR` | Float | **Total Warehouse Cost** | Sum of all components * Multipliers |

---

## 5. Shipping Costs (`05_shipping_costs_generated.csv`)
**Source:** `python/02_data_generation/05_generate_shipping_costs.py`
**Description:** Outbound logistics costs (Only applies to Custom orders; Standard = €0).

| Column Name | Data Type | Description | Logic / Notes |
| :--- | :--- | :--- | :--- |
| `TransactionID` | String | FK to Transactions | |
| `IsStandardOrder` | Boolean | Shipping trigger | If True, Cost = 0 (Customer pays) |
| `BaseShippingCost_EUR` | Float | Base transport fee | €20.00 (if Custom) |
| `WeightSurchargeCost_EUR` | Float | Heavy order fee | €0.75 per kg |
| `ColdChainPremium_EUR` | Float | Refrigerated truck fee | €15-20 for Fresh/Milk/Deli |
| `UrgencyPremium_EUR` | Float | Expedited fee | €20.00 (if Urgent) |
| `TotalShippingCost_EUR` | Float | **Total Shipping Cost** | Sum of components |

---

## 6. Returns Handling (`06_returns_handling_generated.csv`)
**Source:** `python/02_data_generation/06_generate_returns_handling.py`
**Description:** Reverse logistics, QC, and inventory loss from returns.

| Column Name | Data Type | Description | Logic / Notes |
| :--- | :--- | :--- | :--- |
| `TransactionID` | String | FK to Transactions | |
| `IsReturned` | Boolean | Return flag | Probabilistic based on Category rates |
| `ReturnReason` | String | Reason code | OurError, ShippingDamage, Complaint, Quality |
| `ResponsibilityPercentage` | Float | Cost share we pay | 50% - 100% |
| `ReverseShippingCost_EUR` | Float | Transport back | €20 base + €5 cold chain (if Custom) |
| `ReceivingCost_EUR` | Float | Handling labor | €2.50 |
| `QCCost_EUR` | Float | Inspection labor | €2.50 |
| `RestockingCost_EUR` | Float | Put-back labor | €0.33 per kg (for 50% of weight) |
| `DisposalCost_EUR` | Float | Trash/Recycle fee | €0.20 per kg (for scrap portion) |
| `ResellableValue_EUR` | Float | Value recovered | 60% of amount |
| `DiscountedLoss_EUR` | Float | Value lost (discount) | 20% of amount * 40% markdown |
| `ScrapLoss_EUR` | Float | Value lost (scrap) | 20% of amount (100% loss) |
| `TotalReturnExpense_EUR` | Float | **Total Return Cost** | Ops Costs + Inventory Loss |

---

## 7. Payment Terms & Interest (`07_payment_terms_interest_generated.csv`)
**Source:** `python/02_data_generation/07_generate_payment_terms_interest.py`
**Description:** Financing costs for working capital (Days Sales Outstanding).

| Column Name | Data Type | Description | Logic / Notes |
| :--- | :--- | :--- | :--- |
| `TransactionID` | String | FK to Transactions | |
| `PaymentTerms` | String | Terms code | Net-30, Net-60, Net-90 |
| `DSO_Days` | Integer | Days Sales Outstanding | 30, 60, or 90 |
| `AnnualInterestRate` | Float | Cost of Capital | 5.0% |
| `DSO_InterestCost_EUR` | Float | **Financing Cost** | (Amount * DSO * 5%) / 365 |

---

## 9. Admin Overhead (`09_admin_overhead_generated.csv`)
**Source:** `python/02_data_generation/09_generate_admin_overhead.py`
**Description:** Allocation of corporate fixed costs (Salaries, Rent, IT, etc.).

| Column Name | Data Type | Description | Logic / Notes |
| :--- | :--- | :--- | :--- |
| `TransactionID` | String | FK to Transactions | |
| `BaseOverhead_EUR` | Float | Flat allocation | Total Overhead / Total Txns |
| `SegmentMultiplier` | Float | Segment weighting | SMB (0.85x), Mid (1.1x), Ent (1.4x) |
| `ProductAdjustment_EUR` | Float | Category complexity | +€10 Fresh, -€5 Grocery, etc. |
| `TotalAllocatedOverhead_EUR`| Float | **Allocated Overhead** | (Base * Multiplier) + Adjustment (Min €30) |

---

## 10. Financial P&L (`10_financial_p_l_orders.csv`)
**Source:** `python/02_data_generation/10_generate_financial_p_l.py`
**Description:** Master dataset combining all revenues and costs for Net Profit calculation.

| Column Name | Data Type | Description | Formula |
| :--- | :--- | :--- | :--- |
| `TransactionAmount` | Float | Gross Revenue | |
| `COGS_EUR` | Float | Cost of Goods Sold | 60% of Revenue (Standard estimate) |
| `WarehouseCost_EUR` | Float | Ops Cost | From Dataset 4 |
| `ShippingCost_EUR` | Float | Logistics Cost | From Dataset 5 |
| `ReturnsCost_EUR` | Float | Returns Cost | From Dataset 6 |
| `InterestCost_EUR` | Float | Financing Cost | From Dataset 7 |
| `OverheadCost_EUR` | Float | Admin Cost | From Dataset 9 |
| `TotalCost_EUR` | Float | **Total Cost-to-Serve** | Sum of all costs above |
| `Profit_EUR` | Float | **Net Profit** | Revenue - Total Cost |
| `ProfitMargin_Pct` | Float | Net Margin % | (Profit / Revenue) * 100 |
| `ProfitabilityCategory` | String | Label | Loss, Breakeven, Profitable, Highly Profitable |
| `ShouldRaisePrice` | Boolean | Action Flag | True if Profit < 0 |
| `ShouldReduceCost` | Boolean | Action Flag | True if Cost/Rev > 95% |
| `ShouldReviewCustomer` | Boolean | Action Flag | True if either above is True |

---

## 11. Customer Lifetime Value (`11_customer_lifetime_value.csv`)
**Source:** `python/02_data_generation/11_generate_customer_lifetime_value.py`
**Description:** Long-term value analysis for strategic segmentation.

| Column Name | Data Type | Description | Logic / Notes |
| :--- | :--- | :--- | :--- |
| `CustomerID` | String | Unique ID | |
| `AnnualProfit_EUR` | Float | Total Profit (Year 1) | Sum of P&L Profit |
| `ExpectedLifetime_Years`| Float | Retention estimate | SMB (2.5), Mid (6.0), Ent (12.0) |
| `AcquisitionCost_EUR` | Float | CAC estimate | SMB (€300), Mid (€2k), Ent (€10k) |
| `CLV_EUR` | Float | **Lifetime Value** | (AnnualProfit * Years) - CAC |
| `CLVSegment` | String | Strategic Tier | A-Customer (>€5k), B-Customer (>0), C-Customer (<0) |
| `RecommendedAction` | String | Strategy | INVEST, MAINTAIN, RENEGOTIATE, EXIT |

---

## 14. Scenario Planning (`14_scenario_planning.csv`)
**Source:** `python/02_data_generation/14_generate_scenario_planning.py`
**Description:** Simulated outcomes of 5 strategic options.

| Column Name | Data Type | Description | Notes |
| :--- | :--- | :--- | :--- |
| `Scenario` | String | Scenario Name | Status Quo, Exit C, Renegotiate C, etc. |
| `Customers_Kept` | Integer | Count of retained customers | |
| `Profit_EUR` | Float | Projected Total Profit | |
| `Margin_Pct` | Float | Projected Net Margin | |
| `Risk_Level` | String | Risk Assessment | LOW, MEDIUM, HIGH, EXTREME |
| `Recommendation` | String | Final Verdict | OPTIMAL, SAFE, RISKY, UNSUSTAINABLE |
