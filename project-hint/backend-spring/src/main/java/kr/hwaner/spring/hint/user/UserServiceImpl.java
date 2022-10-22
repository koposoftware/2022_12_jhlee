package kr.hwaner.spring.hint.user;

import kr.hwaner.spring.hint.asset.Asset;
import kr.hwaner.spring.hint.asset.AssetRepository;
import kr.hwaner.spring.hint.asset.Transaction;
import kr.hwaner.spring.hint.asset.TransactionRepository;
import lombok.AllArgsConstructor;
import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVRecord;
import org.springframework.stereotype.Service;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Optional;

/**
 * @author hwaner
 */
@Service
@AllArgsConstructor
public class UserServiceImpl implements UserService {

    private final UserRepository repository;
    private final AssetRepository assetRepository;
    private final TransactionRepository transactionRepository;

    @Override
    public User save(User user) {

        User returnUser = repository.save(user);
        Asset asset = new Asset();
        asset.setTotalAsset(10000000);
        asset.setUser(returnUser);
        assetRepository.save(asset);
        transactionRepository.save(new Transaction(
                "",
                10000000,
                new SimpleDateFormat("yyyy. MM. dd.").format(new Date()),
                "초기 자금",
                user.getUserId(),
                10000000));
        return returnUser;
    }

    @Override
    public Optional<User> findByEmailId(String emailId) {
        return repository.findByEmailId(emailId);
    }

    @Override
    public void readCsv() {

        InputStream is = getClass().getResourceAsStream("/static/users.csv");
        try {
            BufferedReader fileReader = new BufferedReader(new InputStreamReader(is, "UTF-8"));
            CSVParser parser = new CSVParser(fileReader, CSVFormat.DEFAULT);
            Iterable<CSVRecord> csvRecords = parser.getRecords();
            for (CSVRecord csvRecord : csvRecords) {
                repository.save(new User(
                        csvRecord.get(0),
                        csvRecord.get(1),
                        csvRecord.get(3),
                        csvRecord.get(2)
                ));
            }
        } catch (Exception e) {

            e.printStackTrace();
        }
    }

    @Override
    public Optional<User> findByUserId(Long id) {
        return repository.findById(id);
    }

    @Override
    public Iterable<User> findAll() {
        return null;
    }

    @Override
    public int count() {
        return 0;
    }

    @Override
    public void delete(User user) {
        repository.delete(user);
    }

    @Override
    public boolean exists(String emailId) {
        return repository.existsByEmailId(emailId);
    }
}
