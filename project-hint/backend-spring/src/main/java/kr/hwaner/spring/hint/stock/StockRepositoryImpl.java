package kr.hwaner.spring.hint.stock;

import com.querydsl.core.types.Projections;
import com.querydsl.jpa.impl.JPAQueryFactory;
import kr.hwaner.spring.hint.util.Pagination;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.data.jpa.repository.support.QuerydslRepositorySupport;
import org.springframework.stereotype.Repository;

import javax.sql.DataSource;
import java.util.ArrayList;
import java.util.List;

import static kr.hwaner.spring.hint.stock.QStock.stock;

/**
 * @author hwaner
 */
@Repository
public class StockRepositoryImpl extends QuerydslRepositorySupport implements IStockRepository {

    private static final Logger logger = LoggerFactory.getLogger(StockRepositoryImpl.class);
    private final JPAQueryFactory queryFactory;
    private final DataSource dataSource;

    public StockRepositoryImpl(JPAQueryFactory queryFactory, DataSource dataSource) {
        super(Stock.class);
        this.queryFactory = queryFactory;
        this.dataSource = dataSource;
    }

    @Override
    public List<String> findAllSymbol() {
        logger.info("StockRepositoryImpl  : findAllSymbol()");
        return queryFactory.select(stock.symbol)
                .from(stock)
                .fetch();
    }

    @Override
    public List<String> findMiniListed() {
        logger.info("StockRepositoryImpl  : findMiniListed()");
        return queryFactory.select(stock.symbol)
                .from(stock)
                .limit(135)
                .fetch();
    }

    @Override
    public List<Stock> selectByStockNameLikeSearchWord(String stockSearch) {
        return queryFactory.selectFrom(stock)
                .where(stock.stockName.like("%"+stockSearch+"%"))
                .fetch();
    }

    @Override
    public Iterable<Stock> selectByStockNameLikeSearchWordPage(String stockSearch) {
        QStock qs = stock;
        List<Stock> result = new ArrayList<>();
        result = queryFactory.selectDistinct(Projections.fields(Stock.class,
                stock.stockId, stock.symbol, stock.stockName))
                .where(stock.stockName.like("%"+stockSearch+"%"))
                .from(stock)
                .orderBy(stock.stockId.desc())
                .limit(8)
                .fetch();
        System.out.println("stock result: "+result);
        System.out.println("stock result: "+result.size());
        return result;
    }

    @Override
    public List<Stock> pagination(Pagination pagination) {
        return queryFactory.selectFrom(stock).orderBy(stock.stockId.asc())
                .offset(pagination.getStartList()).limit(pagination.getListSize()).fetch();
    }

//    @Override
//    public List<List<String>>paginationStock(Pagination pagination) {
//        logger.info("StockRepositoryImpl  : paginationStock()...pagination&&stock");
//        List<List<String>>paginationStock = new ArrayList<>();
//
//        List<>
//
//        return
//    }

    @Override
    public String findBySymbol(String symbol) {
        return queryFactory.select(stock.stockName)
                .from(stock)
                .fetchFirst();
    }
}
