package kr.hwaner.spring.hint.user;

/**
 * @author hwaner
 */
public interface MailService {
    void mailSend(User user);
    String init();
}
