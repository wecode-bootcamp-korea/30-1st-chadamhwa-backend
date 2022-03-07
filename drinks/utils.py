def compute_reviews(drink):
    drink_reviews = drink.review_set.all() 
    review_count  = drink_reviews.count() 
    sum_rating    = 0
    for review in drink_reviews:       
        sum_rating += review.rating
    if review_count == 0:              
        drink_average_review = 0
    elif review_count != 0:                 
        drink_average_review = sum_rating / review_count    
    return drink_average_review
        

def whole_data_list_with_review(filtered_drinks):
    drink_and_average_rating = {}
    for drink in filtered_drinks:      
        drink_reviews = drink.review_set.all() 
        review_count  = drink_reviews.count() 
        sum_rating    = 0
        for review in drink_reviews:       
            sum_rating += review.rating
        if review_count == 0:              
            drink_average_review = 0
        elif review_count != 0:                 
            drink_average_review = sum_rating / review_count 
        drink_and_average_rating[drink.name] = [drink_average_review,review_count]
    whole_data_list = [{
        "name"           : drink.name,
        "price"          : drink.price,
        "average_rating" : drink_and_average_rating[drink.name][0],
        "review_count"   : drink_and_average_rating[drink.name][1],
        "image" : drink.image.image_url
    } for drink in filtered_drinks]
    return whole_data_list

