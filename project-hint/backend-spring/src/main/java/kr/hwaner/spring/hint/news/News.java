package kr.hwaner.spring.hint.news;

import lombok.*;

import javax.persistence.*;

/**
 * @author hwaner
 */
@Entity
@Getter @Setter
@ToString
@NoArgsConstructor
@Table(name = "news")
public class News {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "news_id")
    private Long newsId;

    @Column(name = "news_content", length = 8000) private String newsContent;
    @Column(name = "news_link", length = 8000) private String newsLink;
    @Column(name = "news_regdate") private String newsRegDate;
    @Column(name = "news_thumbnail", length = 8000) private String newsThumbnail;
    @Column(name = "news_title") private String newsTitle;

    @Builder
    public News(String newsRegDate, String newsTitle, String newsContent,
                String newsLink, String newsThumbnail) {
        this.newsRegDate = newsRegDate;
        this.newsTitle = newsTitle;
        this.newsContent = newsContent;
        this.newsLink = newsLink;
        this.newsThumbnail = newsThumbnail;
    }
}
