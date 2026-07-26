import database
from typing import Dict, Any

def get_inventory_metrics() -> Dict[str, Any]:
    """Calculates general inventory metrics."""
    products = database.get_all_products()
    total_items = len(products)
    total_quantity = sum(p['quantity'] for p in products)
    total_value = sum(p['price'] * p['quantity'] for p in products)
    
    return {
        "total_items": total_items,
        "total_quantity": total_quantity,
        "total_value": round(total_value, 2)
    }

def get_low_stock_products(threshold: int = 5):
    """Retrieves products with quantities at or below a specified threshold."""
    products = database.get_all_products()
    return [p for p in products if p['quantity'] <= threshold]

def generate_full_report_text(threshold: int = 5) -> str:
    """Generates a structured plain-text report of the entire inventory system."""
    metrics = get_inventory_metrics()
    products = database.get_all_products()
    low_stock = get_low_stock_products(threshold)
    sales = database.get_all_sales()

    lines = []
    lines.append("=" * 60)
    lines.append("          INVENTORY MANAGEMENT SYSTEM REPORT          ")
    lines.append("=" * 60)
    lines.append("")
    
    lines.append("--- INVENTORY SUMMARY ---")
    lines.append(f" Total Unique Products : {metrics['total_items']}")
    lines.append(f" Total Units in Stock  : {metrics['total_quantity']}")
    lines.append(f" Total Inventory Value : ${metrics['total_value']:.2f}")
    lines.append("")

    lines.append("--- CURRENT INVENTORY DETAILS ---")
    lines.append(f"{'ID':<5} | {'Name':<20} | {'Category':<12} | {'Price':<8} | {'Qty':<5} | {'Supplier':<12}")
    lines.append("-" * 75)
    for p in products:
        lines.append(f"{p['id']:<5} | {p['name']:<20} | {p['category']:<12} | ${p['price']:<7.2f} | {p['quantity']:<5} | {p['supplier']:<12}")
    lines.append("")

    lines.append(f"--- LOW STOCK ALERTS (Quantity <= {threshold}) ---")
    if low_stock:
        lines.append(f"{'ID':<5} | {'Name':<20} | {'Current Stock':<15}")
        lines.append("-" * 45)
        for p in low_stock:
            lines.append(f"{p['id']:<5} | {p['name']:<20} | {p['quantity']:<15}")
    else:
        lines.append(" No low stock alerts.")
    lines.append("")

    lines.append("--- SALES SUMMARY LOG ---")
    if sales:
        total_revenue = sum(s['total_price'] for s in sales)
        lines.append(f" Total Sales Completed : {len(sales)}")
        lines.append(f" Total Revenue Earned  : ${total_revenue:.2f}")
        lines.append("")
        lines.append(f"{'ID':<5} | {'Timestamp':<20} | {'Product':<18} | {'Qty':<5} | {'Total':<8}")
        lines.append("-" * 65)
        for s in sales:
            lines.append(f"{s['id']:<5} | {s['timestamp']:<20} | {s['product_name']:<18} | {s['quantity_sold']:<5} | ${s['total_price']:<7.2f}")
    else:
        lines.append(" No sales transactions recorded.")

    lines.append("")
    lines.append("=" * 60)
    lines.append("                    END OF REPORT                    ")
    lines.append("=" * 60)

    return "\n".join(lines)

def export_report_file(filename: str = "inventory_report.txt", threshold: int = 5) -> bool:
    """Exports the inventory report text to a disk file."""
    report_content = generate_full_report_text(threshold)
    try:
        with open(filename, "w") as file:
            file.write(report_content)
        print(f"\nSuccess: Report saved to file '{filename}'.")
        return True
    except IOError as e:
        print(f"\nError writing report file: {e}")
        return False