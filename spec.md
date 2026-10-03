# E-Commerce / Inventory / Marketplace 

### Entities (tables)

```sql
users
------
id
role: customer | store
name
contact
email
address
```

```sql
products
--------
id
store_id
name
description
price
image_url
quantity_available
quantity_reserved
```

```sql
orders
------
id
customer_id
store_id
order_status
order_value  -- from order_products
order_date
```

Junction Tables

```sql
order_products
-------------
id
order_id
product_id
product_quantity
unit_value -- stored while ordering, unaffected from future prince change
```

### Actions 

```
By Customer
- Register
- Browse products
- Place Order
- Cancel Order (before delivery - 1 day)
- View Order History
- Return order (within 2w)
```

```
By Store
- Register
- Add Inventory
- Remove Inventory
- View Inventory
- Fulfill Order (1 day cron job or immediate via API)
- View Sales History and Earnings
```

### ORDER STATUS TRANSITIONS

```
PLACED -> DELIVERED -> RETURNED
  |
  -> CANCELED
```