from src.gst import  calc_gst
##print(calc_gst(250, 12, False))


def test_intrastate():
    result = calc_gst(250, 12, False)
    ##calculated value 12% of 250 is 30 and for cgst = tax/2 which is 15 for intrastate
    assert result["cgst"] == 15
    ##total product price here is cgst+sgst+base+price
    assert result["total_product_price"] == 280

def test_interstate():
    result2  = calc_gst(250, 12, True)
    assert result2["cgst"] == 0  
    assert result2["igst"] == 30


