package kr.hwaner.spring.hint.investProfile;

/**
 * @author hwaner
 */
interface IInvestProfileRepository {

    InvestProfile findByUserId(Long userId);
}
