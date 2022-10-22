package kr.hwaner.spring.hint.investProfile;

import kr.hwaner.spring.hint.user.UserRepository;
import lombok.AllArgsConstructor;
import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVRecord;
import org.springframework.stereotype.Service;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.Optional;

/**
 * @author hwaner
 */
@Service
@AllArgsConstructor
public class InvestProfileServiceImpl implements InvestProfileService {

    private final InvestProfileRepository repository;
    private final UserRepository userRepository;

    @Override
    public void save(InvestProfileVO investProfile) {

        InvestProfile ip = new InvestProfile(investProfile.getInvestmentPeriod(), investProfile.getInvestmentPropensity(), investProfile.getUser());
        repository.save(ip);
    }

    @Override
    public void update(InvestProfileVO investProfile) {

        InvestProfile ip = repository.findByUserId(investProfile.getUser().getUserId());
        ip.setUser(userRepository.findById(investProfile.getUser().getUserId()).get());
        ip.setInvestmentPropensity(investProfile.getInvestmentPropensity());
        ip.setInvestmentPeriod(investProfile.getInvestmentPeriod());
        repository.save(ip);
    }

    @Override
    public Optional<InvestProfile> findByInvestProfileId(Long id) {
        return Optional.empty();
    }

    @Override
    public void readCsv() {

        InputStream is = getClass().getResourceAsStream("/static/investProfile.csv");
        try {
            BufferedReader fileReader = new BufferedReader(new InputStreamReader(is, "UTF-8"));
            CSVParser csvParser = new CSVParser(fileReader, CSVFormat.DEFAULT);
            Iterable<CSVRecord> csvRecords = csvParser.getRecords();
            for(CSVRecord csvRecord : csvRecords){
                long i = 1;
                repository.save(new InvestProfile(
                        csvRecord.get(0),
                        csvRecord.get(1),
                        userRepository.findById(Long.parseLong(csvRecord.get(2))).get()
                ));
                i = i + 1;
            }
        } catch (Exception e){
            e.printStackTrace();
        }
    }

    @Override
    public InvestProfile findOne(Long userId) {
        return repository.findByUserId(userId);
    }

    @Override
    public Iterable<InvestProfile> findAll() {
        return null;
    }

    @Override
    public int count() {
        return (int) repository.count();
    }

    @Override
    public void delete(InvestProfile investProfile) {

    }

    @Override
    public boolean exists(String id) {
        return false;
    }
}
