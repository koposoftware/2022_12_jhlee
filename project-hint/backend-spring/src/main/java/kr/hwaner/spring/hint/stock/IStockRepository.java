package kr.hwaner.spring.hint.stock;

import kr.hwaner.spring.hint.util.Pagination;

import java.util.List;

/**
 * @author hwaner
 */
interface IStockRepository {

    List<Stock> pagination(Pagination pagination);

    List<String> findAllSymbol();

    String findBySymbol(String symbol);

    List<String> findMiniListed();

    List<Stock> selectByStockNameLikeSearchWord(String stockSearch);

    Iterable<Stock> selectByStockNameLikeSearchWordPage(String stockSearch);
}
