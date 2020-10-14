public class BestForStorePricing extends ComplexPricing  {

    public BestForStorePricing(ISalePricing pricing){
        super(pricing);
    }

    public long getTotal(Sale sale) {
        long highest = 0;
        for(ISalePricing p: this.getPricings()){
            if (p.getTotal(sale) > highest){
                highest = p.getTotal(sale);
            }
        }
        return highest;
    }
}
