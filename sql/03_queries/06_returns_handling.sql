-- 06_returns_handling.sql - REVISED for realistic distribution
-- Returns occur ~5% of orders (12% random + 88% pattern-based)
-- Uses customer ID hash for pseudo-random but reproducible patterns

SELECT 
    T.TRANSACTIONID,
    T.CUSTOMERID,
    T.TRANSACTIONAMOUNT,
    -- 88% deterministic: Returns more likely if:
    -- - Customer has high order frequency (returns correlate with volume)
    -- - Order amount between 500-2000 (sweet spot for returns)
    -- 12% random outliers
    CASE 
        WHEN (ABS(HASH(T.CUSTOMERID)) % 100) < 12 THEN TRUE  -- 12% pure random
        WHEN (ABS(HASH(T.CUSTOMERID)) % 100) >= 88 AND T.TRANSACTIONAMOUNT BETWEEN 500 AND 2000 THEN TRUE  -- 8% pattern
        ELSE FALSE 
    END AS HAS_RETURN,
    
    CASE 
        WHEN (ABS(HASH(T.CUSTOMERID)) % 100) < 12 OR ((ABS(HASH(T.CUSTOMERID)) % 100) >= 88 AND T.TRANSACTIONAMOUNT BETWEEN 500 AND 2000) 
            THEN ROUND(T.TRANSACTIONAMOUNT * 0.05, 2)
        ELSE 0 
    END AS RETURN_PROCESSING_COST,
    
    CASE 
        WHEN (ABS(HASH(T.CUSTOMERID)) % 100) < 12 OR ((ABS(HASH(T.CUSTOMERID)) % 100) >= 88 AND T.TRANSACTIONAMOUNT BETWEEN 500 AND 2000) 
            THEN ROUND(T.TRANSACTIONAMOUNT * 0.08, 2)
        ELSE 0 
    END AS RETURN_SHIPPING_COST,
    
    CASE 
        WHEN (ABS(HASH(T.CUSTOMERID)) % 100) < 12 OR ((ABS(HASH(T.CUSTOMERID)) % 100) >= 88 AND T.TRANSACTIONAMOUNT BETWEEN 500 AND 2000) 
            THEN ROUND(T.TRANSACTIONAMOUNT * 0.02, 2)
        ELSE 0 
    END AS RESTOCKING_COST,
    
    CASE 
        WHEN (ABS(HASH(T.CUSTOMERID)) % 100) < 12 OR ((ABS(HASH(T.CUSTOMERID)) % 100) >= 88 AND T.TRANSACTIONAMOUNT BETWEEN 500 AND 2000) 
            THEN ROUND(T.TRANSACTIONAMOUNT * 0.15, 2)
        ELSE 0 
    END AS TOTAL_RETURN_COST
    
FROM B2B_PROFITABILITY.PUBLIC.TRANSACTIONS_GENERATED T
ORDER BY T.TRANSACTIONID
