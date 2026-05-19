# Data Directory

This directory contains the data files for the CRM Dashboard.

## Upload Your Files

Place your Excel XLSB or XLSX files in this directory. The application will automatically detect and load them.

## Expected File Structure

### Sheet: `customers`
- `customer_id`: Unique customer identifier
- `name`: Customer name
- `email`: Email address
- `phone`: Phone number
- `country`: Country
- `city`: City
- `status`: Customer status (Active/Inactive)

### Sheet: `orders`
- `order_id`: Unique order identifier
- `customer_id`: Reference to customer
- `order_date`: Order date (YYYY-MM-DD format)
- `amount`: Order amount
- `status`: Order status (Completed/Pending/Cancelled)
- `product_id`: Reference to product (optional)

### Sheet: `products` (Optional)
- `product_id`: Unique product identifier
- `name`: Product name
- `price`: Product price
- `category`: Product category

## Example File Names

- `crm_data.xlsb`
- `sales_2024.xlsx`
- `customer_orders.xlsb`

## Notes

- Files are automatically processed and loaded into DuckDB
- The database is stored as `crm_database.duckdb` in this directory
- XLSB files require the `pyxlsb` library
- XLSX files use the standard pandas reader
