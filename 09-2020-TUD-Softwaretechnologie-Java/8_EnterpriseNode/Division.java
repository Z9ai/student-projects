public class Division extends AbstractUnit{

    public Division (String name){
        super(name);
    }

    @Override
    public boolean add(AbstractEnterpriseUnit childNode) {
        if (childNode instanceof Team){
            if (!getNodes().contains(childNode)) {
                getNodes().add(childNode);
            }
            return false;
        }
        throw new IllegalArgumentException();
    }

    @Override
    public boolean remove(AbstractEnterpriseUnit childNode){
        if (childNode instanceof Team){
            if (getNodes().contains(childNode)) {
                getNodes().remove(childNode);
            }
            return false;
        }
        throw new IllegalArgumentException();
    }
}
