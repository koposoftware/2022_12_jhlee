package kr.hwaner.spring.hint.stock;

import com.google.gson.Gson;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import kr.hwaner.spring.hint.util.Pagination;
import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVRecord;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;
import org.jsoup.Connection;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

/**
 * @author hwaner
 */
@Service
class StockServiceImpl implements StockService {

    private static final Logger logger = LoggerFactory.getLogger(StockServiceImpl.class);
    private final StockRepository repository;

    StockServiceImpl(StockRepository repository) {
        this.repository = repository;
    }

    @Override
    public void save(Stock stock) {
    }

    @Override
    public Optional<Stock> findById(String id) {
        return Optional.empty();
    }

    public Optional<Stock> findById(Long id) {
        return Optional.empty();
    }

    @Override
    public Iterable<Stock> findAll() {
        return null;
    }

    @Override
    public int count() {
        return (int) repository.count();
    }

    @Override
    public void delete(Stock stock) {
    }

    @Override
    public boolean exists(String id) {
        return false;
    }

    @Override
    public void readCSV() {

        logger.info("StockServiceImpl : readCSV()");
        
        try {
            BufferedReader fileReader = new BufferedReader(new InputStreamReader(is, "UTF-8"));
            CSVParser csvParser = new CSVParser(fileReader, CSVFormat.DEFAULT);
            Iterable<CSVRecord> csvRecords = csvParser.getRecords();
            for (CSVRecord csvRecord : csvRecords) {
                repository.save(new Stock(
                        csvRecord.get(1),
                        csvRecord.get(2),
                        new ArrayList<>()
                ));
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @Override
    public List<CrawledStockVO> allStock() throws ParseException {

        List<CrawledStockVO> cralwedResults = new ArrayList<>();
//        List<String> listedSymbols = repository.findAllSymbol();
//        for(String stockCode: listedSymbols){
//            t.add(stockCrawling(stockCode)) ;
//        }
        List<String> miniListed = repository.findMiniListed();
        for (String stockCode : miniListed) {
            cralwedResults.add(stockCrawling(stockCode));
        }

        return cralwedResults;
    }

    @Override
    public CrawledStockVO getOneStock(String symbol) throws ParseException {

        CrawledStockVO vo = stockCrawling(symbol);
        return vo;
    }

    private CrawledStockVO stockCrawling(String stockCode) {

        CrawledStockVO vo = null;
        try {
//            String url = "https://finance.naver.com/item/main.nhn?code=" + stockCode;
            String url = "https://finance.naver.com/item/sise.naver?code=" + stockCode;
            Connection.Response homepage = Jsoup.connect(url).method(Connection.Method.GET)
                    .userAgent("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36")
                    .execute();
            Document d = homepage.parse();

            Elements getName = d.select("div.wrap_company");
            Elements getH2 = getName.select("h2");
            Elements stockName = getH2.select("a");

            Elements symbol = d.select("span.code");

            Elements table = d.select("table.no_info");
            Elements trs = table.select("tr");
            Element firstTr = trs.get(0);
            Elements firstTrTds = firstTr.select("td");
            Element high = firstTrTds.get(0);
            Element close = firstTrTds.get(1);
            Element volume = firstTrTds.get(2);

            Elements table2 = d.select("table.type_tax");
            Elements trs2 = table2.select("tr");
            Element selTr = trs2.get(2);
            Elements selTrTds = selTr.select("td");
            Element dayRateSel = selTrTds.get(0);
            Elements dayRate = dayRateSel.select("span.tah");

            Element secondTr = trs.get(1);
            Elements secondTrTds = secondTr.select("td");
            Element open = secondTrTds.get(0);
            Element low = secondTrTds.get(1);
            Element transacAmount = secondTrTds.get(2);

            Elements now = d.select("p.no_today");
            Elements nowBlind = now.select("span.blind");
            Elements openBlind = open.select("span.blind");
            Elements highBlind = high.select("span.blind");
            Elements lowBlind = low.select("span.blind");
            Elements closeBlind = close.select("span.blind");
            Elements volumeBlind = volume.select("span.blind");
            Elements transacAmountBlind = transacAmount.select("span.blind");
            Elements crawledDate = d.select("#time");

            Elements dod = d.select("p.no_exday");
            Elements dodblind = dod.select("span.blind");

            Elements capital = d.select("#_market_sum");

            for (int i = 0; i < symbol.size(); i++) {
                vo = new CrawledStockVO();
                vo.setStockName(stockName.get(i).text());
                System.out.println("stockName = " + vo.getStockName());
                vo.setSymbol(symbol.get(i).text());
                vo.setNow(nowBlind.get(i).text());
                System.out.println("현재가 = " + vo.getNow());
                vo.setHigh(highBlind.get(i).text());
                vo.setLow(lowBlind.get(i).text());
                vo.setOpen(openBlind.get(i).text());
                vo.setClose(closeBlind.get(i).text());
                vo.setVolume(volumeBlind.get(i).text());
                vo.setDate(crawledDate.get(i).text());
                vo.setTransacAmount(transacAmountBlind.get(i).text());

                int dodCustom =
                        Integer.parseInt(delComma(nowBlind.get(i).text()))
                                - Integer.parseInt(delComma(highBlind.get(i).text()));
                String dodCustomStr = Integer.toString(dodCustom);
                addComma(dodCustomStr);
                String resDodCustomStr;
                if (!dodCustomStr.contains("-") && !dodCustomStr.equals("0")) {
                    resDodCustomStr = "+" + dodblind.get(i).text();
                } else if (dodCustomStr.contains("-")){
                    resDodCustomStr = "-" + dodblind.get(i).text();
                } else {
                    resDodCustomStr = dodblind.get(i).text();
                }

                vo.setDayDepth(resDodCustomStr);
                System.out.println("전일대비 = " + resDodCustomStr);

                vo.setDod(dodblind.get(i).text());
                vo.setCapital(capital.get(i).text());
                vo.setDayRate(dayRate.get(i).text());
                System.out.println("전일대비 = " + vo.getDayRate());
                String dayRateColor = vo.getDayRate().contains("-")? "blue" : vo.getDayRate().contains("+")? "red": "zero";
                vo.setDayRateColor(dayRateColor);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

        return vo;
    }

//    private CrawledStockVO stockCrawling(String stockCode) throws ParseException {
//
//        CrawledStockVO vo = null;
//        StringBuilder result = new StringBuilder();
//        try {
//
//            URL url = new URL("http://127.0.0.1:5000/api/stock/realdata");
//            HttpURLConnection con = (HttpURLConnection) url.openConnection();
//            con.setRequestMethod("GET");
//            con.setRequestProperty("Content-type", "application/json");
//            con.setDoOutput(true);
//
//            BufferedReader br = new BufferedReader(
//                    new InputStreamReader(con.getInputStream(), StandardCharsets.UTF_8));
//            while(br.ready()) {
//                result.append(br.readLine());
//            }
//            System.out.println("result = " + result);
//            con.disconnect();
//
//        } catch(Exception e) {
//            e.printStackTrace();
//        }
//            JSONParser jsonParser = new JSONParser();
//            JSONObject jsonObject = (JSONObject)jsonParser.parse(result.toString());
//            JSONObject realData = (JSONObject)jsonObject.get(stockCode);
//
//            String symbolJ = String.valueOf(realData.get("symbol"));
//            String stockNameJ = String.valueOf(realData.get("stockName"));
//            String nowJ = String.valueOf(realData.get("now"));
//            String highJ = String.valueOf(realData.get("high"));
//            String lowJ = String.valueOf(realData.get("low"));
//            String closeJ = String.valueOf(realData.get("close"));
//            String volumeJ = String.valueOf(realData.get("volume"));
//            String transacAmountJ = String.valueOf(realData.get("transacAmount"));
//            String dayRateJ = String.valueOf(realData.get("dayRate"));
//            String dateJ = String.valueOf(realData.get("date"));
//
//            vo = new CrawledStockVO();
//            vo.setSymbol(symbolJ);
//            vo.setStockName(stockNameJ);
//            vo.setNow(nowJ);
//            vo.setHigh(highJ);
//            vo.setLow(lowJ);
//            vo.setClose(closeJ);
//            vo.setVolume(volumeJ);
//            vo.setTransacAmount(transacAmountJ);
//            vo.setDayRate(dayRateJ);
//            vo.setDate(dateJ);
//
//
////                int dodCustom =
////                        Integer.parseInt(delComma(nowBlind.get(i).text()))
////                                - Integer.parseInt(delComma(highBlind.get(i).text()));
////                String dodCustomStr = Integer.toString(dodCustom);
////                addComma(dodCustomStr);
////                String resDodCustomStr;
////                if (!dodCustomStr.contains("-") && !dodCustomStr.equals("0")) {
////                    resDodCustomStr = "+";
////                } else if (dodCustomStr.contains("-")){
////                    resDodCustomStr = "-";
////                } else {
////                }
////
////                vo.setDayDepth("100");
////                vo.setDayRate(dayRate.get(i).text());
////                System.out.println("dayRate = " + vo.getDayRate());
////                String dayRateColor = vo.getDayRate().contains("-")? "blue" : vo.getDayRate().contains("+")? "red": "zero";
////                vo.setDayRateColor(dayRateColor);
////                System.out.println("dayRateColor = " + dayRateColor);
//
////        } catch (Exception e) {
////            e.printStackTrace();
////        }
//
//        return vo;
//    }

    @Override
    public List<CrawledStockVO> pagination(Pagination pagination) throws ParseException {
        List<CrawledStockVO> result = new ArrayList<>();
        List<Stock> crawledStock = repository.pagination(pagination);
        return getStocksVOS(result, crawledStock);
    }

    @Override
    public Object findByStockSearchWordPage(String stockSearch) {
        return repository.selectByStockNameLikeSearchWordPage(stockSearch);
    }

    private List<CrawledStockVO> getStocksVOS(List<CrawledStockVO> result, Iterable<Stock> crawledStock) throws ParseException {
        for (Stock item : crawledStock) {
            String symbol = item.getSymbol();
            result.add(stockCrawling(symbol));
        }
        return result;
    }

    public String delComma(String data) {
        if (data.contains(",")) {
            data = data.replace(",", "");
        }
        return data;
    }

    public String addComma(String data) {
        int result = Integer.parseInt(data);
        return new java.text.DecimalFormat("##,###").format(result);
    }
}
