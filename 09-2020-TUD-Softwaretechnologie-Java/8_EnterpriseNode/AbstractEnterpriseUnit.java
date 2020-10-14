public abstract class AbstractEnterpriseUnit implements EnterpriseNode{
    private String name;

    public AbstractEnterpriseUnit(String name){
        this.name = name;
    }

    @Override
    public String getName() {
        return name;
    }
}
