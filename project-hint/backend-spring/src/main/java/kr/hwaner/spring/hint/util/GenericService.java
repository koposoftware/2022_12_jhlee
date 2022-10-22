package kr.hwaner.spring.hint.util;

/**
 * @author hwaner
 */
public interface GenericService<T> {

    public Iterable<T> findAll();
    public int count();
    public void delete(T t);
    public boolean exists(String id);

}
