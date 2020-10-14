public class ResourceType {
    private String description;
    private KeywordCollector collector;

    public ResourceType(String desc, KeywordCollector collector){
        this.description = desc;
        this.collector = collector;
    }

    public String getDescription(){
        return description;
    }

    public KeywordCollector getCollector() {
        return collector;
    }
}
