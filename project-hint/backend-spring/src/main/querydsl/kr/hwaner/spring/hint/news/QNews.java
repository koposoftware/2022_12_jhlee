package kr.hwaner.spring.hint.news;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;


/**
 * QNews is a Querydsl query type for News
 */
@Generated("com.querydsl.codegen.DefaultEntitySerializer")
public class QNews extends EntityPathBase<News> {

    private static final long serialVersionUID = 679230122L;

    public static final QNews news = new QNews("news");

    public final StringPath newsContent = createString("newsContent");

    public final NumberPath<Long> newsId = createNumber("newsId", Long.class);

    public final StringPath newsLink = createString("newsLink");

    public final StringPath newsRegDate = createString("newsRegDate");

    public final StringPath newsThumbnail = createString("newsThumbnail");

    public final StringPath newsTitle = createString("newsTitle");

    public QNews(String variable) {
        super(News.class, forVariable(variable));
    }

    public QNews(Path<? extends News> path) {
        super(path.getType(), path.getMetadata());
    }

    public QNews(PathMetadata metadata) {
        super(News.class, metadata);
    }

}

