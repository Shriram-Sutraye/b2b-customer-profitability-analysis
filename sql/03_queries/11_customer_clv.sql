-- 11_customer_clv.sql - CUSTOMER LIFETIME VALUE ANALYSIS
-- Strategic segmentation: A/B/C customers + action recommendations
-- Matches Python logic exactly

SELECT 
    C.CUSTOMERID,
    C.CUSTOMERNAME,
    C.CUSTOMERSEGMENT,
    
    -- STEP 1: ANNUAL PROFIT PER CUSTOMER
    ROUND(COALESCE(SUM(PL.PROFIT_EUR), 0), 2) AS ANNUALPROFIT_EUR,
    COUNT(DISTINCT PL.TRANSACTIONID) AS ORDERCOUNT,
    
    -- STEP 2: EXPECTED LIFETIME (years)
    CASE 
        WHEN C.CUSTOMERSEGMENT = 'SMB' THEN 2.5
        WHEN C.CUSTOMERSEGMENT = 'Mid-Market' THEN 6.0
        WHEN C.CUSTOMERSEGMENT = 'Enterprise' THEN 12.0
        ELSE 2.5
    END AS EXPECTEDLIFETIME_YEARS,
    
    -- STEP 3: ACQUISITION COST (one-time)
    CASE 
        WHEN C.CUSTOMERSEGMENT = 'SMB' THEN 300
        WHEN C.CUSTOMERSEGMENT = 'Mid-Market' THEN 2000
        WHEN C.CUSTOMERSEGMENT = 'Enterprise' THEN 10000
        ELSE 300
    END AS ACQUISITIONCOST_EUR,
    
    -- STEP 4: CALCULATE CLV = (Annual Profit × Lifetime Years) - Acquisition Cost
    ROUND(
        (COALESCE(SUM(PL.PROFIT_EUR), 0) * 
            CASE 
                WHEN C.CUSTOMERSEGMENT = 'SMB' THEN 2.5
                WHEN C.CUSTOMERSEGMENT = 'Mid-Market' THEN 6.0
                WHEN C.CUSTOMERSEGMENT = 'Enterprise' THEN 12.0
                ELSE 2.5
            END) -
        CASE 
            WHEN C.CUSTOMERSEGMENT = 'SMB' THEN 300
            WHEN C.CUSTOMERSEGMENT = 'Mid-Market' THEN 2000
            WHEN C.CUSTOMERSEGMENT = 'Enterprise' THEN 10000
            ELSE 300
        END,
        2
    ) AS CLV_EUR,
    
    -- STEP 5: PAYBACK MULTIPLE (how many times acquisition cost)
    ROUND(
        ((COALESCE(SUM(PL.PROFIT_EUR), 0) * 
            CASE 
                WHEN C.CUSTOMERSEGMENT = 'SMB' THEN 2.5
                WHEN C.CUSTOMERSEGMENT = 'Mid-Market' THEN 6.0
                WHEN C.CUSTOMERSEGMENT = 'Enterprise' THEN 12.0
                ELSE 2.5
            END) -
        CASE 
            WHEN C.CUSTOMERSEGMENT = 'SMB' THEN 300
            WHEN C.CUSTOMERSEGMENT = 'Mid-Market' THEN 2000
            WHEN C.CUSTOMERSEGMENT = 'Enterprise' THEN 10000
            ELSE 300
        END) /
        CASE 
            WHEN C.CUSTOMERSEGMENT = 'SMB' THEN 300
            WHEN C.CUSTOMERSEGMENT = 'Mid-Market' THEN 2000
            WHEN C.CUSTOMERSEGMENT = 'Enterprise' THEN 10000
            ELSE 300
        END,
        2
    ) AS PAYBACKMULTIPLE,
    
    -- STEP 6: CLV CLASSIFICATION
    CASE 
        WHEN (COALESCE(SUM(PL.PROFIT_EUR), 0) * 
            CASE 
                WHEN C.CUSTOMERSEGMENT = 'SMB' THEN 2.5
                WHEN C.CUSTOMERSEGMENT = 'Mid-Market' THEN 6.0
                WHEN C.CUSTOMERSEGMENT = 'Enterprise' THEN 12.0
                ELSE 2.5
            END) -
        CASE 
            WHEN C.CUSTOMERSEGMENT = 'SMB' THEN 300
            WHEN C.CUSTOMERSEGMENT = 'Mid-Market' THEN 2000
            WHEN C.CUSTOMERSEGMENT = 'Enterprise' THEN 10000
            ELSE 300
        END > 5000 THEN 'A-Customer'
        WHEN (COALESCE(SUM(PL.PROFIT_EUR), 0) * 
            CASE 
                WHEN C.CUSTOMERSEGMENT = 'SMB' THEN 2.5
                WHEN C.CUSTOMERSEGMENT = 'Mid-Market' THEN 6.0
                WHEN C.CUSTOMERSEGMENT = 'Enterprise' THEN 12.0
                ELSE 2.5
            END) -
        CASE 
            WHEN C.CUSTOMERSEGMENT = 'SMB' THEN 300
            WHEN C.CUSTOMERSEGMENT = 'Mid-Market' THEN 2000
            WHEN C.CUSTOMERSEGMENT = 'Enterprise' THEN 10000
            ELSE 300
        END > 0 THEN 'B-Customer'
        ELSE 'C-Customer'
    END AS CLVSEGMENT,
    
    -- STEP 7: RECOMMENDED ACTION
    CASE 
        WHEN (COALESCE(SUM(PL.PROFIT_EUR), 0) * 
            CASE 
                WHEN C.CUSTOMERSEGMENT = 'SMB' THEN 2.5
                WHEN C.CUSTOMERSEGMENT = 'Mid-Market' THEN 6.0
                WHEN C.CUSTOMERSEGMENT = 'Enterprise' THEN 12.0
                ELSE 2.5
            END) -
        CASE 
            WHEN C.CUSTOMERSEGMENT = 'SMB' THEN 300
            WHEN C.CUSTOMERSEGMENT = 'Mid-Market' THEN 2000
            WHEN C.CUSTOMERSEGMENT = 'Enterprise' THEN 10000
            ELSE 300
        END > 5000 THEN 'INVEST & EXPAND'
        WHEN (COALESCE(SUM(PL.PROFIT_EUR), 0) * 
            CASE 
                WHEN C.CUSTOMERSEGMENT = 'SMB' THEN 2.5
                WHEN C.CUSTOMERSEGMENT = 'Mid-Market' THEN 6.0
                WHEN C.CUSTOMERSEGMENT = 'Enterprise' THEN 12.0
                ELSE 2.5
            END) -
        CASE 
            WHEN C.CUSTOMERSEGMENT = 'SMB' THEN 300
            WHEN C.CUSTOMERSEGMENT = 'Mid-Market' THEN 2000
            WHEN C.CUSTOMERSEGMENT = 'Enterprise' THEN 10000
            ELSE 300
        END > 0 THEN 'MAINTAIN & MONITOR'
        WHEN (COALESCE(SUM(PL.PROFIT_EUR), 0) * 
            CASE 
                WHEN C.CUSTOMERSEGMENT = 'SMB' THEN 2.5
                WHEN C.CUSTOMERSEGMENT = 'Mid-Market' THEN 6.0
                WHEN C.CUSTOMERSEGMENT = 'Enterprise' THEN 12.0
                ELSE 2.5
            END) -
        CASE 
            WHEN C.CUSTOMERSEGMENT = 'SMB' THEN 300
            WHEN C.CUSTOMERSEGMENT = 'Mid-Market' THEN 2000
            WHEN C.CUSTOMERSEGMENT = 'Enterprise' THEN 10000
            ELSE 300
        END < -1000 THEN 'EXIT IMMEDIATELY'
        ELSE 'RENEGOTIATE TERMS'
    END AS RECOMMENDEDACTION
    
FROM B2B_PROFITABILITY.PUBLIC.CUSTOMER_MASTER C
LEFT JOIN B2B_PROFITABILITY.PUBLIC.10_FINANCIAL_P_L_ORDERS PL ON C.CUSTOMERID = PL.CUSTOMERID
GROUP BY C.CUSTOMERID, C.CUSTOMERNAME, C.CUSTOMERSEGMENT
ORDER BY CLV_EUR DESC
