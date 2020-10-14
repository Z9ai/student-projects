public class AbsoluteDiscountPricing implements ISalePricing{
    private long discount;
    private long threshold;

    public AbsoluteDiscountPricing(long discount, long threshold){
        if (discount<0 || threshold <0){
            throw new IllegalArgumentException();
        }
        this.discount = discount;
        this.threshold = threshold;
    }

    public long getTotal(Sale sale){
        if (sale.getPreDiscountTotal()  <=  threshold) {       // unter threshold kann discount gar nicht angewandt werden
            return sale.getPreDiscountTotal();
        }
        if (sale.getPreDiscountTotal()-discount  <  threshold) {    // durch discount darf preis nicht unter threshold fallen
            return threshold;
        }
        return sale.getPreDiscountTotal()-discount;
    }
}
