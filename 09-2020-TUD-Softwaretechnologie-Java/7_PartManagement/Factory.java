public class Factory {
    private ReceivingStock receivingStock;
    private Purchasing purchasing;

    public Factory(Purchasing purchasing, ReceivingStock receivingStock) {
        if (receivingStock == null){
            throw new NullPointerException();
        }
        if (purchasing == null){
            throw new NullPointerException();
        }
        this.receivingStock = receivingStock;
        this.purchasing = purchasing;
    }

    public Purchasing getPurchasing() {
        return purchasing;
    }

    public ReceivingStock getReceivingStock() {
        return receivingStock;
    }

    public static Part createPart(PartType partType, String id, String name){
        if (partType == null || id == null || name == null){
            throw new NullPointerException();
        }
        if (id == ""  || name  == null){
            throw new IllegalArgumentException();
        }
        if(partType == PartType.COMPONENTS){
            return new Components(id, name);
        }
        else if(partType == PartType.SINGLE_COMPONENT){
            return new SingleComponent(id, name);
        }
        else{
            return new Resource(id, name);
        }
    }
}
