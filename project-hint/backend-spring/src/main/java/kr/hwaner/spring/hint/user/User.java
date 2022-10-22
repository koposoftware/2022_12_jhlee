package kr.hwaner.spring.hint.user;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonManagedReference;
import kr.hwaner.spring.hint.asset.Asset;
import kr.hwaner.spring.hint.investProfile.InvestProfile;
import lombok.*;

import javax.persistence.*;
import java.util.List;

/**
 * @author hwaner
 */
@Entity
@Getter @Setter
@ToString
@NoArgsConstructor
@Table(name="user")
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name="user_id")
    private Long userId;

    @Column(name = "email_id") private String emailId;
    @Column(name = "password") private String password;
    @Column(name="nickname") private String nickname;
    @Column(name="name") private String name;

    @Override
    public String toString() {
        return String.format("User[email_id=%s, password='%s', name='%s', nickname='%s]",
                emailId, password, name, nickname);
    }

    @Builder
    public User(String emailId, String password, String nickname, String name) {
        this.emailId = emailId;
        this.password = password;
        this.nickname = nickname;
        this.name = name;
    }

//    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL) @JsonIgnore
//    private List<Board> boardList;
//
//    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL) @JsonIgnore
//    private List<Comment> commentList;

    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL) @JsonIgnore
    private List<Asset> assetList;

    @OneToOne(mappedBy = "user", cascade = CascadeType.ALL) @JsonManagedReference
    private InvestProfile investProfile;

}
