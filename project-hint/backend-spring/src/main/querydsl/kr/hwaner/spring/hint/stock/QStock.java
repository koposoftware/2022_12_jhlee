package kr.hwaner.spring.hint.stock;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;
import com.querydsl.core.types.dsl.PathInits;


/**
 * QStock is a Querydsl query type for Stock
 */
@Generated("com.querydsl.codegen.DefaultEntitySerializer")
public class QStock extends EntityPathBase<Stock> {

    private static final long serialVersionUID = 1982403738L;

    public static final QStock stock = new QStock("stock");

    public final ListPath<kr.hwaner.spring.hint.asset.Asset, kr.hwaner.spring.hint.asset.QAsset> assetList = this.<kr.hwaner.spring.hint.asset.Asset, kr.hwaner.spring.hint.asset.QAsset>createList("assetList", kr.hwaner.spring.hint.asset.Asset.class, kr.hwaner.spring.hint.asset.QAsset.class, PathInits.DIRECT2);

    public final NumberPath<Long> stockId = createNumber("stockId", Long.class);

    public final StringPath stockName = createString("stockName");

    public final StringPath symbol = createString("symbol");

    public QStock(String variable) {
        super(Stock.class, forVariable(variable));
    }

    public QStock(Path<? extends Stock> path) {
        super(path.getType(), path.getMetadata());
    }

    public QStock(PathMetadata metadata) {
        super(Stock.class, metadata);
    }

}

