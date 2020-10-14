import java.util.Iterator;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;

public class EventCatalogImpl extends TreeMap<Event, Set<Time>> implements EventCatalog{

    @Override
    public boolean addCatalogEntry(Event e, Set<Time> tSet) {
        if(e==null || tSet==null){
            throw new NullPointerException();
        }
        Iterator it = tSet.iterator();
        while (it.hasNext()){
            Time t = (Time)it.next();
            if ((t.getHour()<0) || (t.getHour()>23) || (t.getMinute()<0) || (t.getMinute()>59) ) {
                throw new IllegalArgumentException();
            }
        }
        if(this.containsKey(e)){
            return false;
        }
        else{
            this.put(e, tSet);
            return true;
        }
    }

    @Override
    public boolean addTimeToEvent(Event e, Time t){
        if(e==null || t==null){
            throw new NullPointerException();
        }
        Set<Time> tSet;
        if(this.containsKey(e)){
            tSet = this.get(e);
            if(tSet.contains(t)){
                return false;
            }
            tSet.add(t);
            this.put(e,tSet);
            return true;
        }
        return false;
    }

    @Override
    public Set<Event> getAllEvents(){
        return this.keySet();
    }

    @Override
    public Set<Time> getTimesOfEvent(Event e) {
        if(e==null){
            throw new NullPointerException();
        }
        if(this.containsKey(e)){
            return this.get(e);
        }
        return null;
    }

    @Override
    public Map<Event, Set<Time>> filterByEventCategory(EventCategory category) {
        if(category==null){
            throw new NullPointerException();
        }
        Map<Event, Set<Time>> filtered = new TreeMap();
        for(Map.Entry<Event, Set<Time>> entry : this.entrySet()){
            if(entry.getKey().getCategory()==category){
                filtered.put(entry.getKey(),entry.getValue());
            }
        }
        return filtered;
    }

    @Override
    public Set<Time> deleteEvent(Event e) {
        if(e==null){
            throw new NullPointerException();
        }
        if(this.containsKey(e)){
            Set<Time> temp = this.get(e);
            this.remove(e);
            return temp;
        }
        return null;
    }

    @Override
    public boolean deleteTime(Event e, Time t) {
        if(e==null || t==null){
            throw new NullPointerException();
        }
        Set<Time> tSet;
        if(this.containsKey(e)){
            tSet = this.get(e);
            for(Time time :tSet){
                if (time == t){
                    tSet.remove(t);
                    this.put(e, tSet);
                    return true;
                }
            }
        }
        return false;
    }
}

