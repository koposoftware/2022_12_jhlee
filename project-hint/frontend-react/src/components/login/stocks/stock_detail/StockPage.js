import React, { useEffect, useState, useContext } from "react";
import {RealtimeChart, CandleChart, StockDetail} from "../index";
import Navbar from "../../logined_navbar/Navbar";
import Menu from "../../menu/Menu";
import axios from "axios";
import { AssetContext } from "../../../../context";
import "./stockPage.css";

const startInterval = (seconds, callback) => {
    callback();
    return setInterval(callback, seconds * 1000);
}

export const stopInterval = () => {
    clearInterval(startInterval);
}

const StockPage = ({ props, match }) => {

  const { asset, setAsset } = useContext(AssetContext);
  const [stockDetail, setStockDetail] = useState({});

  useEffect(() => {

      // startInterval(3, () => {
          axios.get(`http://localhost:8080/stocks/${match.params.symbol}`)
              .then((response) => {
                  setStockDetail(response.data);
              })
              .catch((error) => {
                  throw error;
              });
      // })
    // setInterval(() => {
    //   axios.get(`http://localhost:8080/stocks/${match.params.symbol}`)
    //       .then((response) => {
    //         setStockDetail(response.data);
    //       })
    //       .catch((error) => {
    //         throw error;
    //       });
      // }, 5000)
  }, []);

  useEffect(() => {
    axios
      .get(
        `http://localhost:8080/assets/holdingCount/${
          JSON.parse(sessionStorage.getItem("logined_user")).userId
        }`
      )
      .then((response) => {
        setAsset(response.data.holdingCount);
      })
      .catch((error) => {
        throw error;
      });
  }, []);

  return (
    <>
      <Navbar />
      <div className="content-container">
        <div className="wrapper">
          {/*<Menu />*/}
          <div className="stock-detali-content-1">
            <StockDetail stockDetail={stockDetail} asset={asset} setAsset={setAsset}/>
            {/*<div className="candle">*/}
              <CandleChart match={match} />
            {/*</div>*/}
          </div>
        </div>
      </div>
    </>
  );
};

export default StockPage;
