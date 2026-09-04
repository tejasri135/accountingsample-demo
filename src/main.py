from gst import calc_gst
from product import Product
gst_rates = {
    "essentials": 5,
    "standard": 12,
    "electronics": 18,
    "luxury": 28,
    "misc": 18
}

details = [] 
name = input("Hello pls enter the name")
try:
    total_expense_list = int(input(("enter a no of expenses/purchases that needs to be stored")))
except ValueError:
    print("That's not a valid number defaulting no of entries as 1")
    total_expense_list = 1
for i in range(total_expense_list): 
    product_no = i
    product_name = (input("enter the product name "))
    try:
        product_price = int(input("enter the base price "))
    except ValueError:
        print("That's not a valid number. setting default baseprice as 100")
        product_price = 100
    purchase_type = (input("enter the  purchase type (electronics ,standard,essentials,misc,luxury)"))    
    is_intrastate = input("is the purchase in the same state ?? Enter True/yes or False/no: ").capitalize()
    if is_intrastate in("Yes","Y","True"):
         is_intrastate = True
    else:
        is_intrastate = False

    rate = gst_rates.get(purchase_type, 18)
    p = Product(product_name, product_price, rate, not is_intrastate) 
    ##total_price = calc_gst(product_price, rate, not is_intrastate)
    total_price = p.calculate_gst()
    details.append({"product_no":product_no,"product_name":product_name,"purchase_type":purchase_type,
                    "base_price":product_price,"is_intrastate":is_intrastate,"tax_rate":rate,"total_price":total_price, })
#print(f"{product_name:<12}{purchase_type:<10}{product_price:<10}{is_intrastate:<10}{rate:<10}{total_price:<10}")

#adding proper display format
print('-'*160)
print(f'------------------------------------------------------------------WELCOME  {name.capitalize()}--------------------------------------------------------------------')
print('-'*160)
print(f"{'Product':<20}{'Category':<20}{'Base':<20}{'CGST':<20}{'SGST':<20}{'IGST':<20}{'Rate':<20}{'Total':<20}")
print('-'*160)
grand_total,cgst_total,igst_total,sgst_total,total_tax,taxable_value = 0, 0, 0, 0, 0,0

for item in details:
    name = item['product_name']
    cat = item['purchase_type']
    base = item['base_price']
    cgst = item['total_price']['cgst']
    sgst = item['total_price']['sgst']
    igst = item['total_price']['igst']
    rate = item['tax_rate']
    total = item['total_price']['total_product_price']
    taxable_value += base
    grand_total +=total
    cgst_total +=cgst
    sgst_total +=sgst
    igst_total +=igst
    print(f"{name:<20}{cat:<20}{base:<20}{cgst:<20}{sgst:<20}{igst:<20}{rate:<20}{total:<20}")
    print('-'*160)
total_tax = sum([cgst_total,sgst_total,igst_total])    
print('-'*160)
print(f"{'Total Taxable Value':<25}{taxable_value:>15}")
print(f"{'Total CGST':<25}{cgst_total:>15}")
print(f"{'Total SGST':<25}{sgst_total:>15}")
print(f"{'Total IGST':<25}{igst_total:>15}")
print(f"{'Total Tax':<25}{total_tax:>15}")
print(f"{'Grand Total':<25}{grand_total:>15}")