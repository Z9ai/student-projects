import java.util.HashMap;
import java.util.Map;
import java.util.Set;

public class Surface extends RenovationObject{
    private double length;
    private double width;
    private Material selectedMaterial;

    public Surface(double length, double width) {
        if(length <= 0 || width <= 0){
            throw new IllegalArgumentException();
        }
        this.length = length;
        this.width = width;
    }

    public void setMaterial(Material material){
        if(material == null){
            throw new NullPointerException();
        }
        this.selectedMaterial = material;
    }

    public double getArea() {
        return length*width;
    }

    public double getLength() {
        return length;
    }

    public double getWidth() {
        return width;
    }

    public double getPrice(){
        return selectedMaterial.getPriceOfASurface(this);
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
        String key = selectedMaterial.getName();
        int value = 0;
        if(materialsActualized.containsKey(selectedMaterial.getName())){
            value = materialsActualized.get(key)  +  se
}
