package kr.hwaner.spring.hint.user;

import kr.hwaner.spring.hint.util.GenericService;

import java.util.Optional;

/**
 * @author hwaner
 */
public interface UserService extends GenericService<User> {

    User save(User user);
    Optional<User> findByEmailId(String emailId);
    void readCsv();
    Optional<User> findByUserId(Long userId);

}
