INSERT INTO dim_region (region_id, region_name, parent_region) VALUES
    (1, 'Japan', 'APAC'),
    (2, 'India', 'APAC'),
    (3, 'Singapore', 'APAC'),
    (4, 'Germany', 'EMEA'),
    (5, 'United States', 'North America');

INSERT INTO dim_business_unit (business_unit_id, name) VALUES
    (1, 'Retail'),
    (2, 'Wholesale');

INSERT INTO dim_customer (customer_id, name, segment) VALUES
    (1, 'Acme Stores', 'Premium'),
    (2, 'Blue Market', 'Standard'),
    (3, 'City Retail', 'Standard'),
    (4, 'Northstar', 'Premium');

INSERT INTO dim_product (product_id, name) VALUES
    (1, 'Core Banking Bundle'),
    (2, 'Analytics Add-on'),
    (3, 'Payment Gateway');

-- APAC Retail: Q2 decline is driven by lower units in Japan/India and higher refunds in Singapore.
INSERT INTO fact_sales
    (sale_id, date, region_id, business_unit_id, product_id, customer_id, revenue, refunds, expense, units)
VALUES
    (1, '2026-01-15', 1, 1, 1, 1, 120000, 5000, 42000, 120),
    (2, '2026-02-15', 2, 1, 1, 2, 140000, 7000, 50000, 140),
    (3, '2026-03-15', 3, 1, 2, 3, 90000, 4000, 30000, 90),
    (4, '2026-04-15', 1, 1, 1, 1, 95000, 8000, 41000, 95),
    (5, '2026-05-15', 2, 1, 1, 2, 105000, 9000, 48000, 104),
    (6, '2026-06-15', 3, 1, 2, 3, 83000, 16000, 31000, 86),

    -- Controls: other geographies and business units are stable or growing.
    (7, '2026-01-15', 4, 1, 1, 4, 110000, 4000, 39000, 112),
    (8, '2026-04-15', 4, 1, 1, 4, 118000, 4500, 40000, 119),
    (9, '2026-01-15', 5, 2, 3, 1, 160000, 6000, 62000, 150),
    (10, '2026-04-15', 5, 2, 3, 1, 168000, 6500, 64000, 157);
