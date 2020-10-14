public class BestForCustomerPricing extends ComplexPricing {

    public BestForCustomerPricing(ISalePricing pricing){
        super(pricing);
    }

    public long getTotal(Sale sale) {
        long lowest = 999999999;
        for(ISalePricing p: this.getPricings()){
            if (p.getTotal(sale)< lowest){
                lowest = p.getTotal(sale);
            }
        }
        return lowest;
    }
}
