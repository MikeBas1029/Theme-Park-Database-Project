// src/utils/getRideImage.js

// utils/getRideImage.js
export const getRideImage = (rideType) => {
	return `${process.env.PUBLIC_URL}/assets/rides/${rideType}.jpeg`;
};
export default getRideImage;
