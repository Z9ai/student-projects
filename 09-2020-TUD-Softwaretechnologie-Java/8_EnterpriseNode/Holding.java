public class Holding extends AbstractUnit{

    public Holding (String name){
        super(name);
    }

    @Override
    public boolean add(AbstractEnterpriseUnit childNode) {
        if (childNode instanceof Company){
            if (!getNodes().contains(childNode)) {
                getNodes().add(childNode);
            }
            return false;
        }
        throw new IllegalArgumentException();
    }

    @Override
    public boolean remove(AbstractEnterpriseUnit childNode){
        if (childNode instanceof Company){
            if (getNodes().contains(childNode)) {
                getNodes().remove(childNode);
            }
            return false;
        }
        throw new IllegalArgumentException();
    }
}
