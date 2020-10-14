import java.util.*;

public class Index {
    private Map<String,List<Resource>> index = new HashMap<>();

    public Index(){
    }

    public void add(Resource res){
        Set<String> keywords = res.getType().getCollector().getKeywords(res);
        for(String keyword: keywords){
            if (index.containsKey(keyword)){
                List<Resource> newResources = new ArrayList(index.get(keyword));
                newResources.add(res);
                index.put(keyword,newResources);
            }
            else{
                List<Resource> newResources = new ArrayList();
                newResources.add(res);
                index.put(keyword,newResources);
            }
        }
    }

    public List<Resource> getResources(String keyword){
        return index.get(keyword);
    }
}
