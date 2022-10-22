package kr.hwaner.spring.hint.news;

import kr.hwaner.spring.hint.util.Pagination;

import java.util.List;

/**
 * @author hwaner
 */
interface INewsRepository {
    List<News> showAllNews();

    News showNewsDetail(Long newsId);

    List<News> pagination(Pagination pagination);

    Iterable<News> selectByNewsTitleLikeSearchWordPage(String newsSearch, Pagination pagination);
}
