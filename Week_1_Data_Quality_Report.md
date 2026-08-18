# Project FORESIGHT --- Week 1 Data Quality Report

## 1. Overview

**Project:** FORESIGHT --- AI-Powered Demand & Inventory Intelligence
Platform\
**Phase:** Week 1 --- Data Profiling, Cleaning & Quality Validation\
**Role:** Data Engineering

### Objective

The Week 1 objective was to profile the supplied datasets, identify
data-quality issues, apply justified cleaning transformations, create
quality flags for unresolved exceptions, and validate relationships
across the datasets.

## 2. Datasets

  Dataset         Final Rows Purpose
  ------------- ------------ -----------------------------------------------
  Sales Daily         20,906 Daily SKU-level sales, pricing and revenue
  SKU Master              40 SKU reference/master data
  Calendar               546 Date and promotion information
  Inventory           21,840 Daily inventory and replenishment information

The initial Sales dataset contained 20,931 rows; the cleaned Sales
dataset contains 20,906 rows.

## 3. Profiling and Date Validation

All four datasets were profiled for structure, missing values,
duplicates, data types, outliers, and consistency.

Initial date columns were stored as `object` dtype. After cleaning,
Sales `date`, SKU Master `launch_date`, Calendar `date`, and Inventory
`date` were converted to `datetime64[ns]`.

Invalid date checks returned **0 invalid date values** for all datasets.

## 4. Sales Data Quality

### SKU and duplicate checks

-   Unique SKUs in Sales: **40**
-   SKUs in Master: **40**
-   Sales SKUs missing from Master: **0**
-   Duplicates before cleaning: **0**
-   Duplicates removed: **0**
-   Duplicates after cleaning: **0**

### Missing `units_sold`

There were **70 missing `units_sold` records**.

`calculated_units = revenue / price` was used to identify supported
candidates.

-   Calculated units: **70**
-   Non-integer calculated units: **15**
-   Whole-unit candidates: **55**
-   Units successfully filled: **55**
-   Remaining missing `units_sold`: **15**

The 15 unresolved records were retained as missing rather than forcing
unsupported values.

### Missing `price`

There were **50 missing price records**.

-   Non-promotion exact-price candidates: **40**
-   Promotional missing prices: **10**
-   Prices successfully filled: **40**
-   Remaining missing prices: **10**

The remaining 10 missing prices are associated with promotional records.

### SKU001 price correction

A validation identified **34 non-promotion price mismatches**, all
belonging to SKU001.

-   Records matching the SKU Master price: **34**
-   SKU001 prices corrected: **34**
-   Remaining non-promotion price mismatches: **0**

### Revenue validation

Final revenue quality flags:

  Flag                      Records
  -------------------- ------------
  `OK`                       17,627
  `REVENUE_MISMATCH`          3,254
  `MISSING_INPUT`                25
  **Total**              **20,906**

The 3,254 revenue mismatches consisted of:

  Promotion status                 Records
  ------------------------------ ---------
  Promo (`promo_flag = 1`)           3,247
  Non-promo (`promo_flag = 0`)           7

### Outlier analysis

**Units sold**

-   Q1: 34
-   Q3: 83
-   IQR: 49
-   Lower bound: -39.5
-   Upper bound: 156.5
-   Outliers: **124**

**Price**

-   Q1: 1,844.52
-   Q3: 5,788.57
-   IQR: 3,944.05
-   Lower bound: -4,071.555
-   Upper bound: 11,704.645
-   Outliers: **0**

**Revenue**

-   Q1: 89,121.90
-   Q3: 327,322.67
-   IQR: 238,200.77
-   Lower bound: -268,179.255
-   Upper bound: 684,623.825
-   Outliers: **966**

Outliers were treated as quality observations rather than automatically
deleting records.

### Sales promotion distribution

  `promo_flag`     Records
  -------------- ---------
  0                 17,657
  1                  3,274

## 5. SKU Master Data Quality

### Integrity

-   Rows: **40**
-   Duplicate SKU IDs: **0**
-   Unique Master SKUs: **40**

### Categories

  Category             SKUs
  ------------------ ------
  Furniture              10
  Home Decor             10
  Small Appliances       10
  Office                 10

