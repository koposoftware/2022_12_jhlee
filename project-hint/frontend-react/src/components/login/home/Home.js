import React from "react";
import "./home.style.scss";
import {Link} from "react-router-dom";
import WordCanvas from "./wordcanvas/WordCanvas";
import Recent_News from "./recent_news/Recent_News";
import Asset from "./asset/Asset";
// import Recent_Opinion from "./recent_opinion/Recent_Opinion";
import RecommendationStock from "./recommendation_stock/RecommendationStock";
import {Navbar} from "../logined_navbar";
import Menu from "../menu/Menu";
// import Lottie from "lottie-web";
import LottieButton from "./LottieButton";
import Swal from "sweetalert2";
import MainIcon from "../../../assets/home/home_main_logo.png";
import Change_Ratio_Up from "./change_ratio/Change_Ratio_Up";
import Change_Ratio_Down from "./change_ratio/Change_Ratio_Down";
import { faArrowTrendUp,
    faArrowTrendDown,
    faMagnifyingGlassChart,
    faWandMagicSparkles,
    faNewspaper } from "@fortawesome/free-solid-svg-icons";
import { faSquare } from "@fortawesome/free-regular-svg-icons";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";

const Home = () => {

    return (
        <>
            <Navbar/>
            <div className="main_container">
                <div className="wrapper">

                    {/*<Menu />*/}

                    <div className="home_container">

                        <div className="recent_news_container">
                            <div className="recent_news_section">
                                <div className="title_section">
                                    <div className="documentroom_text">
                                        <FontAwesomeIcon icon={faNewspaper} color="black" />
                                        &nbsp;&nbsp;최신 뉴스
                                    </div>
                                    <Link to="/news" className="more">
                                        <span>더보기 ▶</span>
                                    </Link>
                                </div>
                                <div className="newsList">
                                    <Recent_News/>
                                </div>
                            </div>

                            <div className="keyword_wordcloud">
                                <div className="title_section">
                                    <div className="documentroom_text">
                                        <FontAwesomeIcon icon={faMagnifyingGlassChart} color="green" />
                                        &nbsp;&nbsp;급상승 키워드
                                    </div>
                                </div>
                                <div className="wordcloud">
                                    <WordCanvas/>
                                </div>
                            </div>
                        </div>

                        <div className="other_container">
                            {/*<div className="asset_section">*/}
                            {/*  <div className="title_section">*/}
                            {/*    <div className="documentroom_text">투자 현황</div>*/}
                            {/*    <Link to="/portfolio" className="more_2">*/}
                            {/*      <span>더보기 ▶</span>*/}
                            {/*    </Link>*/}
                            {/*  </div>*/}

                            {/*  <div>*/}
                            {/*    <Asset />*/}
                            {/*  </div>*/}
                            {/*</div>*/}
                            <div className="stock_section_up">
                                <div className="title_section">
                                    <div className="documentroom_text">
                                        {/*<FontAwesomeIcon icon={faArrowTrendUp} color="red" beatFade/>*/}
                                        <FontAwesomeIcon icon={faArrowTrendUp} color="red"/>
                                        &nbsp;&nbsp;상승률 TOP5
                                    </div>
                                </div>
                                <div>
                                    <Change_Ratio_Up/>
                                </div>
                            </div>
                            <div className="stock_section_down">
                                <div className="title_section">
                                    <div className="documentroom_text">
                                        <FontAwesomeIcon icon={faArrowTrendDown} color="blue"/>
                                        &nbsp;&nbsp;하락률 TOP5
                                    </div>
                                </div>
                                <div>
                                    <Change_Ratio_Down/>
                                </div>
                            </div>

                            <div className="stock_section">
                                <div className="title_section">
                                    <div className="documentroom_text">
                                        <FontAwesomeIcon icon={faWandMagicSparkles} color="orange" />
                                        &nbsp;&nbsp;추천 종목
                                    </div>
                                </div>
                                <div>
                                    <RecommendationStock/>
                                </div>
                            </div>
                            <div className="a_section">
                                <LottieButton/>
                                <div className="a_section_button">
                                    <div className="button_container">
                                        <button className="btn_home" onClick={(e) => {
                                            e.preventDefault();
                                            let timerInterval
                                            Swal.fire({
                                                width: 600,
                                                imageUrl: MainIcon,
                                                imageWidth: 500,
                                                imageHeight: 500,
                                                // imageAlt: 'Custom image',
                                                title: '잠시후 종목 분석실로 이동합니다.',
                                                text: 'dsdsaf',
                                                html: '취소하시려면 오른쪽 상단의 버튼을 클릭하세요.',
                                                // html: '잠시후 종목 분석실로 이동합니다.',
                                                timer: 3000,
                                                timerProgressBar: true,
                                                // showCancelButton: true,
                                                // cancelButtonText:'취소',
                                                showCloseButton: true,
                                                // color: 'green',
                                                // background: 'grey',
                                                backdrop: `rgba(0,0,0,0.8)no-repeat`,
                                                didOpen: () => {
                                                    Swal.showLoading()
                                                },
                                                willClose: () => {
                                                    clearInterval(timerInterval)
                                                },
                                                showClass: {
                                                    popup: 'animate__animated animate__fadeInRightBig'
                                                    // popup: 'animate__animated animate__fadeInBottomRight'
                                                },
                                                hideClass: {
                                                    popup: 'animate__animated animate__fadeOutLeftBig'
                                                }
                                            }).then((result) => {
                                                if (!(result.dismiss === Swal.DismissReason.close)) {
                                                    setTimeout(function () {
                                                        window.open(
                                                            'http://127.0.0.1:5050',
                                                            '_self',//_parent : 부모 프레임, _self : 현재 페이지, _top : 로드된 프레임셋 대체
                                                            'width=1500, height=1000, location=no, status=no, scrollbars=yes'
                                                        )
                                                    }, 200)
                                                }
                                            }).catch((error) => {
                                                throw error;
                                            })
                                        }}>
                        <span>
                          종목 분석실
                        </span>
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </>
    );
};

export default Home;
