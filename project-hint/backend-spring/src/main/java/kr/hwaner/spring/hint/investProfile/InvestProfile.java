package kr.hwaner.spring.hint.investProfile;

import com.fasterxml.jackson.annotation.JsonBackReference;
import kr.hwaner.spring.hint.user.User;
import lombok.*;

import javax.persistence.*;

/**
 * @author hwaner
 */
@Entity
@Getter @Setter
@ToString
@NoArgsConstructor
@Table(name = "invest_profile")
public class InvestProfile {

    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "invest_profile_id")
    private Long investProfileId;

    @Column(name = "investment_period") private String investmentPeriod;
    @Column(name = "investment_propensity") private String investmentPropensity;

    @Builder
    public InvestProfile(String investmentPeriod, String investmentPropensity, User user) {
        this.investmentPeriod = investmentPeriod;
        this.investmentPropensity = investmentPropensity;
        this.user = user;
    }

    @OneToOne
    @JoinColumn(name = "user_id")
    @JsonBackReference
    private User user;

}
