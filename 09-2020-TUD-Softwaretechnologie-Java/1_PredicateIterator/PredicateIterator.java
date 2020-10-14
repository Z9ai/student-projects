import java.util.Iterator;
import java.util.NoSuchElementException;

public class PredicateIterator<T> implements Iterator<T> {
    private Iterator<T> iter;
    private Predicate<T> predicate;

    public PredicateIterator(Iterator<T> iter, Predicate<T> predicate){
        this.iter = iter;
        this.predicate = predicate;
    }

    public boolean hasNext(){
        T item = null;
        Iterator<T> iterN = iter;
        while(iterN.hasNext()){
            item = iterN.next();
            if(predicate.test(item)){
                return true;
            }
        }
        return false;
    }

    public T  next(){
        T item = null;
        Iterator<T> iterN = iter;
        while(iterN.hasNext()){
            item = iterN.next();
            if(predicate.test(item)){
                return item;
            }
        }
        throw new NoSuchElementException();
    }
}
