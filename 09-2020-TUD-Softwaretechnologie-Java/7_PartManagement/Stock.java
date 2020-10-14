import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public abstract class Stock {
    private Map<Part, Integer> parts;
    private List<StockObserver> observers;

    public int getCount(Part part){
        if (part == null){
            throw new NullPointerException();
        }
        if(parts.containsKey(part)){
            return parts.get(part);
        }
        return -1;
    }

    public boolean insert(Part part, int amount){
        if (part == null){
            throw new NullPointerException();
        }
        if (amount < 1){
            throw new IllegalArgumentException();
        }
        if (parts == null){
            parts = new HashMap<>();
            parts.put(part, amount);
            notifyPartCountChanged(part);
            return true;
        }
        else if (parts.containsKey(part)){
            parts.put(part, parts.get(part)+amount);
            notifyPartCountChanged(part);
            return true;
        }
        else{
            parts.put(part, amount);
            notifyPartCountChanged(part);
            return true;
        }
    }

    public boolean remove(Part part, int amount){
        if (part == null){
            throw new NullPointerException();
        }
        if (amount < 1){
            throw new IllegalArgumentException();
        }
        if (parts == null){
            parts = new HashMap<>();
        }
        if(parts.get(part)!=null) {
            if (parts.get(part) >= amount) {
                parts.put(part, parts.get(part) - amount);
                notifyPartCountChanged(part);
                return true;
            }
        }
        return false;
    }

    public void addObserver(StockObserver observer){
        if (observer == null){
            throw new NullPointerException();
        }
        if (observers == null){
            observers = new ArrayList<>();
        }
        observers.add(observer);
    }

    private void notifyPartCountChanged(Part part){
        if (part == null){
            throw new NullPointerException();
        }
        if(observers != null){
            for (StockObserver observer : observers){
                observer.onPartCountChanged(part, parts.get(part));
            }
        }
    }
}
