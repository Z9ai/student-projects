import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class JMember implements  ContentObserver{
    private Set<JTopic> topics = new HashSet<>();

    public void subscribe(JTopic topic){
        topic.addObserver(this);
        topics.add(topic);
    }

    public void unsubscribe(JTopic topic){
        topic.removeObserver(this);
        topics.remove(topic);
    }

    public void update(JContent content){

        for(JTopic topic : topics){

            if (content == topic){
                System.out.println("The topic "+topic.getId()+ " has been updated!");
            }
        }
    }

    public Set<JTopic> getSubscribedTopics(){
        return topics;
    }
}
