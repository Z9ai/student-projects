public class PercentageDiscountPricing implements ISalePricing{
    private double percentage;

    public PercentageDiscountPricing(double percentage){
        if (percentage <0||percentage >100){
            throw new IllegalArgumentException();
        }
        this.percentage = percentage;
    }
    public long getTotal(Sale sale){
        return (long) ((double) sale.getPreDiscountTotal() * (100-percentage) *0.01);  // prediscount in cent, percentage von 0 bis 100
    }
}
