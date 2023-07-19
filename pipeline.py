def pipeline(product):
    title, price, image, link = product.values()

    title = title.strip()
    price = float(price.replace("$", "").replace(",", ""))

    new_product = {
        "title": title,
        "price": price,
        "image": image,
        "link": link
    }

    return new_product
    # This function will make sure every project has the same elements, like no whitespace, float as currency, etc
