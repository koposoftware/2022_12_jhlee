package kr.hwaner.spring.hint.investProfile;

import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

/**
 * @author hwaner
 */
public interface InvestProfileRepository extends JpaRepository<InvestProfile, Long>, IInvestProfileRepository {

}
