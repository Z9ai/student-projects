public class Company extends AbstractUnit{

    public Company (String name){
        super(name);
    }

    @Override
    public boolean add(AbstractEnterpriseUnit childNode) {
        if (childNode instanceof Division){
            if (!this.getNodes().contains(childNode)) {
                this.getNodes().add(childNode);
            }
            return false;
        }
        throw new IllegalArgumentException();
    }

    @Override
    public boolean remove(AbstractEnterpriseUnit childNode){
        if (childNode instanceof Division){
            if (this.getNodes().contains(childNode)) {
                this.getNodes().remove(childNode);
            }
            return false;
        }
        throw new IllegalArgumentException();
    }
}
