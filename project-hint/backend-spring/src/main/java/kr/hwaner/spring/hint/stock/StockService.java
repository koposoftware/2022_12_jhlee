package kr.hwaner.spring.hint.stock;

import kr.hwaner.spring.hint.util.GenericService;
import kr.hwaner.spring.hint.util.Pagination;
import org.json.simple.parser.ParseException;

import java.util.List;
import java.util.Optional;

/**
 * @author hwaner
 */
public interface StockService extends GenericService<Stock> {

    Optional<Stock> findById(String id);

    void save(Stock stock);

    void readCSV();

    List<CrawledStockVO> allStock() throws ParseException;

    CrawledStockVO getOneStock(String symbol) throws ParseException;

    List<CrawledStockVO> pagination(Pagination pagination) throws ParseException;

    Object findByStockSearchWordPage(String stockSearch);
}

