package kr.hwaner.spring.hint.news;

import kr.hwaner.spring.hint.util.GenericService;
import kr.hwaner.spring.hint.util.Pagination;

import java.util.List;

/**
 * @author hwaner
 */
public interface NewsService extends GenericService<News> {
    void readCsv();

    News getNewsDetailById(Long newsId);

    List<News> pagination(Pagination pagination);

    List<News> showNewsList();

    List<News> findByNewsSearchWord(String newsSearch);

    Object findByNewsSearchWordPage(String newsSearch, Pagination pagination);
}
