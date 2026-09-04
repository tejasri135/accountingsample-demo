

def calc_gst(base_price, rate, is_interstate):
        tax = base_price*(rate/100)
        total_product_price = base_price+tax
        if is_interstate == True:
                return {
                        "transaction_type": "Interstate",
                        "base_price": round(base_price,2),
                        "cgst" : 0.0,
                        "sgst" : 0.0,
                        "igst": round(tax,2),
                        "total_product_price": round(total_product_price,2)

                    }
        else:
                  return {
                                "transaction_type": "Intrastate",
                                "base_price": round(base_price,2),
                                "cgst" :round((tax / 2),2),
                                "sgst" :round((tax / 2),2),
                                "igst": 0.0,
                                "total_product_price": round(total_product_price,2)
                
                                }


    
