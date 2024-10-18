const { Box } = require( "amui/material");
const { styled } = require("@mui/system");

 {/*handy flex between component */}
const FlexBetween = styled(Box)({
display: "flex",
 justifyContent: "space-between",
alignItems: "center"
});

export default FlexBetween;


