import graphlab

business = graphlab.SFrame.read_csv('yelp_academic_dataset_business.json', header=False, delimiter='\n', column_type_hints=dict)
checkin = graphlab.SFrame.read_csv('yelp_academic_dataset_checkin.json', header=False, delimiter='\n', column_type_hints=dict)
review = graphlab.SFrame.read_csv('yelp_academic_dataset_review.json', header=False, delimiter='\n', column_type_hints=dict)
user = graphlab.SFrame.read_csv('yelp_academic_dataset_user.json', header=False, delimiter='\n', column_type_hints=dict)
tip = graphlab.SFrame.read_csv('yelp_academic_dataset_tip.json', header=False, delimiter='\n', column_type_hints=dict)

# Changing JSON into tables, i.e. SFrames
reviews = review.unpack('X1', column_name_prefix='')
businesses = business.unpack('X1', column_name_prefix='', limit=['business_id', 'name', 'latitude', 'longitude', 'stars'])

# Build a recommender system
m = graphlab.recommender.create(reviews, 'user_id', 'business_id')

# Find businesses that are similar based on users in common
m.get_similar_items(['BVxlrYWgmi-8TPGMe6CTpg']).join(businesses, on={'similar_item':'business_id'})
