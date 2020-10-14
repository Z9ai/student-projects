import java.util.List;
import java.util.Map;

public class DesktopSearch {
    private Map<String, ResourceType> types;
    private Index index;

    public DesktopSearch(){
    }

    public void registerType(String extension, ResourceType type){
        types.put(extension, type);
    }

    public ResourceType getType(String extension){
        return types.get(extension);
    }

    public void unregisterType(String extension){
        types.remove(extension);
    }

    public void registerResource(Resource res){
        index.add(res);
    }

    public List<Resource> processRequest(String request){
        return index.getResources(request);
    }
}