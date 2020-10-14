import java.util.*;

public class JIdeaPool {
    private Map<JTopic, Set<JIdea>> pool = new HashMap();

    public JIdeaPool() {
    }

    public void add(JTopic topic){
        if(topic == null){
            throw new NullPointerException();
        }
        if (pool.containsKey(topic)==false) {
            pool.put(topic, new HashSet<>());
        }
    }

    public void add(JIdea idea ,JTopic topic) {
        if (idea == null || topic == null) {
            throw new NullPointerException();
        }
        boolean otherIdeaContainsSameTitle = false;
        for (Map.Entry entry : pool.entrySet()) {
            Set<JIdea> ideas = (Set<JIdea>) entry.getValue();
            for (JIdea ideaN : ideas) {
                if (ideaN.getTitle() == idea.getTitle() && ideaN != idea) {
                    otherIdeaContainsSameTitle = true;
                    break;
                }
            }
        }
        if (otherIdeaContainsSameTitle == false) {
            if (pool.containsKey(topic)) {
                pool.get(topic).add(idea);
            } else {
                Set<JIdea> ideas = new HashSet<>();
                ideas.add(idea);
                pool.put(topic, ideas);
            }
        }
    }

    public boolean remove(JTopic topic){
        if(topic == null){
            throw new NullPointerException();
        }
        if(pool.containsKey(topic)){
            pool.remove(topic);
            return true;
        }
        return false;
    }

    public boolean remove(JIdea idea){
        if(idea == null){
            throw new NullPointerException();
        }
        boolean removed = false;
        for(Map.Entry entry : pool.entrySet()){
            Set<JIdea> ideas = (Set<JIdea>)entry.getValue();
            if(ideas.contains(idea)){
                ideas.remove(idea);
                removed = true;
            }
        }
        return removed;
    }

    public JIdea getIdea(String title){
        if(title == null){
            throw new NullPointerException();
        }
        if(title == ""){
            throw new IllegalArgumentException();
        }
        for(Map.Entry entry : pool.entrySet()) {
            Set<JIdea> ideas = (Set<JIdea>) entry.getValue();
            for (JIdea idea : ideas) {
                if (idea.getTitle() == title) {
                    return idea;
                }
            }
        }
        return null;
    }

    public int numberOfTopics(){
        return pool.size();
    }

    public int numberOfIdeas() {
        int number = 0;
        Set<JIdea> allIdeas = new HashSet<>();
        for (Map.Entry entry : pool.entrySet()) {
            Set<JIdea> ideas = (Set<JIdea>) entry.getValue();
            for (JIdea idea : ideas){
                allIdeas.add(idea);
            }
        }
        return allIdeas.size();
    }

    public void removeReleased(){
        for(Map.Entry entry : pool.entrySet()) {
            Set<JIdea> ideas = (Set<JIdea>) entry.getValue();
            Iterator it = ideas.iterator();
            while (it.hasNext()) {
                JIdea ideaN = (JIdea)it.next();
                if(ideaN.isReleased()){
                    it.remove();
                }
            }
        }
    }

    public void removeDeclined(){
        for(Map.Entry entry : pool.entrySet()) {
            Set<JIdea> ideas = (Set<JIdea>) entry.getValue();
            Iterator it = ideas.iterator();
            while (it.hasNext()) {
                JIdea ideaN = (JIdea)it.next();
                if(ideaN.isDeclined()){
                    it.remove();
                }
            }
        }
    }
}
