import java.util.ArrayList;
import java.util.List;

public abstract class AbstractUnit extends AbstractEnterpriseUnit{
    private List<AbstractEnterpriseUnit> childNodes = new ArrayList<AbstractEnterpriseUnit>();

    public AbstractUnit(String name){
        super(name);
    }

    public abstract boolean add(AbstractEnterpriseUnit childNode);  // muss in der unteren Klasse spezifisch implementiert werden, da bei hinzufügen von falschem ein error kommen soll, bei jedem ist das falsche jedoch anderst definiert

    public abstract boolean remove(AbstractEnterpriseUnit childNode);

    public List<AbstractEnterpriseUnit> getNodes(){
        return childNodes;
    }
}
