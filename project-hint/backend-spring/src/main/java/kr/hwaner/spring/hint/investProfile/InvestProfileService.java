package kr.hwaner.spring.hint.investProfile;

import kr.hwaner.spring.hint.util.GenericService;

import java.util.Optional;

/**
 * @author hwaner
 */
interface InvestProfileService extends GenericService<InvestProfile> {

    void save(InvestProfileVO investProfile);

    void update(InvestProfileVO investProfile);

    Optional<InvestProfile> findByInvestProfileId(Long id);

    void readCsv();

    InvestProfile findOne(Long userId);
}
