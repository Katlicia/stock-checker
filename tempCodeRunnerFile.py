                    unavailable_stock = product.find_element(By.CLASS_NAME, "add-to-basket.productNo.ng-star-inserted")
                    if unavailable_stock.is_enabled():
                        print(f"{product_name}: Out of stock")
                        products[product_name] = 0