package kr.hwaner.spring.hint.stock;

import org.springframework.data.jpa.repository.JpaRepository;

/**
 * @author hwaner
 */
public interface StockRepository extends JpaRepository<Stock, Long>, IStockRepository {

    Stock findByStockName(String stockName);
}


