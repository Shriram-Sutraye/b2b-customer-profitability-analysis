-- 07_payment_terms_interest.sql - MATCHES PYTHON LOGIC EXACTLY
-- Generates payment terms based on customer segment
-- Logic: 12% random outliers + 88% segment-based distribution
-- SMB: 71% Net-30, 17% Net-60, 12% Net-90
-- Mid-Market: 34% Net-30, 46% Net-60, 20% Net-90
-- Enterprise: 67% Net-30, 32% Net-60, 1% Net-90
-- Calculates DSO interest cost (5% annual rate)

SELECT 
    T.TRANSACTIONID,
    T.CUSTOMERID,
    C.CUSTOMERSEGMENT,
    T.TRANSACTIONAMOUNT,
    
    -- STEP 1: GENERATE PAYMENT TERMS based on customer segment
    -- Logic: 12% random (any term) + 88% by segment
    CASE 
        -- 12% RANDOM OUTLIERS (distribute randomly across all terms)
        WHEN (ABS(HASH(T.TRANSACTIONID)) % 100) < 12 THEN
            CASE WHEN (ABS(HASH(T.TRANSACTIONID)) % 3) = 0 THEN 'Net-30'
                 WHEN (ABS(HASH(T.TRANSACTIONID)) % 3) = 1 THEN 'Net-60'
                 ELSE 'Net-90'
            END
        
        -- 88% SEGMENT-BASED DISTRIBUTION
        -- SMB: 80% Net-30, 15% Net-60, 5% Net-90 (from Python adjusted to 71/17/12)
        WHEN C.CUSTOMERSEGMENT = 'SMB' THEN
            CASE WHEN (ABS(HASH(T.TRANSACTIONID)) % 100) < 71 THEN 'Net-30'
                 WHEN (ABS(HASH(T.TRANSACTIONID)) % 100) < 88 THEN 'Net-60'
                 ELSE 'Net-90'
            END
        
        -- MID-MARKET: 40% Net-30, 45% Net-60, 15% Net-90 (from Python adjusted to 34/46/20)
        WHEN C.CUSTOMERSEGMENT = 'Mid-Market' THEN
            CASE WHEN (ABS(HASH(T.TRANSACTIONID)) % 100) < 34 THEN 'Net-30'
                 WHEN (ABS(HASH(T.TRANSACTIONID)) % 100) < 80 THEN 'Net-60'
                 ELSE 'Net-90'
            END
        
        -- ENTERPRISE: 20% Net-30, 40% Net-60, 40% Net-90 (from Python adjusted to 67/32/1)
        WHEN C.CUSTOMERSEGMENT = 'Enterprise' THEN
            CASE WHEN (ABS(HASH(T.TRANSACTIONID)) % 100) < 67 THEN 'Net-30'
                 WHEN (ABS(HASH(T.TRANSACTIONID)) % 100) < 99 THEN 'Net-60'
                 ELSE 'Net-90'
            END
        
        ELSE 'Net-30'
    END AS PAYMENT_TERMS,
    
    -- STEP 2: MAP PAYMENT TERMS TO DSO DAYS
    CASE 
        WHEN (ABS(HASH(T.TRANSACTIONID)) % 100) < 12 THEN
            CASE WHEN (ABS(HASH(T.TRANSACTIONID)) % 3) = 0 THEN 30
                 WHEN (ABS(HASH(T.TRANSACTIONID)) % 3) = 1 THEN 60
                 ELSE 90
            END
        WHEN C.CUSTOMERSEGMENT = 'SMB' THEN
            CASE WHEN (ABS(HASH(T.TRANSACTIONID)) % 100) < 71 THEN 30
                 WHEN (ABS(HASH(T.TRANSACTIONID)) % 100) < 88 THEN 60
                 ELSE 90
            END
        WHEN C.CUSTOMERSEGMENT = 'Mid-Market' THEN
            CASE WHEN (ABS(HASH(T.TRANSACTIONID)) % 100) < 34 THEN 30
                 WHEN (ABS(HASH(T.TRANSACTIONID)) % 100) < 80 THEN 60
                 ELSE 90
            END
        WHEN C.CUSTOMERSEGMENT = 'Enterprise' THEN
            CASE WHEN (ABS(HASH(T.TRANSACTIONID)) % 100) < 67 THEN 30
                 WHEN (ABS(HASH(T.TRANSACTIONID)) % 100) < 99 THEN 60
                 ELSE 90
            END
        ELSE 30
    END AS DSO_DAYS,
    
    -- STEP 3: CALCULATE INTEREST COSTS
    -- Formula: (Order Value × DSO Days × Annual Interest Rate) / 365
    -- Annual Interest Rate: 5%
    ROUND(T.TRANSACTIONAMOUNT * 0.05, 2) AS ANNUAL_INTEREST_COST_EUR,
    
    ROUND((T.TRANSACTIONAMOUNT * 0.05) / 365, 4) AS DAILY_INTEREST_COST_EUR,
    
    ROUND(
        (T.TRANSACTIONAMOUNT * 0.05 / 365) * 
        CASE 
            WHEN (ABS(HASH(T.TRANSACTIONID)) % 100) < 12 THEN
                CASE WHEN (ABS(HASH(T.TRANSACTIONID)) % 3) = 0 THEN 30
                     WHEN (ABS(HASH(T.TRANSACTIONID)) % 3) = 1 THEN 60
                     ELSE 90
                END
            WHEN C.CUSTOMERSEGMENT = 'SMB' THEN
                CASE WHEN (ABS(HASH(T.TRANSACTIONID)) % 100) < 71 THEN 30
                     WHEN (ABS(HASH(T.TRANSACTIONID)) % 100) < 88 THEN 60
                     ELSE 90
                END
            WHEN C.CUSTOMERSEGMENT = 'Mid-Market' THEN
                CASE WHEN (ABS(HASH(T.TRANSACTIONID)) % 100) < 34 THEN 30
                     WHEN (ABS(HASH(T.TRANSACTIONID)) % 100) < 80 THEN 60
                     ELSE 90
                END
            WHEN C.CUSTOMERSEGMENT = 'Enterprise' THEN
                CASE WHEN (ABS(HASH(T.TRANSACTIONID)) % 100) < 67 THEN 30
                     WHEN (ABS(HASH(T.TRANSACTIONID)) % 100) < 99 THEN 60
                     ELSE 90
                END
            ELSE 30
        END,
        2
    ) AS DSO_INTEREST_COST_EUR
    
FROM B2B_PROFITABILITY.PUBLIC.TRANSACTIONS_GENERATED T
JOIN B2B_PROFITABILITY.PUBLIC.CUSTOMER_MASTER C ON T.CUSTOMERID = C.CUSTOMERID
ORDER BY T.TRANSACTIONID
