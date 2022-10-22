package kr.hwaner.spring.hint.investProfile;

import kr.hwaner.spring.hint.user.User;
import lombok.*;

/**
 * @author hwaner
 */
@Getter @Setter
@ToString
@NoArgsConstructor
public class InvestProfileVO {

    private User user;
    private String investmentPeriod, investmentPropensity;
}


