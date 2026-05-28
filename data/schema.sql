DROP TABLE IF EXISTS fact_sales;
DROP TABLE IF EXISTS dim_product;
DROP TABLE IF EXISTS dim_customer;
DROP TABLE IF EXISTS dim_business_unit;
DROP TABLE IF EXISTS dim_region;

CREATE TABLE dim_region (
    region_id INTEGER PRIMARY KEY,
    region_name TEXT NOT NULL,
    parent_region TEXT NOT NULL
);

CREATE TABLE dim_business_unit (
    business_unit_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE dim_customer (
    customer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    segment TEXT NOT NULL
);

CREATE TABLE dim_product (
    product_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE fact_sales (
    sale_id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    region_id INTEGER NOT NULL,
    business_unit_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    revenue REAL NOT NULL,
    refunds REAL NOT NULL,
    expense REAL NOT NULL,
    units INTEGER NOT NULL,
    FOREIGN KEY (region_id) REFERENCES dim_region(region_id),
    FOREIGN KEY (business_unit_id) REFERENCES dim_business_unit(business_unit_id),
    FOREIGN KEY (product_id) REFERENCES dim_product(product_id),
    FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id)
);
