import { useEffect, useState } from "react";
import { ResponsiveLine } from "@nivo/line";
import { useTheme } from "@mui/material";
import { tokens } from "../theme";



const LineChart = ({ isDashboard = false }) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);





  // Function to aggregate customer data by month
  const transformData = (apiData) => {
    const monthlyData = new Array(12).fill(0); // Initialize an array for 12 months with 0 counts

    // Sum up the number of customers for each month
    apiData.forEach((entry) => {
      monthlyData[entry.month - 1] += entry.num_customers; // -1 to adjust for 0-based index
    });

    // Format data for Nivo Line Chart
    const transformed = [
      {
        id: "Customers",
        color: "hsl(205, 70%, 50%)",
        data: monthlyData.map((count, index) => ({
          x: `Month ${index + 1}`, // Label for x-axis
          y: count, // Total customers for the month
        })),
      },
    ];

    return transformed;
  };



  
  // Fetch data from the API using fetch
  useEffect(() => {
    const fetchCustomerData = async () => {
      try {
        const response = await fetch( "https://theme-park-backend.ambitioussea-02dd25ab.eastus.azurecontainerapps.io/api/v1/reports/customer-count");
        if (!response.ok) throw new Error("Network response was not ok");
        const apiData = await response.json();
        const transformedData = transformData(apiData);
        setData(transformedData);
        console.log("Line chart data",data)
      } catch (error) {
        console.error("Error fetching customer data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchCustomerData();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }




  return (
    <ResponsiveLine
      data={data}
      theme={{
        axis: {
          domain: {
            line: {
              stroke: colors.grey[100],
            },
          },
          legend: {
            text: {
              fill: colors.grey[100],
            },
          },
          ticks: {
            line: {
              stroke: colors.grey[100],
              strokeWidth: 1,
            },
            text: {
              fill: colors.grey[100],
            },
          },
        },
        legends: {
          text: {
            fill: colors.grey[100],
          },
        },
        tooltip: {
          container: {
            color: colors.primary[500],
          },
        },
      }}
      colors={isDashboard ? { datum: "color" } : { scheme: "nivo" }} 
      margin={{ top: 50, right: 110, bottom: 50, left: 60 }}
      xScale={{ type: "point" }}
      yScale={{
        type: "linear",
        min: "auto",
        max: "auto",
        stacked: false,
        reverse: false,
      }}
      yFormat=" >-.2f"
      curve="catmullRom"
      axisTop={null}
      axisRight={null}
      axisBottom={{
        orient: "bottom",
        tickSize: 5,
        tickPadding: 5,
        tickRotation: 0,
        legend: "Months",
        legendOffset: 36,
        legendPosition: "middle",
      }}
      axisLeft={{
        orient: "left",
        tickValues: 5, 
        tickSize: 3,
        tickPadding: 5,
        tickRotation: 0,
        legend: "Number of Customers",
        legendOffset: -40,
        legendPosition: "middle",
      }}
      enableGridX={true}
      enableGridY={true}
      pointSize={8}
      pointColor={{ theme: "background" }}
      pointBorderWidth={2}
      pointBorderColor={{ from: "serieColor" }}
      pointLabelYOffset={-12}
      useMesh={true}
      legends={[
        {
          anchor: "bottom-right",
          direction: "column",
          justify: false,
          translateX: 100,
          translateY: 0,
          itemsSpacing: 0,
          itemDirection: "left-to-right",
          itemWidth: 80,
          itemHeight: 20,
          itemOpacity: 0.75,
          symbolSize: 12,
          symbolShape: "circle",
          symbolBorderColor: "rgba(0, 0, 0, .5)",
          effects: [
            {
              on: "hover",
              style: {
                itemBackground: "rgba(0, 0, 0, .03)",
                itemOpacity: 1,
              },
            },
          ],
        },
      ]}
    />
  );
};

export default LineChart;