from gst import calc_gst

gst_rates = {
    "essentials": 5,
    "standard": 12,
    "electronics": 18,
    "luxury": 28,
    "misc": 18
}

details = [] 
pn= 1
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
    purchase_type = (input("enter the  purchase type (electroncis ,standard,essentials,misc,luxury)"))    
    is_intrastate = input("is the purchase in the same state ?? Enter True or False: ") == "True"
    rate = gst_rates.get(purchase_type, 18)
    total_price = calc_gst(product_price, rate, not is_intrastate)
    details.append({"product_no":product_no,"product_name":product_name,"purchase_type":purchase_type,"base_price":product_price,"is_intrastate":is_intrastate,"tax_rate":rate,"total_price":total_price })
#print(f"{product_name:<12}{purchase_type:<10}{product_price:<10}{is_intrastate:<10}{rate:<10}{total_price:<10}")

#adding proper display format
print('-'*100)
print(f'--------------------------------------------WELCOME  {name.capitalize()}--------------------------------------')
print('-'*100)
print(f"{'Product':<20}{'Category':<20}{'Base':<20}{'Rate':<20}{'Total':<20}")
print('-'*100)

for item in details:
    name = item['product_name']
    cat = item['purchase_type']
    base = item['base_price']
    rate = item['tax_rate']
    total = item['total_price']['total_product_price']
    print(f"{name:<20}{cat:<20}{base:<20}{rate:<20}{total:<20}")