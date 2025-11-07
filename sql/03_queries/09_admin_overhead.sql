-- 09_admin_overhead.sql - ADMIN OVERHEAD ALLOCATION
-- Hybrid approach: Base + Segment Multiplier + Product Adjustment
-- Matches Python logic exactly

SELECT 
    T.TRANSACTIONID,
    T.CUSTOMERID,
    C.CUSTOMERSEGMENT,
    T.PRODUCTCATEGORY,
    T.TRANSACTIONAMOUNT,
    
    -- STEP 1: CALCULATE BASE OVERHEAD PER TRANSACTION
    -- Total annual overhead: €1,030,000 / 14,488 transactions = €71.15/order
    ROUND(1030000.00 / 14488, 2) AS BASE_OVERHEAD_EUR,
    
    -- STEP 2: SEGMENT MULTIPLIER
    -- SMB: 0.85x, Mid-Market: 1.1x, Enterprise: 1.4x
    CASE 
        WHEN C.CUSTOMERSEGMENT = 'SMB' THEN 0.85
        WHEN C.CUSTOMERSEGMENT = 'Mid-Market' THEN 1.1
        WHEN C.CUSTOMERSEGMENT = 'Enterprise' THEN 1.4
        ELSE 1.0
    END AS SEGMENT_MULTIPLIER,
    
    -- STEP 3: SEGMENT-ADJUSTED OVERHEAD
    ROUND(
        (1030000.00 / 14488) * 
        CASE 
            WHEN C.CUSTOMERSEGMENT = 'SMB' THEN 0.85
            WHEN C.CUSTOMERSEGMENT = 'Mid-Market' THEN 1.1
            WHEN C.CUSTOMERSEGMENT = 'Enterprise' THEN 1.4
            ELSE 1.0
        END,
        2
    ) AS SEGMENT_ADJUSTED_OVERHEAD_EUR,
    
    -- STEP 4: PRODUCT ADJUSTMENT
    -- Fresh: +10, Deli: +8, Milk: +5, Frozen: 0, Grocery: -5, Detergent/Paper: -5
    CASE 
        WHEN T.PRODUCTCATEGORY = 'Fresh' THEN 10.00
        WHEN T.PRODUCTCATEGORY = 'Delicatessen' THEN 8.00
        WHEN T.PRODUCTCATEGORY = 'Milk' THEN 5.00
        WHEN T.PRODUCTCATEGORY = 'Frozen' THEN 0.00
        WHEN T.PRODUCTCATEGORY = 'Grocery' THEN -5.00
        WHEN T.PRODUCTCATEGORY IN ('DetergentsPaper', 'Detergents/Paper') THEN -5.00
        ELSE 0.00
    END AS PRODUCT_ADJUSTMENT_EUR,
    
    -- STEP 5: TOTAL ALLOCATED OVERHEAD (minimum €30)
    GREATEST(
        ROUND(
            (1030000.00 / 14488) * 
            CASE 
                WHEN C.CUSTOMERSEGMENT = 'SMB' THEN 0.85
                WHEN C.CUSTOMERSEGMENT = 'Mid-Market' THEN 1.1
                WHEN C.CUSTOMERSEGMENT = 'Enterprise' THEN 1.4
                ELSE 1.0
            END +
            CASE 
                WHEN T.PRODUCTCATEGORY = 'Fresh' THEN 10.00
                WHEN T.PRODUCTCATEGORY = 'Delicatessen' THEN 8.00
                WHEN T.PRODUCTCATEGORY = 'Milk' THEN 5.00
                WHEN T.PRODUCTCATEGORY = 'Frozen' THEN 0.00
                WHEN T.PRODUCTCATEGORY = 'Grocery' THEN -5.00
                WHEN T.PRODUCTCATEGORY IN ('DetergentsPaper', 'Detergents/Paper') THEN -5.00
                ELSE 0.00
            END,
            2
        ),
        30.00
    ) AS TOTAL_ALLOCATED_OVERHEAD_EUR,
    
    -- STEP 6: OVERHEAD AS % OF REVENUE
    ROUND(
        GREATEST(
            ROUND(
                (1030000.00 / 14488) * 
                CASE 
                    WHEN C.CUSTOMERSEGMENT = 'SMB' THEN 0.85
                    WHEN C.CUSTOMERSEGMENT = 'Mid-Market' THEN 1.1
                    WHEN C.CUSTOMERSEGMENT = 'Enterprise' THEN 1.4
                    ELSE 1.0
                END +
                CASE 
                    WHEN T.PRODUCTCATEGORY = 'Fresh' THEN 10.00
                    WHEN T.PRODUCTCATEGORY = 'Delicatessen' THEN 8.00
                    WHEN T.PRODUCTCATEGORY = 'Milk' THEN 5.00
                    WHEN T.PRODUCTCATEGORY = 'Frozen' THEN 0.00
                    WHEN T.PRODUCTCATEGORY = 'Grocery' THEN -5.00
                    WHEN T.PRODUCTCATEGORY IN ('DetergentsPaper', 'Detergents/Paper') THEN -5.00
                    ELSE 0.00
                END,
                2
            ),
            30.00
        ) / T.TRANSACTIONAMOUNT * 100,
        2
    ) AS OVERHEAD_AS_PCT_OF_REVENUE
    
FROM B2B_PROFITABILITY.PUBLIC.TRANSACTIONS_GENERATED T
JOIN B2B_PROFITABILITY.PUBLIC.CUSTOMER_MASTER C ON T.CUSTOMERID = C.CUSTOMERID
ORDER BY T.TRANSACTIONID
