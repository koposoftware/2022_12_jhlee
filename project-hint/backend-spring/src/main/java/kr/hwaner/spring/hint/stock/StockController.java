package kr.hwaner.spring.hint.stock;

import kr.hwaner.spring.hint.util.Pagination;
import lombok.AllArgsConstructor;
import org.json.simple.parser.ParseException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * @author hwaner
 */
@RestController
@AllArgsConstructor
@CrossOrigin(origins = "*", allowedHeaders = "*")
@RequestMapping("/stocks")
public class StockController {

    private static final Logger logger = LoggerFactory.getLogger(StockController.class);
    private StockService stockService;
    private final Pagination pagination;

    @GetMapping("/csv")
    public void readCsv() {
        stockService.readCSV();
    }

    @GetMapping("/pagination/{page}/{range}")
    public Map<?,?> pagination(@PathVariable int page, @PathVariable int range) throws ParseException {
        System.out.println(page + ", " + range);
        pagination.pageInfo(page, range, Math.toIntExact(stockService.count()));
        Map<String, Object> box = new HashMap<>();
        box.put("pagination", pagination);
        box.put("list", stockService.pagination(pagination));
        return box;
    }

    @GetMapping("/search/{stockSearch}")
    public Map<?,?> searchStock(@PathVariable String stockSearch){
        System.out.println("stock:" + stockSearch);
        Map<String, Object> box = new HashMap<>();
        box.put("list", stockService.findByStockSearchWordPage(stockSearch));
        return box;
    }

    @GetMapping("/marketprices")
    public List<CrawledStockVO> getStockPrice() throws ParseException {
        return  stockService.allStock();
    }

    @GetMapping("/{symbol}")
    public CrawledStockVO getStockDetail(@PathVariable String symbol) throws ParseException {
        logger.info("/stocks/{stockId}");
        return stockService.getOneStock(symbol);
    }

//    @GetMapping("/candles")
//    public List<CrawledStockVO> getCandle() {
//        logger.info("/candle");
//        return stockService.candleCarts();
//    }

}


