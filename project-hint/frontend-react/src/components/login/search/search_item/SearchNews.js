import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "../search_item/searchNews.style.css";
import axios from "axios";

const SearchNews = ({ keyword }) => {
  console.log(keyword);

  const showDetail = () => {};
  const [newsList, setNewsList] = useState([]);
  const [pageArr, setPageArr] = useState([]);
  const [prev, setPrev] = useState(false);
  const [next, setNext] = useState(false);
  const [page, setPage] = useState(1);
  const [range, setRange] = useState(1);

  const clickNext = () => {
    getAll(pageArr[0] + 5, range + 1);
  };

  const clickPrev = () => {
    getAll(pageArr[0] - 1, range - 1);
  };

  const getAll = (page, range) => {
    setPage(page);
    setRange(range);
    setPageArr([]);
    setNewsList([]);
    axios
      .get(`http://localhost:8080/news/search/${keyword}/${page}/${range}`)
      .then((response) => {
        console.log(`검색 결과: ${response.data.list}`);
        if (response.data.list != 0) {
          response.data.list.map((item) => {
            setNewsList((newsList) => [...newsList, item]);
          });
        } else {
          alert(`검색결과가 없습니다.`);
          window.location.assign("/news");
        }
        let i = 0;
        const startPage = response.data.pagination.startPage;
        if (
          response.data.pagination.pageCnt <
          startPage + response.data.pagination.rangeSize
        ) {
          for (i; i < response.data.pagination.pageCnt - startPage + 1; i++)
            setPageArr((pageArr) => [...pageArr, startPage + i]);
        } else {
          for (i; i < response.data.pagination.rangeSize; i++)
            setPageArr((pageArr) => [...pageArr, startPage + i]);
        }
        setPrev(response.data.pagination.prev);
        setNext(response.data.pagination.next);
      })
      .catch((error) => console.log(error));
  };
  useEffect(() => {
    getAll(1, 1);
  }, []);

  return (
    <>
        <div className="snews_container">
            <div className="sdocumentroom_container">
                {/*<div className="documentroom_text_newslist">뉴스</div>*/}
                <div className="news_table">
                    {newsList.map((item) => (
                        <ul className="news-ul-news">
                            <li className="news-li">
                                <ul className="news-row-list">
                                    <li className="post-row-list-item-news">
                                        <img className="thumbnail-style" src={item.newsThumbnail} alt="media" key={item.newsTitle}/>
                                    </li>
                                    <Link to={`/news/detail/${item.newsId}`}>
                                        <div className="news_title_div_se" onClick={() => {showDetail(item.newsTitle);}}>
                                            {item.newsTitle}
                                        </div>
                                    </Link>
                                    <li className="pnews_summary_div">
                                        <div className="news_summary_div">
                                            {item.newsRegDate}
                                            {item.newsContent}
                                        </div>
                                    </li>
                                    {/*<li>*/}
                                    {/*  <div className="news_regdate_div">*/}
                                    {/*    {item.newsRegDate}*/}
                                    {/*  </div>*/}
                                    {/*</li>*/}
                                </ul>
                            </li>
                        </ul>

                    ))}
                </div>

                <div className="pagination-div">
                    <div className="pagination">
                        {prev && (
                            <div className="page_button" id="prev" onClick={clickPrev}>
                                이전
                            </div>
                        )}

                        {pageArr.map((pagenum) => (
                            <div
                                className="page_button"
                                key={pagenum}
                                onClick={() => {
                                    getAll(pagenum, range);
                                }}
                            >
                                {pagenum}
                            </div>
                        ))}

                        {next && (
                            <div className="page_button" id="next" onClick={clickNext}>
                                다음
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    </>
  );
};

export default SearchNews;
