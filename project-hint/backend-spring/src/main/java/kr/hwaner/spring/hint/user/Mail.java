package kr.hwaner.spring.hint.user;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;

/**
 * @author hwaner
 */
@Getter @Setter
@ToString
@NoArgsConstructor
public class Mail {

    private String address, title, message;
}
