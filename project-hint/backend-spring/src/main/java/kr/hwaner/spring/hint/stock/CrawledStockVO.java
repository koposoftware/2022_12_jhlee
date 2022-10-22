package kr.hwaner.spring.hint.stock;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

/**
 * @author hwaner
 */
@Getter @Setter
@ToString
@JsonIgnoreProperties(ignoreUnknown = true)
public class CrawledStockVO {

    private String stockName, symbol, date, now, open, high, low, close, volume, transacAmount,
            dod, capital, dayDepth, dayRate, dayRateColor;

//    private String stockName, symbol, date, now, high, low, close, volume, transacAmount,
//            dod, dayDepth, dayRate, dayRateColor;
}
