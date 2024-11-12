// utils/getRestaurantImage.js
const getRestaurantImage = (restaurantId) => {
	console.log(restaurantId);
	return `/assets/restaurants/${restaurantId}.jpeg`;
};

export default getRestaurantImage;
