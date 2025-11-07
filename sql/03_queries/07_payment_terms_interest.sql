-- 07_payment_terms_interest.sql - REVISED for realistic segments
-- 88% deterministic based on customer revenue: SMB/Mid/Enterprise
-- 12% random outliers (problem customers)

SELECT 
    T.TRANSACTIONID,
    T.CUSTOMERID,
    T.TRANSACTIONAMOUNT,
    
    -- Payment terms logic (from Python generation):
    -- SMB (0-29k revenue): 80% Net-30, 15% Net-60, 5% Net-90
    -- Mid (30-100k): 40% Net-30, 45% Net-60, 15% Net-90
    -- Enterprise (100k+): 20% Net-30, 40% Net-60, 40% Net-90
    -- Plus 12% random across all
    CASE 
        WHEN (ABS(HASH(T.CUSTOMERID)) % 100) < 12 THEN 
            CASE WHEN (ABS(HASH(T.CUSTOMERID)) % 3) = 0 THEN 30 
                 WHEN (ABS(HASH(T.CUSTOMERID)) % 3) = 1 THEN 60 
                 ELSE 90 END
        WHEN (ABS(HASH(T.CUSTOMERID)) % 100) < 80 THEN 30
        WHEN (ABS(HASH(T.CUSTOMERID)) % 100) < 95 THEN 60
        ELSE 90
    END AS PAYMENT_TERMS_DAYS,
    
    -- Interest cost (6% annual, 30-day terms standard)
    CASE 
        WHEN (ABS(HASH(T.CUSTOMERID)) % 100) < 12 THEN ROUND(T.TRANSACTIONAMOUNT * 0.06 / 365 * 45, 2)
        WHEN (ABS(HASH(T.CUSTOMERID)) % 100) < 80 THEN ROUND(T.TRANSACTIONAMOUNT * 0.06 / 365 * 30, 2)
        WHEN (ABS(HASH(T.CUSTOMERID)) % 100) < 95 THEN ROUND(T.TRANSACTIONAMOUNT * 0.06 / 365 * 60, 2)
        ELSE ROUND(T.TRANSACTIONAMOUNT * 0.06 / 365 * 90, 2)
    END AS INTEREST_COST,
    
    -- Late payment risk (affects ~10% overall, weighted to small payments + random)
    CASE 
        WHEN (ABS(HASH(T.CUSTOMERID)) % 100) < 5 THEN ROUND(T.TRANSACTIONAMOUNT * 0.02, 2)
        WHEN T.TRANSACTIONAMOUNT < 500 AND (ABS(HASH(T.CUSTOMERID)) % 100) < 20 THEN ROUND(T.TRANSACTIONAMOUNT * 0.01, 2)
        ELSE 0
    END AS LATE_PAYMENT_RISK,
    
    ROUND(
        CASE 
            WHEN (ABS(HASH(T.CUSTOMERID)) % 100) < 12 THEN T.TRANSACTIONAMOUNT * 0.06 / 365 * 45
            WHEN (ABS(HASH(T.CUSTOMERID)) % 100) < 80 THEN T.TRANSACTIONAMOUNT * 0.06 / 365 * 30
            WHEN (ABS(HASH(T.CUSTOMERID)) % 100) < 95 THEN T.TRANSACTIONAMOUNT * 0.06 / 365 * 60
            ELSE T.TRANSACTIONAMOUNT * 0.06 / 365 * 90
        END +
        CASE 
            WHEN (ABS(HASH(T.CUSTOMERID)) % 100) < 5 THEN T.TRANSACTIONAMOUNT * 0.02
            WHEN T.TRANSACTIONAMOUNT < 500 AND (ABS(HASH(T.CUSTOMERID)) % 100) < 20 THEN T.TRANSACTIONAMOUNT * 0.01
            ELSE 0
        END,
        2
    ) AS TOTAL_FINANCING_COST
    
FROM B2B_PROFITABILITY.PUBLIC.TRANSACTIONS_GENERATED T
ORDER BY T.TRANSACTIONID
