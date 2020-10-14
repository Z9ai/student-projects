import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

public class StructuredObject extends RenovationObject{
    private Set<RenovationObject> parts = new HashSet();

    public StructuredObject(){
    }

    public void add(RenovationObject renovationObject){
        if(renovationObject == null){
            throw new NullPointerException();
        }
        parts.add(renovationObject);
    }

    public double getPrice(){
        double price = 0;
        for(RenovationObject part : parts){
            price = price + part.getPrice();
        }
        return price;
    }

    public Map<String, Integer> addMaterialRequirements(Map<String, Integer> materials){
        Set<String> keys = materials.keySet();
        for(String k : keys){
            if(k == null){
                throw new NullPointerException();
            }
        }
        if(materials == null || materials.containsValue(null)){
            throw new NullPointerException();
        }
        Map<String, Integer> materialsActualized = new HashMap<>();
        for(Map.Entry entry : materials.entrySet()){
            materialsActualized.put((String) entry.getKey(), (int) entry.getValue());
        }
        for(RenovationObject part : parts){
            materialsActualized.putAll(part.addMaterialRequirements(materialsActualized));
        }
        return materialsActualized;
    }
}