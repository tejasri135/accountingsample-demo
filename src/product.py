class Product:
    def __init__(self, name, base_price, rate,is_interstate):
        self.name = name
        self.base_price = base_price
        self.rate = rate
        self.is_interstate = is_interstate
        
    def calculate_gst(self):
        tax = self.base_price * (self.rate / 100)
        if self.is_interstate == True: 
                return {
                        "transaction_type": "Interstate",
                        "base_price": round(self.base_price,2),
                        "cgst" : 0.0,
                        "sgst" : 0.0,
                        "igst": round(tax,2),
                        "total_product_price": round(( self.base_price+tax),2)

                    }
        else:
                  return {
                                "transaction_type": "Intrastate",
                                "base_price": round(self.base_price,2),
                                "cgst" :round((tax / 2),2),
                                "sgst" :round((tax / 2),2),
                                "igst": 0.0,
                                "total_product_price": round(( self.base_price+tax),2)
                
                                }

