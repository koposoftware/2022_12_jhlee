package kr.hwaner.spring.hint.user;

import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

/**
 * @author hwaner
 */
public interface UserRepository extends JpaRepository<User, Long>, IUserRepository {

    Optional<User> findByEmailId(String emailId);

    Boolean existsByEmailId(String emailId);

}