### Subcategories

  Subcategory      Count
  -------------- -------
  Chair               10
  Toaster             10
  Organizer           10
  Clock                9
  `home decor`         1

No leading/trailing whitespace was detected.

### Missing unit cost

One record has a missing `unit_cost`:

-   SKU: **SKU018**
-   Category: **Home Decor**
-   Subcategory: **Clock**
-   List price: **3,475.70**

Comparable records were reviewed, but a unit cost was not invented.

Final SKU quality flags:

  Flag                      Records
  ----------------------- ---------
  `OK`                           38
  `UNUSUAL_SUBCATEGORY`           1
  `MISSING_UNIT_COST`             1
  **Total**                  **40**

## 6. Inventory Data Quality

### Lead time

All 40 SKUs with observed lead-time data had consistent SKU-level
values.

-   SKUs with more than one lead-time value: **0**
-   SKUs with consistent lead time: **40**
-   Remaining missing `lead_time_days`: **0**
-   Lead-time values filled: **40**

Lead-time statistics:

  Metric            Value
  ----------- -----------
  Count            21,800
  Mean          7.80 days
  Std. Dev.     3.74 days
  Minimum          2 days
  Q1               6 days
  Median           7 days
  Q3              10 days
  Maximum         14 days

### Inventory exceptions

-   Missing `on_hand_units`: **40**
-   Negative `on_hand_units`: **1**
-   Missing `lead_time_days` after cleaning: **0**

The negative inventory record was:

-   SKU: **SKU003**
-   Date: **2025-05-23**
-   `on_hand_units`: **-25**
-   `on_order_units`: **18**
-   `lead_time_days`: **7**
-   `reorder_point`: **48**

Final inventory quality flags:

  Flag                      Records
  -------------------- ------------
  `OK`                       21,799
  `MISSING_ON_HAND`              40
  `NEGATIVE_ON_HAND`              1
  **Total**              **21,840**

## 7. Calendar Data Quality

-   Rows: **546**
-   Missing dates: **0**
-   Duplicate dates: **0**
-   Invalid dates: **0**
-   Promotion-event records: **85**

Promotion events:

  Event             Records
  --------------- ---------
  Summer Sale            22
  Spring Sale            19
  Year End Sale          17
  Black Friday           11
  Festive Sale           10
  New Year Sale           6

Promotion flag distribution:

  `promo_flag`     Records
  -------------- ---------
  0                    461
  1                     85

## 8. Cross-Dataset Referential Integrity

  Validation                                 Result
  ---------------------------------------- --------
  Sales SKUs missing from SKU Master          **0**
  Inventory SKUs missing from SKU Master      **0**
  Sales dates missing from Calendar           **0**
  Inventory dates missing from Calendar       **0**

No orphan SKUs or orphan dates were identified.

## 9. Final Week 1 Quality Summary

  ------------------------------------------------------------------------
  Dataset                                       Rows Key Remaining Issues
  --------------------- ---------------------------- ---------------------
  Sales Daily                                 20,906 15 missing units, 10
                                                     missing prices, 3,254
                                                     revenue mismatches

  SKU Master                                      40 1 missing unit cost,
                                                     1 unusual subcategory

  Calendar                                       546 No missing/duplicate
                                                     dates; 85 promotion
                                                     events

  Inventory                                   21,840 40 missing on-hand
                                                     values, 1 negative
                                                     on-hand value
  ------------------------------------------------------------------------

## 10. Data Engineering Approach

The cleaning approach followed these principles:

1.  Profile before modifying data.
2.  Use deterministic calculations where source data supports them.
3.  Use master/reference data to resolve known inconsistencies.
4.  Do not fabricate unresolved business values.
5.  Create quality flags for remaining exceptions.
6.  Validate referential integrity after cleaning.
7.  Preserve traceability of data-quality decisions.

## 11. Week 1 Conclusion

Week 1 profiling, cleaning, quality assessment, and cross-dataset
validation have been completed.

The cleaned datasets are structurally consistent and maintain
referential integrity across Sales, Inventory, SKU Master, and Calendar.

Remaining exceptions have been explicitly identified and flagged for
downstream handling. Revenue mismatches, unresolved promotional prices,
missing inventory quantities, the negative inventory value, and the
missing SKU018 unit cost remain visible rather than being silently
overwritten.

**Week 1 status: COMPLETED**
