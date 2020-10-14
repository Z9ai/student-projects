import java.util.HashSet;
import java.util.Set;

public abstract class JContent {
    private String title;
    private String description;
    private Set<ContentObserver> observers = new HashSet<>();

    public JContent(String title, String description) {
        if (title == "" || description == ""){
            throw new IllegalArgumentException();
        }
        if(title == null || description == null){
            throw new NullPointerException();
        }
        this.title = title;
        this.description = description;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        if(description == null){
            throw new NullPointerException();
        }
        if(description == ""){
            throw new IllegalArgumentException();
        }
        this.description = description;

        for (ContentObserver observer : observers){
            observer.update(this);
        }
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        if(title == null){
            throw new NullPointerException();
        }
        if(title == ""){
            throw new IllegalArgumentException();
        }
        this.title = title;
        for (ContentObserver observer : observers){
            observer.update(this);
        }
    }

    public void addObserver(ContentObserver observer){
        if(observer == null){
            throw new NullPointerException();
        }
        observers.add(observer);
    }

    public void removeObserver(ContentObserver observer){
        if(observer == null){
            throw new NullPointerException();
        }
        observers.remove(observer);
    }
    public int countObservers(){
        return observers.size();
    }

    public abstract String toString();
}
