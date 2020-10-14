public class Sale {
    private long preDiscountTotal;
    private ISalePricing pricing;

    public Sale(long preDiscountTotal, ISalePricing pricing){
        if (pricing == null){
            throw new NullPointerException();
        }
        if (preDiscountTotal<0){
            throw new IllegalArgumentException();
        }
        this.preDiscountTotal = preDiscountTotal;
        this.pricing = pricing;
    }

    public long getPreDiscountTotal(){
        return preDiscountTotal;
    }

    public long getTotal(){
        return pricing.getTotal(this);
    }

    public void setPricing(ISalePricing pricing){
        if (pricing == null){
            throw new NullPointerException();
        }
        this.pricing = pricing;
    }

    public static ISalePricing createPricing(DiscountType discountType, double percentage, long discount, long threshold) {
        if (discountType == null){
            throw new NullPointerException();
        }
        if (discountType == DiscountType.PERCENTAGEDISCOUNT) {   // discountType musste dann auch irgendwann mal DiscountType.PERCENTAGEDISCOUNT gesetzt worden sein
            return new PercentageDiscountPricing(percentage);
        }
        return new AbsoluteDiscountPricing(discount, threshold);
    }
}
