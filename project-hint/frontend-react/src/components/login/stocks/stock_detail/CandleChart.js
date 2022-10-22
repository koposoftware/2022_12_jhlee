import React, { useState, useEffect } from "react";
import ReactApexChart from "react-apexcharts";
import "./stockDetail.css";
import axios from "axios";

const CandleChart = (props) => {

  const [series, setSeries] = useState([]);
  useEffect(() => {
    axios
      .get(`http://127.0.0.1:5000/stocks/candle/${props.match.params.symbol}`)
      .then((response) => {
        let tmpList = [];
        response.data.map((candle, i) => {
          tmpList[i] = {
            x: candle.x,
            y: [candle.y[2], candle.y[0], candle.y[1], candle.y[3]],
          };
        });
        setSeries([{ data: tmpList }]);
      })
      .catch((error) => {
        console.log(`CandleChart useEffect catch python`);
      });
  }, []);

  const [options] = useState({
    chart: {
      type: "candlestick",
      // height: 500,
      // background: '#FFFFFF',
      // padding: 30,
      toolbar: {
        show: false
      }
    },
    xaxis: {
      type: "datetime",
    },
    yaxis: {
      tooltip: {
        enabled: true,
      },
    },
    scrollbar: {
      enabled: true
    },
    plotOptions: {
      candlestick: {
        colors: {
          upward: "#ED3838",
          downward: "#0A7DF3",
        },
      },
    },
  });

    return (
    <>
      <div id="chart">
        <ReactApexChart options={options} series={series} type="candlestick" height={580} width={1400}/>
      </div>
    </>
  );
};

export default CandleChart;
