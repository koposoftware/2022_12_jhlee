import React, {useEffect, useRef, useState} from "react";
import "./change_ratio_up.style.css";
import {Link} from "react-router-dom";
import axios from "axios";
import useInterval from "../../../useInterval";

const Change_Ratio_Down = () => {

    const [stocks, setStocks] = useState([]);

    const loop = function () {
        axios
            .get(
                `https://`
            )
            .then((res) => {
                const stock1 = {
                    종목명: res.data[0].종목명,
                    현재가: res.data[0].종가.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","),
                    전일비: res.data[0].등락률.toString().includes("-") ? (res.data[0].등락률.toString().replace("-", "")) / 100 : (res.data[0].등락률) / 100,
                    redofblue: res.data[0].등락률.toString().includes("-") ? "down" : "up",
                };
                const stock2 = {
                    종목명: res.data[1].종목명,
                    현재가: res.data[1].종가.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","),
                    전일비: res.data[1].등락률.toString().includes("-") ? (res.data[1].등락률.toString().replace("-", "")) / 100 : (res.data[1].등락률) / 100,
                    redofblue: res.data[1].등락률.toString().includes("-") ? "down" : "up",
                };
                const stock3 = {
                    종목명: res.data[2].종목명,
                    현재가: res.data[2].종가.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","),
                    전일비: res.data[2].등락률.toString().includes("-") ? (res.data[2].등락률.toString().replace("-", "")) / 100 : (res.data[2].등락률) / 100,
                    redofblue: res.data[2].등락률.toString().includes("-") ? "down" : "up",
                };
                const stock4 = {
                    종목명: res.data[3].종목명,
                    현재가: res.data[3].종가.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","),
                    전일비: res.data[3].등락률.toString().includes("-") ? (res.data[3].등락률.toString().replace("-", "")) / 100 : (res.data[3].등락률) / 100,
                    redofblue: res.data[3].등락률.toString().includes("-") ? "down" : "up",
                };
                const stock5 = {
                    종목명: res.data[4].종목명,
                    현재가: res.data[4].종가.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","),
                    전일비: res.data[4].등락률.toString().includes("-") ? (res.data[4].등락률.toString().replace("-", "")) / 100 : (res.data[4].등락률) / 100,
                    redofblue: res.data[4].등락률.toString().includes("-") ? "down" : "up",
                };
                setStocks([stock1, stock2, stock3, stock4, stock5]);
                console.log(stock1, stock2, stock3, stock4, stock5)
            })
    }

    loop();

    useInterval(() => {

        axios
            .get(
                `https:`
            )
            .then((res) => {
                const stock1 = {
                    종목명: res.data[0].종목명,
                    현재가: res.data[0].종가.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","),
                    전일비: res.data[0].등락률.toString().includes("-") ? (res.data[0].등락률.toString().replace("-", "")) / 100 : (res.data[0].등락률) / 100,
                    redofblue: res.data[0].등락률.toString().includes("-") ? "down" : "up",
                };
                const stock2 = {
                    종목명: res.data[1].종목명,
                    현재가: res.data[1].종가.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","),
                    전일비: res.data[1].등락률.toString().includes("-") ? (res.data[1].등락률.toString().replace("-", "")) / 100 : (res.data[1].등락률) / 100,
                    redofblue: res.data[1].등락률.toString().includes("-") ? "down" : "up",
                };
                const stock3 = {
                    종목명: res.data[2].종목명,
                    현재가: res.data[2].종가.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","),
                    전일비: res.data[2].등락률.toString().includes("-") ? (res.data[2].등락률.toString().replace("-", "")) / 100 : (res.data[2].등락률) / 100,
                    redofblue: res.data[2].등락률.toString().includes("-") ? "down" : "up",
                };
                const stock4 = {
                    종목명: res.data[3].종목명,
                    현재가: res.data[3].종가.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","),
                    전일비: res.data[3].등락률.toString().includes("-") ? (res.data[3].등락률.toString().replace("-", "")) / 100 : (res.data[3].등락률) / 100,
                    redofblue: res.data[3].등락률.toString().includes("-") ? "down" : "up",
                };
                const stock5 = {
                    종목명: res.data[4].종목명,
                    현재가: res.data[4].종가.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","),
                    전일비: res.data[4].등락률.toString().includes("-") ? (res.data[4].등락률.toString().replace("-", "")) / 100 : (res.data[4].등락률) / 100,
                    redofblue: res.data[4].등락률.toString().includes("-") ? "down" : "up",
                };
                setStocks([stock1, stock2, stock3, stock4, stock5]);
            })
            .catch((err) => {
                console.log(err);
            });
    }, 3000);


    return (
        <div className="recommendation_stock_container2">
            {stocks.map((stock) => (
                <div className="stock_detail_section_02" key={stock.index}>
                    <Link to={`/stock/detail/${stock.종목코드}`} className="link">
                        <div className="stock_title_section1">{stock.종목명}</div>
                    </Link>
                    <div className={stock.redofblue}>
                        {/*<div className="stock_column_section1">{stock.현재가}원</div>*/}
                        {/*<div className="stock_column_section">{stock.전일대비}</div>*/}
                        <div className="stock_column_section2">▼&nbsp;{stock.전일비}%</div>
                    </div>
                </div>
            ))}
        </div>
    );
};

export default Change_Ratio_Down;
