package kr.hwaner.spring.hint.user;

import com.querydsl.jpa.impl.JPAQueryFactory;
import org.springframework.data.jpa.repository.support.QuerydslRepositorySupport;
import org.springframework.stereotype.Repository;

import javax.sql.DataSource;

/**
 * @author hwaner
 */
@Repository
public class UserRepositoryImpl extends QuerydslRepositorySupport implements IUserRepository {

    private final JPAQueryFactory queryFactory;
    private final DataSource dataSource;

    public UserRepositoryImpl(JPAQueryFactory queryFactory, DataSource dataSource) {
        super(User.class);
        this.queryFactory = queryFactory;
        this.dataSource = dataSource;
    }

}
