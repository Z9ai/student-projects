public class ReceivingStock extends Stock{
    private int minStockItems;
    private int maxStockItems;

    public ReceivingStock(int minStockItems, int maxStockItems) {
        if (minStockItems <0   || maxStockItems  <= minStockItems){
            throw new IllegalArgumentException();
        }
        this.minStockItems = minStockItems;
        this.maxStockItems = maxStockItems;
    }

    @Override
    public boolean insert(Part part, int amount) {
        if(amount > maxStockItems){
            return false;
        }
        return super.insert(part, amount);
    }

    public int getMinStockItems() {
        return minStockItems;
    }

    public int getMaxStockItems() {
        return maxStockItems;
    }
}
