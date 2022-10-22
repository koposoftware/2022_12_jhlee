package kr.hwaner.spring.hint.user;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;
import com.querydsl.core.types.dsl.PathInits;


/**
 * QUser is a Querydsl query type for User
 */
@Generated("com.querydsl.codegen.DefaultEntitySerializer")
public class QUser extends EntityPathBase<User> {

    private static final long serialVersionUID = 717886890L;

    private static final PathInits INITS = PathInits.DIRECT2;

    public static final QUser user = new QUser("user");

    public final ListPath<kr.hwaner.spring.hint.asset.Asset, kr.hwaner.spring.hint.asset.QAsset> assetList = this.<kr.hwaner.spring.hint.asset.Asset, kr.hwaner.spring.hint.asset.QAsset>createList("assetList", kr.hwaner.spring.hint.asset.Asset.class, kr.hwaner.spring.hint.asset.QAsset.class, PathInits.DIRECT2);

    public final StringPath emailId = createString("emailId");

    public final kr.hwaner.spring.hint.investProfile.QInvestProfile investProfile;

    public final StringPath name = createString("name");

    public final StringPath nickname = createString("nickname");

    public final StringPath password = createString("password");

    public final NumberPath<Long> userId = createNumber("userId", Long.class);

    public QUser(String variable) {
        this(User.class, forVariable(variable), INITS);
    }

    public QUser(Path<? extends User> path) {
        this(path.getType(), path.getMetadata(), PathInits.getFor(path.getMetadata(), INITS));
    }

    public QUser(PathMetadata metadata) {
        this(metadata, PathInits.getFor(metadata, INITS));
    }

    public QUser(PathMetadata metadata, PathInits inits) {
        this(User.class, metadata, inits);
    }

    public QUser(Class<? extends User> type, PathMetadata metadata, PathInits inits) {
        super(type, metadata, inits);
        this.investProfile = inits.isInitialized("investProfile") ? new kr.hwaner.spring.hint.investProfile.QInvestProfile(forProperty("investProfile"), inits.get("investProfile")) : null;
    }

}

